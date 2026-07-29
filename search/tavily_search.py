import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def search_web(query):

    try:

        response = client.search(
            query=query,
            search_depth="basic",
            max_results=3
        )

        results = response.get("results", [])

        if not results:
            return None

        text = ""

        for result in results:
            text += result["content"] + "\n\n"

        return text

    except Exception as e:
        print("Tavily Error:", e)
        return None