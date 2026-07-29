from search.tavily_search import search_web
from ai.groq_ai import summarize_search

query = input("Search : ")

search_result = search_web(query)

summary = summarize_search(search_result)

print("\nSummary:\n")
print(summary)