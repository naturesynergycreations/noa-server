WAKE_WORDS = [
    "noa",
    "noah",
    "nova",
    "hey noa",
    "hi noa",
    "hello noa",
    "hey noah",
    "hi noah",
    "hello noah",
    "okay noa",
    "ok noa"
]


def is_wake_word(text):
    if not text:
        return False

    text = text.lower().strip()

    return any(word in text for word in WAKE_WORDS)


def remove_wake_word(text):
    if not text:
        return ""

    text = text.lower()

    for word in sorted(WAKE_WORDS, key=len, reverse=True):
        text = text.replace(word, "")

    return text.strip(" ,?.!")