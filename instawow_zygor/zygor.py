import re

from instawow.wow_installations import Flavour

from instawow_zygor.mediafire import MediaFireFile

_zygor_major_version = {
    Flavour.Retail: "9",
    Flavour.Classic: "2",
    Flavour.VanillaClassic: "1"
}

def select_zygor_file(files: list[MediaFireFile], flavour: Flavour) -> MediaFireFile:
    for file in files:
        if get_zygor_version_from_filename(file.name).startswith(_zygor_major_version.get(flavour)):
            return file
    raise RuntimeError("Could not find a suitable ZygorGuidesViewer file in the Mediafire folder.")

def get_zygor_version_from_filename(filename: str) -> str:
    if match := re.search(r'\d+\.\d+\.\d+', filename):
        return match.group()
    raise RuntimeError("Could not find ZygorGuidesViewer version in the filename.")
