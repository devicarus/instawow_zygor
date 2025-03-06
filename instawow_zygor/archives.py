from contextlib import contextmanager
from pathlib import Path
import rarfile

from instawow.pkg_archives import (
    Archive,
    find_archive_addon_tocs,
    make_archive_member_filter_fn,
)


@contextmanager
def open_rar_archive(path: Path):
    with rarfile.RarFile(path) as rf:
        top_level_folders = {h for _, h in find_archive_addon_tocs(rf.namelist())}
        should_extract = make_archive_member_filter_fn(top_level_folders)

    def extract(parent: Path):
        for member in rf.namelist():
            if should_extract(member):
                rf.extract(member, parent)

    yield Archive(top_level_folders, extract)
