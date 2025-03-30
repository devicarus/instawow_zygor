from instawow.definitions import Defn, ChangelogFormat, SourceMetadata
from instawow.resolvers import BaseResolver, PkgCandidate
from instawow.results import PkgNonexistent, PkgSourceInvalid
from instawow.config_ctx import config

from instawow_zygor.mediafire import MediaFireClient
from instawow_zygor.archive import open_rar_archive
from instawow_zygor.config import Config
from instawow_zygor.zygor import select_zygor_file, get_zygor_version_from_filename


class ZygorResolver(BaseResolver):
    metadata = SourceMetadata(
        id='zygor',
        name='ZygorGuidesViewer',
        strategies=frozenset(),
        changelog_format=ChangelogFormat.Html,
        addon_toc_key=None,
    )
    requires_access_token = None
    archive_opener = staticmethod(open_rar_archive)

    async def resolve_one(self, defn: Defn, metadata: None) -> PkgCandidate:
        if defn.alias != 'zygor':
            raise PkgNonexistent

        folder_key = Config(config().global_config.plugins_config_dir/"zygor.json").get("folder_key")
        if not folder_key:
            raise PkgSourceInvalid

        files = MediaFireClient().folder_get_files(folder_key)
        file = select_zygor_file(files, config().game_flavour)

        return PkgCandidate(
            id='1',
            slug=defn.alias,
            name='ZygorGuidesViewer',
            description='Zygor Guides',
            url='https://zygorguides.com/',
            download_url=file.get_direct_url(),
            date_published=file.created,
            version=get_zygor_version_from_filename(file.name),
            changelog_url='https://zygorguides.com/archive/',
        )
