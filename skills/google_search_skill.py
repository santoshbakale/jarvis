from skills.base import BaseSkill
from googlesearch import search
import requests
from bs4 import BeautifulSoup

class GoogleSearchSkill(BaseSkill):
    @property
    def name(self) -> str:
        return "google_search"

    @property
    def description(self) -> str:
        return "Search Google for real-time information, websites, and deep-dive facts."

    def execute(self, query: str, num_results: int = 5) -> str:
        """Search Google and return simplified results."""
        try:
            results = []
            # Performing the search
            for url in search(query, num_results=num_results, advanced=True):
                snippet = url.description if url.description else "No description available."
                results.append(f"Title: {url.title}\nSnippet: {snippet}\nLink: {url.url}")
            
            if not results:
                return f"I couldn't find any Google results for '{query}', Sir."
                
            return "\n\n---\n\n".join(results)
        except Exception as e:
            return f"An error occurred while accessing Google: {str(e)}"

if __name__ == "__main__":
    skill = GoogleSearchSkill()
    print(skill.execute("Latest news on Avengers Doomsday"))
