import os
import json
import requests
from tabulate import tabulate

from constants import BColors
from constants import SLUG_FILE_PATH, CRED_FILE_PATH
from constants import SPRINT_PATH
from constants import API_DOMAIN_ROOT
from constants import VERBOSE_COLOR_MAP
from constants import VerbosityLevel


def send_request(url, sprint_slug=None, team_slug=None):
    url = API_DOMAIN_ROOT + url

    if sprint_slug:
        url = url.format(sprint_slug=sprint_slug)
    if team_slug:
        url = url.format(team_slug=team_slug)

    data = {}
    data = apply_auth_creds(data)
    response = requests.post(url, data=json.dumps(data))

    if response.status_code == 200:
        return response
    else:
        r_json = response.json()
        msg = "ERROR: %s\n" % r_json['emessage'][0]
        msg_ctx = {'line_color': VERBOSE_COLOR_MAP[VerbosityLevel.ERROR]}
        log(msg, msg_ctx)

        return


def log(msg, msg_ctx={}, line_break=True):
    msg_ctx.update({
        'default_color': BColors.DEFAULT
    })
    if 'line_color' in msg_ctx:
        msg = '{line_color}%s{default_color}' % msg

    if line_break:
        print msg.format(**msg_ctx)
    else:
        print msg.format(**msg_ctx),


def apply_auth_creds(ctx):
    if not os.path.exists(CRED_FILE_PATH):
        msg = "Login to send this request:"
        msg_ctx = {'line_color': BColors.BOLD}
        log(msg, msg_ctx)
        force_login()
    else:
        with open(CRED_FILE_PATH, 'r') as fp:
            data = json.load(fp)
        ctx.update(data)
        return ctx


def save_slug(sprint_slug):
    if os.path.exists(SPRINT_PATH):
        data = {'sprint_slug': sprint_slug}
        with open(SLUG_FILE_PATH, 'wb') as fp:
            json.dump(data, fp)
    else:
        msg = "Please login first"
        msg_ctx = {'line_color': BColors.BOLD}
        force_login()
        log(msg, msg_ctx)


def force_login():
    from sprint_commands.base import BaseSprintCommand
    from sprint_commands.login import Login
    Login(BaseSprintCommand).run()


def get_slug():
    """
    Return sprint_slug by reading it from SLUG_FILE_PATH
    """
    if os.path.exists(SLUG_FILE_PATH):
        with open(SLUG_FILE_PATH, 'r') as fp:
            data = json.load(fp)
        sprint_slug = data.get("sprint_slug", "")
        return sprint_slug

    msg = ("{color}Please access the hackathon first.{default_color}"
           "\n Help:\n>> sprint access <sprint_slug>")
    msg_ctx = {'color': BColors.BOLD}
    log(msg, msg_ctx)


def print_sprint_details(json_data):
    """
    Print sprint data in a tabular format.
    """
    headers = []
    table = []

    row = []
    data = '{color} Hackathon Title {default_color}'
    data = data.format(
        color=VERBOSE_COLOR_MAP[VerbosityLevel.BOLD],
        default_color=VERBOSE_COLOR_MAP[VerbosityLevel.INFO])
    row.append(data)
    row.append(json_data['title'])
    table.append(row)

    row = []
    data = '{color} Short Description {default_color}'
    data = data.format(
        color=VERBOSE_COLOR_MAP[VerbosityLevel.BOLD],
        default_color=VERBOSE_COLOR_MAP[VerbosityLevel.INFO]
    )
    row.append(data)
    row.append(json_data['short_description'])
    table.append(row)

    row = []
    data = '{color} URL {default_color}'
    data = data.format(
        color=VERBOSE_COLOR_MAP[VerbosityLevel.BOLD],
        default_color=VERBOSE_COLOR_MAP[VerbosityLevel.INFO]
    )
    row.append(data)
    row.append(json_data['url'])
    table.append(row)

    row = []
    data = '{color} Start {default_color}'
    data = data.format(
        color=VERBOSE_COLOR_MAP[VerbosityLevel.BOLD],
        default_color=VERBOSE_COLOR_MAP[VerbosityLevel.INFO]
    )
    row.append(data)
    row.append(json_data['start'])
    table.append(row)

    row = []
    data = '{color} End {default_color}'
    data = data.format(
        color=VERBOSE_COLOR_MAP[VerbosityLevel.BOLD],
        default_color=VERBOSE_COLOR_MAP[VerbosityLevel.INFO]
    )
    row.append(data)
    row.append(json_data['end'])
    table.append(row)

    row = []
    data = '{color} Team Size {default_color}'
    data = data.format(
        color=VERBOSE_COLOR_MAP[VerbosityLevel.BOLD],
        default_color=VERBOSE_COLOR_MAP[VerbosityLevel.INFO]
    )
    row.append(data)
    row.append(json_data['team_size'])
    table.append(row)

    print tabulate(table, headers, tablefmt="grid")
