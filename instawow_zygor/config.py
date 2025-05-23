import json
from pathlib import Path

from instawow.config import make_plugin_dirs

CONFIG_PATH = make_plugin_dirs("zygor").config/"config.json"

class Config:
    _path: Path
    _data: dict = None

    def __init__(self, path: Path):
        self._path = path

    def set(self, key, value):
        if self._data is None:
            self._load()
        self._data[key] = value
        self._save()

    def get(self, key, default=None):
        if self._data is None:
            self._load()
        return self._data.get(key, default)

    def _load(self):
        try:
            with self._path.open('r') as file:
                self._data = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            self._data = {}

    def _save(self):
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open('w') as file:
            json.dump(self._data, file, indent=4)
