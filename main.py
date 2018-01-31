#! /usr/bin/env python
# -*- coding: utf-8 -*-

# ============================================= #
#  ----------------- Modules -----------------  #
# ============================================= #

import argparse

# ============================================= #
#  -------------- From Modules ---------------  #
# ============================================= #

from core.information import Info
from core.jsonreader import ReadJSON


# ============================================= #
#  -------------- Release Info ---------------  #
# ============================================= #
class release:
    __author__ = "Kike Puma"
    __copyright__ = "Copyright 2018, CosasDePuma"
    __credits__ = ["KikePuma", "CosasDePuma"]
    __license__ = "MIT"
    __version__ = "1.0a"
    __maintainer__ = "KikePuma"
    __email__ = "kikefontanlorenzo@gmail.com"
    __status__ = "In development"


# ============================================= #
#  ------------------ Colors -----------------  #
# ============================================= #
class color:
    BOLD = '\033[1m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


# ============================================= #
#  --------------- Arguments -----------------  #
# ============================================= #

# ----------
#  Version and commands
# ----------------
parser = argparse.ArgumentParser(version=release.__version__)
subparser = parser.add_subparsers(dest="cmd")

# ----------
#  Config commands
# ----------------
for cmd in ["install", "search", "uninstall"]:
    subsubparser = subparser.add_parser(cmd)
    subsubparser.add_argument('repository', type=str)
    # ----------
    #  Customize (un)install command
    # ----------------
    if "install" in cmd:
        subsubparser.add_argument(
            '-q',
            '--quiet',
            '--silent',
            help="Do not print info messages",
            action="store_true")
        subsubparser.add_argument(
            '-y', '--yes', help="Accept all dialogs", action="store_true")

# ----------
#  Get arguments
# ----------------
args = parser.parse_args()


# ============================================= #
#  ------------------ Main -------------------  #
# ============================================= #
class Main:
    database_name = "octopus_db.json"

    # ----------
    #  Initial Functions
    # ----------------
    def __init__(self):
        self.info = Info()
        self.database_path = self.info.get_filepath(self.database_name)
        self.reader = ReadJSON(self.database_path)
        self.database = self.reader.read()
        if self.database is None:
            raise IOError('Database not found')

    # ----------
    #  Configure Installers
    # ----------------
    def configure(self):
        # ----------
        #  Check OS
        # ----------------
        if self.info.get_os() == "Linux":
            self.distro = self.info.get_distro()
            self.installation_path = "/opt/peral_tools"
            # ----------
            #  Configure installer
            # ----------------
            if args.cmd == "install":
                from core.install.linux import LinuxInstaller
                self.installer = LinuxInstaller(
                    self.database, self.installation_path, self.info)
            # ----------
            #  Configure uninstaller
            # ----------------
            elif args.cmd == "uninstall":
                from core.uninstall.linux import LinuxUninstaller
                self.installer = LinuxUninstaller(
                    self.database, self.installation_path, self.info)

    # ----------
    #  Search Function
    # ----------------

        def search(self, __repository):
            # ----------
            #  Variables
            # ----------------
            found = False
            return_repositoy = None
            # ----------
            #  Find Repository
            # ----------------
            for repository in self.database['repos']:
                if not found and __repository.lower(
                ) == repository['name'].lower():
                    return_repositoy = repository
            return return_repositoy


# ============================================= #
#  ------------ Main Conditional -------------  #
# ============================================= #

if __name__ == '__main__':
    # ----------
    #  Handle exceptions
    # ----------------
    try:
        main = Main()
        # ----------
        #  Install repository
        # ----------------
        if args.cmd == "install":
            main.configure()
            # ----------
            #  Search the repository
            # ----------------
            repository = self.search(__reponame)
            if repository is not None:
                # ----------
                #  Install the repository
                # ----------------
                if args.cmd == "install":
                    self.installer.install(repository)
                # ----------
                #  Uninstall the repository
                # ----------------
                elif args.cmd == "uninstall":
                    self.installer.uninstall(repository)
            else:
                # ----------
                #  Handle errors
                # ----------------
                print("{}[!] Repository {} not found in the DB{}".format(
                    color.FAIL, __reponame, color.ENDC))
            main.install(args.repository)
    # ----------
    #  Custom exceptions
    # ----------------
    except (IOError, SystemError, ImportError) as custom_exception:
        print("{}{}[!] {}{}".format(color.BOLD, color.FAIL,
                                    custom_exception[0], color.ENDC))
