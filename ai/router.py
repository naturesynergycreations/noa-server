from ai.groq_ai import ask_ai, summarize_search
from search.tavily_search import search_web

LATEST_WORDS = [
    "latest",
    "current",
    "today",
    "news",
    "weather",
    "score",
    "election",
    "president",
    "prime minister",
    "chief minister",
    "cm",
    "who won"
]


def ask(question):

    q = question.lower()

    if any(word in q for word in LATEST_WORDS):

        search_result = search_web(question)

        if search_result:
            return summarize_search(search_result)

    return ask_ai(question)