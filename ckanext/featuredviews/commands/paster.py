from __future__ import print_function
import sys
from ckan.lib.cli import CkanCommand
from ckanext.featuredviews.db import setup as model_setup

# Paster commands for CKAN 2.8 and below


class FeaturedCommands(CkanCommand):
    """
    ckanext-featuredviews commands:

    Usage::

        paster featured migrate
    """
    summary = __doc__.split('\n')[0]
    usage = __doc__

    def __init__(self, name):
        super(FeaturedCommands, self).__init__(name)

    def command(self):
        self._load_config()

        if len(self.args) == 0:
            self.parser.print_usage()
            sys.exit(1)
        cmd = self.args[0]
        if cmd == 'migrate':
            self._migrate()
        else:
            print("Command {0} not recognized".format(cmd))

    def _migrate(self):
        model_setup()
