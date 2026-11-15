/**
 * Spending Tracker: Google Sheet backend.
 *
 * Paste this into Extensions → Apps Script of a new Google Sheet,
 * set SECRET to your own secret (the same one you type into the app),
 * then Deploy → New deployment → Web app
 * (Execute as: Me, Who has access: Anyone).
 *
 * Entries go to the "Entries" tab, your target and limit to the "Settings" tab.
 */
const SECRET = 'PASTE-YOUR-SECRET-HERE';

function doGet(e) { return handle_((e && e.parameter) || {}); }

function doPost(e) {
  let p = {};
  try { p = JSON.parse(e.postData.contents); } catch (err) {}
  return handle_(p);
}

function handle_(p) {
  if (!SECRET || SECRET === 'PASTE-YOUR-SECRET-HERE') return out_({ ok: false, error: 'no_secret_set' });
  if (p.secret !== SECRET) return out_({ ok: false, error: 'unauthorised' });

  const lock = LockService.getScriptLock();
  lock.waitLock(15000);
  try {
    const ss = SpreadsheetApp.getActive();
    const sh = sheet_(ss, 'Entries', ['ID', 'Date', 'Amount (€)', 'Category', 'Note', 'Created']);
    const st = sheet_(ss, 'Settings', ['Setting', 'Value']);
    if (st.getLastRow() < 3) st.getRange(2, 1, 2, 2).setValues([['Minimum target', 600], ['Limit', 800]]);

    switch (p.action) {
      case 'add':
        sh.appendRow([String(p.id), toDate_(p.date), Number(p.amount), String(p.cat || ''), String(p.note || ''), Number(p.created) || Date.now()]);
        break;
      case 'update': {
        const r = findRow_(sh, p.id);
        if (!r) return out_({ ok: false, error: 'not_found' });
        sh.getRange(r, 2, 1, 4).setValues([[toDate_(p.date), Number(p.amount), String(p.cat || ''), String(p.note || '')]]);
        break;
      }
      case 'delete': {
        const r = findRow_(sh, p.id);
        if (r) sh.deleteRow(r);
        break;
      }
      case 'settings':
        st.getRange(2, 2, 2, 1).setValues([[Number(p.min)], [Number(p.max)]]);
        break;
      default: // 'list'
        break;
    }
    return out_({
      ok: true,
      entries: list_(sh),
      min: Number(st.getRange(2, 2).getValue()) || 600,
      max: Number(st.getRange(3, 2).getValue()) || 800,
      sheetUrl: ss.getUrl()
    });
  } finally {
    lock.releaseLock();
  }
}

function sheet_(ss, name, header) {
  let sh = ss.getSheetByName(name);
  if (!sh) {
    sh = ss.insertSheet(name);
    sh.getRange(1, 1, 1, header.length).setValues([header]).setFontWeight('bold');
    sh.setFrozenRows(1);
    if (name === 'Entries') {
      sh.getRange('A:A').setNumberFormat('@');
      sh.getRange('B:B').setNumberFormat('d mmm yyyy');
      sh.getRange('C:C').setNumberFormat('#,##0.00');
      sh.hideColumns(1);
      sh.hideColumns(6);
    }
  }
  return sh;
}

function toDate_(s) {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(s));
  return m ? new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3]), 12) : String(s);
}

function list_(sh) {
  const n = sh.getLastRow() - 1;
  if (n < 1) return [];
  const tz = Session.getScriptTimeZone();
  return sh.getRange(2, 1, n, 6).getValues()
    .filter(r => r[0] !== '')
    .map(r => ({
      id: String(r[0]),
      date: (r[1] && typeof r[1].getTime === 'function') ? Utilities.formatDate(r[1], tz, 'yyyy-MM-dd') : String(r[1]),
      amount: Number(r[2]) || 0,
      cat: String(r[3]),
      note: String(r[4]),
      created: Number(r[5]) || 0
    }));
}

function findRow_(sh, id) {
  const cell = sh.getRange('A:A').createTextFinder(String(id)).matchEntireCell(true).findNext();
  return cell ? cell.getRow() : 0;
}

function out_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
