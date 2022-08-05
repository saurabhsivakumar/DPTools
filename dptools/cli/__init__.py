from dptools import __version__
from importlib import import_module
import argparse

commands = (
    "train",
    "parity",
    "run",
    "sample",
    "convert",
    "set",
    "get",
    #"info": "dptools.?", show env stuff
)

class BaseCLI:
    help_info = ""
    def __init__(self, parser):
        self.parser = parser

    def add_args(self):
        '''Command specific arguments'''
        pass

    def main(self, args):
        '''Command specific main method'''
        pass


def main():
    parser = argparse.ArgumentParser(prog="dptools",
                                     description="DPTools CLI for doing stuff with deepmd-kit",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     )
    parser.add_argument("--version", action="version", version=__version__)
    subparsers = parser.add_subparsers(dest="command")
    # TODO: Add logging
    command_clis = {}
    for comm in commands:
        subparser = subparsers.add_parser(comm, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        mod = "dptools.cli." + comm
        CLI = import_module(mod).CLI
        cli = CLI(subparser)
        cli.add_args()
        command_clis[comm] = cli

    parsed_args = parser.parse_args()
    command_clis[parsed_args.command].main(parsed_args)