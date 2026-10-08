"""Sprachpartner / Partenaire linguistique

A conversation partner that chats with you in German or French and
corrects your grammar as you go. Powered by Claude.

Usage:
    python language_tutor.py                    # asks which language you want
    python language_tutor.py --language german --level B1
    python language_tutor.py -l french

While chatting:
    /help     show the commands
    /explain  ask for a fuller English explanation of the last correction
    /quit     end the session
"""

import argparse
import sys

import anthropic

MODEL = "claude-opus-5-5"

LANGUAGES = {
    "german": {
        "name": "German",
        "native_name": "Deutsch",
        "greeting_prompt": "Hallo! Ich möchte Deutsch üben.",
    },
    "french": {
        "name": "French",
        "native_name": "Français",
        "greeting_prompt": "Bonjour ! Je voudrais pratiquer le français.",
    },
}

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

SYSTEM_PROMPT = """\
You are a warm, patient {language} conversation partner and tutor. The learner \
is an English speaker practising {language} at roughly CEFR level {level}.

How to respond to every learner message:

1. Corrections first. If the learner's message has grammar, spelling, word-order, \
gender/article, conjugation or word-choice mistakes, start with a short block:

   ✏️ Correction: <their sentence rewritten correctly in {language}>
   • <one short bullet per mistake, in English: what was wrong and the rule behind it>

   Only correct real mistakes, and be sure before you call something wrong: if the \
learner's version is grammatical and a native speaker would accept it, it is not a \
mistake. Double-check prepositions with places (e.g. German "von den Philippinen"). \
If a phrasing is correct but unnatural, you may add \
one bullet starting with "Tip:" suggesting what a native speaker would say. If the \
message is error-free, write "✅ Perfekt!" (German) or "✅ Parfait !" (French) instead \
of the block. If the learner writes in English, gently show how to say it in \
{language} instead of correcting it.

2. Then continue the conversation in {language}. Keep it natural and friendly: \
react to what they said, share a little, and end with a question so the \
conversation keeps going. Pitch your vocabulary and grammar to level {level} — \
slightly challenging but understandable. Keep this part to 2-5 sentences.

3. If you use a word that is likely new at this level, you may add it in a short \
"📖 Vocabulary:" line at the end (word — English meaning). At most three words.

When the learner types "/explain", give a fuller explanation in English of the \
grammar behind your most recent correction, with two or three extra example \
sentences, then invite them to continue in {language}.

Do not switch to English for the conversation itself unless the learner is \
clearly lost and asks for help.
"""

HELP_TEXT = """\
Commands:
  /explain  get a fuller English explanation of the last correction
  /help     show this message
  /quit     end the session
"""


def choose_language() -> str:
    print("Which language would you like to practise?")
    print("  1) German / Deutsch")
    print("  2) French / Français")
    while True:
        choice = input("> ").strip().lower()
        if choice in ("1", "german", "deutsch", "de"):
            return "german"
        if choice in ("2", "french", "français", "francais", "fr"):
            return "french"
        print("Please type 1 for German or 2 for French.")


def send(client: anthropic.Anthropic, system: str, history: list) -> bool:
    """Stream Claude's reply to the terminal and append it to history.

    Returns False if the reply could not be completed, so the caller can drop
    the learner's last message and let them try again.
    """
    print()
    with client.beta.messages.stream(
        model=MODEL,
        max_tokens=16000,
        system=system,
        messages=history,
        thinking={"type": "adaptive"},
        output_config={"effort": "medium"},
        # If a reply is declined by a safety classifier, retry it on
        # Anthropic's recommended fallback model instead of failing.
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
        response = stream.get_final_message()
    print("\n")

    if response.stop_reason == "refusal":
        print("(Sorry, I couldn't answer that one. Try saying something else.)\n")
        return False

    # Append the full content (not just the text) so the conversation history
    # stays exactly as Claude produced it.
    history.append({"role": "assistant", "content": response.content})
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Practise German or French with an AI tutor.")
    parser.add_argument("-l", "--language", choices=sorted(LANGUAGES), help="language to practise")
    parser.add_argument("--level", choices=LEVELS, default="A2", help="your CEFR level (default: A2)")
    args = parser.parse_args()

    language_key = args.language or choose_language()
    language = LANGUAGES[language_key]
    system = SYSTEM_PROMPT.format(language=language["name"], level=args.level)

    client = anthropic.Anthropic()
    history = [{"role": "user", "content": language["greeting_prompt"]}]

    print(f"\n=== {language['native_name']} practice (level {args.level}) ===")
    print("Type your message and press Enter. /help for commands, /quit to stop.")

    try:
        send(client, system, history)
        while True:
            try:
                user_text = input("You: ").strip()
            except EOFError:
                break
            if not user_text:
                continue
            if user_text.lower() in ("/quit", "/exit"):
                break
            if user_text.lower() == "/help":
                print(HELP_TEXT)
                continue

            history.append({"role": "user", "content": user_text})
            if not send(client, system, history):
                history.pop()
    except KeyboardInterrupt:
        pass
    except anthropic.AuthenticationError:
        sys.exit("Authentication failed. Set ANTHROPIC_API_KEY (see README.md).")
    except anthropic.RateLimitError:
        sys.exit("Rate limited by the API. Wait a moment and try again.")
    except anthropic.APIConnectionError:
        sys.exit("Could not reach the Claude API. Check your internet connection.")
    except anthropic.APIStatusError as e:
        sys.exit(f"API error {e.status_code}: {e.message}")

    print("\nTschüss! / À bientôt !")


if __name__ == "__main__":
    main()
