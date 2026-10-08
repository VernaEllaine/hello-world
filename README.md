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
- **Listen**: replies are read aloud in a German or French voice
- **Speaking**: dictate with your phone keyboard's microphone
