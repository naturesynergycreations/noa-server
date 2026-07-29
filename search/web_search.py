from duckduckgo_search import DDGS


def search_web(query):
    try:
        search_query = f"{query} latest"

        with DDGS() as ddgs:
            results = list(ddgs.text(search_query, max_results=5))

        if not results:
            return None

        answer = ""

        for result in results:
            answer += (
                f"{result['title']}\n"
                f"{result['body']}\n\n"
            )

        return answer

    except Exception as e:
        print(e)
        return None