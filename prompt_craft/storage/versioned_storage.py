from abc import ABC, abstractmethod
from typing import List, Optional

from prompt_craft.models.prompt import Prompt


class VersionedPromptStorage(ABC):

    @abstractmethod
    def save_prompt(self, prompt: Prompt) -> None:
        """Сохраняет новую версию промпта."""
        pass

    @abstractmethod
    def get_prompt(self, name: str, version: Optional[int] = None) -> Optional[Prompt]:
        """Загружает определенную версию промпта или последнюю версию, если версия не указана."""
        pass

    @abstractmethod
    def get_all_versions(self, name: str) -> List[int]:
        """Возвращает список всех версий для указанного промпта."""
        pass

    @abstractmethod
    def get_latest_version(self, name: str) -> Optional[int]:
        """Возвращает последнюю версию промпта."""
        pass
