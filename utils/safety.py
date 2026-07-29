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
    "kiss",
    "boobs",
    "breast",
    "private part",
    "condom"
]

MAX_WORDS = 15
MAX_CHARACTERS = 100


def check_question(question):

    if not question:
        return "normal"

    q = question.lower()

    # Check 18+ words
    for word in BAD_WORDS:
        if word in q:
            return "restricted"

    # Check very lengthy question
    if len(q.split()) > MAX_WORDS:
        return "long"

    return "normal"