# hello-world
This is my first repository

Hello there, this is my yet another try at learning to code.

## Language Tutor (German / French)

`language_tutor.py` is a conversation partner that chats with you in **German** or
**French** and corrects your grammar as you go. Each reply:

1. **✏️ Correction** – your sentence rewritten correctly, with a short English note on each mistake (or ✅ if it was perfect)
2. **The conversation continues** in your chosen language, ending with a question
3. **📖 Vocabulary** – new words with English meanings (optional)

### Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key-here"   # get one at https://console.anthropic.com
```

### Run it

```bash
python language_tutor.py                          # asks: German or French?
python language_tutor.py --language german --level B1
python language_tutor.py -l french --level A1
```

`--level` is your CEFR level (A1 beginner → C2 fluent, default A2). The tutor adjusts its vocabulary to match.

While chatting, type `/explain` for a deeper English explanation of the last correction, `/help` for commands, or `/quit` to stop.

### On your phone

`web/tutor.html` is the same tutor as a mobile web page, published as a Claude artifact:
https://claude.ai/artifact/SdXiBfgpVMPaKeaesQJyh8

It runs inside the Claude app (or claude.ai) on your own Claude account, so no API key is needed. Extras:

- **Role-play scenes**: café, bakery, directions, hotel, doctor, job interview, small talk
- **Mistake notebook**: every correction is saved, and a review drill quizzes you on your recent mistakes
- **Natural voice**: replies are read aloud using the most natural female voice on your device (pick another under **Voice**, plus speed and auto-read). Download a free Enhanced/Premium voice on your phone for the best sound; the Voice panel explains how.
- **Speaking**: dictate with your phone keyboard's microphone. For real spoken conversation, use Claude voice mode with the instructions in [`voice-mode-tutor.md`](voice-mode-tutor.md).

### With a microphone (GitHub Pages)

Claude artifacts can't use the microphone, so the same page is also published as a standalone site from `docs/index.html` (regenerate it with `python web/build_pages.py` after editing `web/tutor.html`). There it gets:

- **Mic button**: tap, speak, and your answer is sent when you pause
- **Hands-free**: the tutor reads her reply aloud, then listens for yours, like a normal conversation
- **Pauses are fine**: your answer is sent only after you've been quiet for a moment (1.5, 3 or 5 seconds, set under the speaker icon); tap the mic button to send right away
- **Natural voice** (optional): paste an ElevenLabs API key under the speaker icon for a human-sounding voice; the phone's voice is the fallback

The standalone site calls the Claude API with your own API key (from console.anthropic.com), which is saved only in your browser. Usage is billed to your API account.

On a phone, use **Add to Home Screen** (Safari: Share → Add to Home Screen) to get the Tandem icon and open it full-screen like an app. The icons are drawn by `python web/make_icons.py` (needs Pillow) and the app manifest is written by `web/build_pages.py`.

To put it online: repository **Settings → Pages → Build and deployment → Deploy from a branch**, pick the branch and the `/docs` folder. It will be at `https://vernaellaine.github.io/hello-world/`.
