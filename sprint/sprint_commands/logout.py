import os
from utils import log

from constants import CRED_FILE_PATH
from constants import BColors

from sprint_commands.base import BaseSprintCommand


class Logout(BaseSprintCommand):
    """
    sprint `logout` command
    """
    namespace = 'logout'

    def run(self):
        if os.path.exists(CRED_FILE_PATH):
            os.remove(CRED_FILE_PATH)
        msg = 'Successfully logged out of HackerEarth Sprint.{default_color}'
        msg_ctx = {'line_color': BColors.OKGREEN}
        log(msg, msg_ctx)
