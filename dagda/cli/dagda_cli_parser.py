import argparse
import sys
from cli.vuln_cli_parser import VulnCLIParser
from cli.check_cli_parser import CheckCLIParser
from cli.history_cli_parser import HistoryCLIParser


class DagdaCLIParser:

    # -- Public methods

    # DagdaCLIParser Constructor
    def __init__(self):
        super(DagdaCLIParser, self).__init__()
        self.parser = DagdaGlobalParser(prog='dagda.py', usage=dagda_global_parser_text, add_help=False)
        self.parser.add_argument('command', choices=['vuln', 'check', 'history'])
        self.parser.add_argument('-h', '--help', action=_HelpAction)
        self.parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.4.0')
        self.args, self.unknown = self.parser.parse_known_args()
        if self.get_command() == 'vuln':
            self.extra_args = VulnCLIParser()
        elif self.get_command() == 'check':
            self.extra_args = CheckCLIParser()
        elif self.get_command() == 'history':
            self.extra_args = HistoryCLIParser()

    # -- Getters

    # Gets command
    def get_command(self):
        return self.args.command

    # Gets extra args
    def get_extra_args(self):
        return self.extra_args


# Overrides Help Action class

class _HelpAction(argparse._HelpAction):

    def __call__(self, parser, namespace, values, option_string=None):
        if sys.argv[1] != 'vuln' and sys.argv[1] != 'check' and sys.argv[1] != 'history':
            parser.print_help()
            parser.exit()


# Custom Parser

class DagdaGlobalParser(argparse.ArgumentParser):

    # Overrides the error method
    def error(self, message):
        self.print_usage()
        exit(2)

    # Overrides the format help method
    def format_help(self):
        return dagda_global_parser_text


# -- Custom message

dagda_global_parser_text = '''dagda.py [--version] [--help] <command> [args]

Dagda Commands:
  vuln                  perform operations over your personal CVE, BID &
                        ExploitDB database
  check                 perform the analysis of known vulnerabilities in
                        docker images/containers
  history               retrieve the analysis history for the docker images

Optional Arguments:
  -h, --help            show this help message and exit
  -v, --version         show the version message and exit
'''
