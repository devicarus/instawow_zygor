import click

import instawow
from instawow.config_ctx import config

from instawow_zygor.config import Config
from instawow_zygor.resolver import ZygorResolver


@click.group()
def zygor():
    pass

@zygor.command()
@click.argument("folder_key", type=str)
def set_folder_key(folder_key: str):
    Config(config().global_config.plugins_config_dir/"zygor.json").set("folder_key", folder_key)

@instawow.plugins.hookimpl
def instawow_add_commands():
    return (zygor,)

@instawow.plugins.hookimpl
def instawow_add_resolvers():
    return (ZygorResolver,)