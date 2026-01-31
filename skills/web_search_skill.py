from skills.base import BaseSkill
from duckduckgo_search import DDGS
import json

class WebSearchSkill(BaseSkill):
    @property
    def name(self) -> str:
        return "web_search"

    @property
    def description(self) -> str:
        return "Search the internet for real-time information, news, and facts."

    def execute(self, query: str, max_results: int = 5) -> str:
        """Search the web for the given query."""
        try:
            with DDGS() as ddgs:
                results = ddgs.text(query, max_results=max_results)
                if not results:
                    return f"No results found for '{query}'."
                
                formatted_results = []
                for i, r in enumerate(results, 1):
                    formatted_results.append(f"{i}. {r['title']}\n   {r['body']}\n   URL: {r['href']}")
                
                return "\n\n".join(formatted_results)
        except Exception as e:
            return f"An error occurred while searching: {str(e)}"

if __name__ == "__main__":
    skill = WebSearchSkill()
    print(skill.execute("Current weather in London"))
