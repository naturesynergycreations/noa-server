import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_web(query):
    try:
        response = client.search(
            query=query,
            search_depth="basic",
            max_results=3
        )

        answer = ""

        for result in response.get("results", []):
            answer += result.get("content", "") + "\n"

        return answer if answer else "No information found."

    except Exception as e:
        print(f"Tavily Error: {e}")
        return "Unable to retrieve information from the internet at the moment."