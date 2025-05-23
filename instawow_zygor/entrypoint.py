import click

import instawow

from instawow_zygor.config import Config, CONFIG_PATH
from instawow_zygor.resolver import ZygorResolver


@click.group()
def zygor():
    pass

@zygor.command()
@click.argument("folder_key", type=str)
def set_folder_key(folder_key: str):
    Config(CONFIG_PATH).set("folder_key", folder_key)

@instawow.plugins.hookimpl
def instawow_add_commands():
    return (zygor,)

@instawow.plugins.hookimpl
def instawow_add_resolvers():
    return (ZygorResolver,)
