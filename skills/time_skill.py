from skills.base import BaseSkill
from datetime import datetime

class TimeSkill(BaseSkill):
    """Provides current time and date information."""
    
    @property
    def name(self) -> str:
        return "time"
    
    @property
    def description(self) -> str:
        return "Get current time, date, or day of week"
    
    def execute(self, query: str = "time") -> str:
        """
        Execute the time skill.
        
        Args:
            query: What time information to get (time, date, day, full)
        
        Returns:
            Formatted time/date string
        """
        now = datetime.now()
        
        query = query.lower()
        
        if "date" in query:
            return now.strftime("%A, %B %d, %Y")
        elif "day" in query:
            return now.strftime("%A")
        elif "full" in query or "datetime" in query:
            return now.strftime("%A, %B %d, %Y at %I:%M %p")
        else:  # default to time
            return now.strftime("%I:%M %p")
