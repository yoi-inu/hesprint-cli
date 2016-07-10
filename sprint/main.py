#!/usr/bin/env python
"""
HackerEarth Sprint CLI

Usage:
    sprint login
    sprint logout
    sprint access <sprint_slug>
    sprint register
    sprint register <sprint_slug>
    sprint team
    sprint team [<team_slug>]
    sprint team <join>
    sprint team <join> <team_slug>
    sprint teams
    sprint submission
    sprint submission save
    sprint submission <team_slug>
    sprint submissions


Options:
  -h --help                         Show this screen.
  -v --version                      Show version.

Help:
    >> sprint login                 # Login to HackerEarth Sprint
    >> sprint access djangothon     # Set cli to communicate to `djangothon`
    >> sprint register              # Register for `djangothon`
    >> sprint logout                # Logout of HackerEarth Sprint
"""
from docopt import docopt
from inspect import isclass, getmembers

from sprint_commands import login, logout, access, register
from sprint_commands import team
import sprint_commands

if __name__ == '__main__':
    options = docopt(__doc__, version='0.1')

    for key, value in options.iteritems():
        if value and hasattr(sprint_commands, key):
            module = getattr(sprint_commands, key)
            commands = getmembers(module, isclass)
            klass = None
            for name, command in commands:
                if getattr(command, 'namespace', '') == key:
                    klass = command

            if klass:
                klass = klass(options)
                klass.run()
