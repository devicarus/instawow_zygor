import datetime
import re
from dataclasses import dataclass

from curl_cffi import requests


@dataclass
class MediaFireFile:
    name: str
    link: str
    created: datetime.datetime

    def get_direct_url(self) -> str:
        response = requests.get(self.link, impersonate='chrome')
        response.raise_for_status()
        body = response.text
        if match := re.search(r'(?<=href=\")(?:http|https)://download[^\"]+', body):
            return match.group()
        raise RuntimeError("Could not find a download URL in the Mediafire body.")


class MediaFireClient:
    _api_url = "https://www.mediafire.com/api/1.4/folder/get_content.php?r=megafire&content_type=files&version=1.5&response_format=json&folder_key="

    def folder_get_files(self, folder_key: str) -> list[MediaFireFile]:
        response = requests.get(self._api_url + folder_key, impersonate='chrome')
        response.raise_for_status()
        data = response.json()

        files: list[MediaFireFile] = []
        for file in data['response']['folder_content']['files']:
            files.append(MediaFireFile(
                name=file['filename'],
                link=file['links']['normal_download'],
                created=datetime.datetime.fromisoformat(file['created_utc'])
            ))

        return files
