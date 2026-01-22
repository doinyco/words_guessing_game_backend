from pathlib import Path

WORDS = set()

def load_dictionary():
    global WORDS
    words_path = Path(__file__).resolve().parent / "words.txt"
    with words_path.open("r", encoding="utf-8") as f:
        WORDS = {line.strip().lower() for line in f if line.strip()}

def is_valid_word(word: str) -> bool:
    return word.strip().lower() in WORDS