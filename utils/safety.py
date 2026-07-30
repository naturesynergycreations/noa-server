BAD_WORDS = [
    "sex",
    "porn",
    "nude",
    "naked",
    "xxx",
    "adult",
    "18+",
    "18",
    "18 +",
    "18+ content",
    "18 + content",
    "18+content",
    "kiss",
    "boobs",
    "breast",
    "private part",
    "condom"
]


def check_question(question):
    """
    Returns:
        normal
        restricted
    """

    if not question:
        return "normal"

    q = question.lower().strip()

    for word in BAD_WORDS:
        if word in q:
            return "restricted"

    return "normal"