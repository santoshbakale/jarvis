from abc import ABC, abstractmethod

class BaseSkill(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the skill."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """A description of what the skill does."""
        pass

    @abstractmethod
    def execute(self, *args, **kwargs):
        """Execute the skill."""
        pass
