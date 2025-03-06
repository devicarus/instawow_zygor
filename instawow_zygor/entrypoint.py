import click

import instawow
from instawow.cli import ConfigBoundCtxProxy

from instawow_zygor.config import Config
from instawow_zygor.resolver import ZygorResolver


@click.group()
def zygor():
    pass

@zygor.command()
@click.argument("folder_key", type=str)
@click.pass_obj
def set_folder_key(config_ctx: ConfigBoundCtxProxy, folder_key: str):
    Config(config_ctx.config.global_config.plugins_config_dir/"zygor.json").set("folder_key", folder_key)

@instawow.plugins.hookimpl
def instawow_add_commands():
    return (zygor,)

@instawow.plugins.hookimpl
def instawow_add_resolvers():
    return (ZygorResolver,)