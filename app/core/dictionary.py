WORDS = set()

def load_dictionary():
    global WORDS
    with open("words.txt") as f:
        WORDS = {w.strip().lower() for w in f}

def is_valid_word(word: str) -> bool:
    return word.lower() in WORDS