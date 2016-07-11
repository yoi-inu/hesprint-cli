import requests
import getpass
import os
import json
from utils import log, send_request

from constants import API_DOMAIN_ROOT
from constants import CONFIG_PATH
from constants import HESPRINT_PATH
from constants import CRED_FILE_PATH
from constants import BColors

from sprint_commands.base import BaseSprintCommand


class Login(BaseSprintCommand):
    """
    sprint `login` command
    """
    namespace = 'login'

    def run(self):
        url = API_DOMAIN_ROOT + 'login/'
        email = raw_input('Email: ')
        password = getpass.getpass()
        data = {
            'email': email,
            'password': password,
        }
        response = requests.post(url, data=data)

        if not response.status_code == 200:
            msg = 'Invalid email/password. Please check your credentials.'
            msg_ctx = {'line_color': BColors.FAIL}
            log(msg, msg_ctx)
            return

        credentials = response.json()
        if not os.path.exists(CONFIG_PATH):
            os.makedirs(CONFIG_PATH)

        if not os.path.exists(HESPRINT_PATH):
            os.makedirs(HESPRINT_PATH)
        with open(CRED_FILE_PATH, 'wb') as temp_file:
            json.dump(credentials, temp_file)
        msg = 'Successfully logged in to HackerEarth Sprint.'
        msg_ctx = {'line_color': BColors.OKGREEN}
        log(msg, msg_ctx)
