import shutil
import json
import subprocess
from contextlib import contextmanager
from pathlib import Path
from typing import Type

from instawow.pkg_archives import (
    Archive,
    find_archive_addon_tocs,
    make_archive_member_filter_fn,
)

class ArchiveExtractor:
    _path: Path

    def __init__(self, path: Path):
        self._path = path

    def extract(self, items: list[str], output: Path):
        raise NotImplementedError()

    def list(self):
        raise NotImplementedError()

    @staticmethod
    def good() -> bool:
        raise NotImplementedError()

class TheUnarchiver(ArchiveExtractor):
    def extract(self, items: list[str], output: Path):
        subprocess.check_call([
            "unar",
            "-quiet",
            "-o",
            str(output),
            self._path,
            *(item for item in items),
        ])

    def list(self) -> list[str]:
        output = json.loads(subprocess.check_output(
            ["lsar", "-j", "-jss", self._path],
        ))

        assert output["lsarFormatVersion"] == 2

        return [item["XADFileName"] for item in output["lsarContents"]]

    @staticmethod
    def good() -> bool:
        return (shutil.which("unar") is not None
                and shutil.which("lsar") is not None)

def get_archive_extractor(path: Path) -> ArchiveExtractor:
    extractors: list[Type[ArchiveExtractor]] = [TheUnarchiver]
    for extractor_cls in extractors:
        if extractor_cls.good():
            return extractor_cls(path)
    raise RuntimeError("No supported unarchiver found.")

@contextmanager
def open_rar_archive(path: Path):
    extractor = get_archive_extractor(path)
    top_level_folders = {h for _, h in find_archive_addon_tocs(extractor.list())}
    should_extract = make_archive_member_filter_fn(top_level_folders)

    def extract(parent: Path):
        extractor.extract([item for item in extractor.list() if should_extract(item)], parent)

    yield Archive(top_level_folders, extract)
