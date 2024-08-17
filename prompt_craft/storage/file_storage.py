import json
import os
from typing import List, Optional

from prompt_craft.models.prompt import Prompt
from prompt_craft.storage.versioned_storage import VersionedPromptStorage


class FileVersionedPromptStorage(VersionedPromptStorage):

    def __init__(self, storage_dir: str = "prompt_storage"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    def save_prompt(self, prompt: Prompt) -> None:
        """Сохраняет новую версию промпта в файл."""
        file_path = self._get_file_path(prompt.name)
        all_prompts = self._load_prompts(file_path)

        all_prompts[str(prompt.version)] = prompt.model_dump(mode="json")

        # Записываем данные в файл
        with open(file_path, 'w') as f:
            json.dump(all_prompts, f, indent=4)

    def get_prompt(self, name: str, version: Optional[int] = None) -> Optional[Prompt]:
        """Загружает конкретную версию промпта или последнюю, если версия не указана."""
        file_path = self._get_file_path(name)
        all_prompts = self._load_prompts(file_path)

        if not all_prompts:
            return None

        if version is None:
            version = self.get_latest_version(name)

        prompt_data = all_prompts.get(str(version))
        if prompt_data:
            return Prompt(**prompt_data)

        return None

    def get_all_versions(self, name: str) -> List[int]:
        """Возвращает список всех версий для указанного промпта."""
        file_path = self._get_file_path(name)
        all_prompts = self._load_prompts(file_path)
        return [int(v) for v in all_prompts.keys()]

    def get_latest_version(self, name: str) -> Optional[int]:
        """Возвращает последнюю версию промпта."""
        all_versions = self.get_all_versions(name)
        if all_versions:
            return max(all_versions)
        return None

    def _get_file_path(self, name: str) -> str:
        """Возвращает путь к файлу с данными для конкретного промпта."""
        return os.path.join(self.storage_dir, f"{name}.json")

    def _load_prompts(self, file_path: str) -> dict:
        """Загружает все данные о версиях промпта из файла."""
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)

        return {}
