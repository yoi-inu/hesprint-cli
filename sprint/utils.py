import os
import json
import requests
import shutil
from tabulate import tabulate

from constants import BColors
from constants import SLUG_FILE_PATH, CRED_FILE_PATH
from constants import SUBMISSION_BASE_META_FILE_PATH
from constants import SUBMISSION_META_FILE_NAME
from constants import SUBMISSION_FILES_FILE_NAME
from constants import HESPRINT_PATH
from constants import API_DOMAIN_ROOT
from constants import VERBOSE_COLOR_MAP
from constants import VerbosityLevel


def send_request(url, sprint_slug='', team_slug='', data={}, files={},
                 headers=""):
    url = API_DOMAIN_ROOT + url

    url = url.format(sprint_slug=sprint_slug, team_slug=team_slug)

    cred_data = {}
    cred_data = apply_auth_creds(cred_data)

    for key, value in cred_data.iteritems():
        data[key] = value

    data['files_data'] = files

    data = json.dumps(data)

    response = requests.post(url, data=data)

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
    if os.path.exists(HESPRINT_PATH):
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


def print_sprint_details(sprint_data):
    """
    Print sprint data in a tabular format.
    """
    headers = []
    table = []

    data_order = [
        ('Hackathon Name', sprint_data['title']),
        ('Description', sprint_data['short_description']),
        ('URL', sprint_data['url']),
        ('Start', sprint_data['start']),
        ('End', sprint_data['end']),
        ('Team Size', sprint_data['team_size']),
    ]

    for title, value in data_order:
        row = []
        data = '{color}%s{default_color}' % title
        data = data.format(
            color=VERBOSE_COLOR_MAP[VerbosityLevel.BOLD],
            default_color=VERBOSE_COLOR_MAP[VerbosityLevel.INFO])
        row.append(data)
        row.append(value)
        table.append(row)

    print tabulate(table, headers, tablefmt="grid")


def print_submission_details(submission_data):
    """
    Print submission data in a tabular format.
    """
    submission_title = 'PROJECT TITLE:  ' + submission_data['title']
    submission_description = submission_data['description']
    submission_tags = submission_data['tags']
    submission_theme = submission_data.get("theme", None)
    submission_presentation = submission_data["presentation"]
    submission_souce_code = submission_data['attachment']
    submission_source_url = submission_data['source_url']
    submission_video_link = submission_data['video_url']
    submission_instructions = submission_data['instruction']
    submission_demo_link = submission_data['demo_link']

    data_order = [
        ('Description', submission_description),
        ('Tags', submission_tags),
    ]

    if submission_theme is not None:
        data_order.append(
            ('Theme', submission_theme)
        )

    data_order.extend([
        ("Presentation", submission_presentation),
        ("Souce Code", submission_souce_code),
        ("Repository Link", submission_source_url),
        ("Demo Link", submission_demo_link),
        ("Video Link", submission_video_link),
        ("Instructions to Run", submission_instructions),
    ])

    print BColors.BOLD
    print submission_title
    print "=" * len(submission_title)
    print BColors.DEFAULT

    for subheading_name, subheading_value in data_order:
        if subheading_value:
            print BColors.WARNING + subheading_name + ":"
            print "-" * (len(subheading_name) + 1) + BColors.DEFAULT
            print subheading_value
            print


def get_submission_meta_file_path(sprint_slug):
    if not os.path.exists(SUBMISSION_BASE_META_FILE_PATH):
        log("Package Corrupt. Please reinstall.",
            msg_ctx={'line_color': BColors.FAIL})

    # Create sprint specific dir if it doesn't exists
    SPRINT_PATH = os.path.join(HESPRINT_PATH, sprint_slug)
    if not os.path.exists(SPRINT_PATH):
        os.mkdir(SPRINT_PATH)

    SUBMISSION_META_FILE_PATH = os.path.join(
        SPRINT_PATH,
        SUBMISSION_META_FILE_NAME)
    if not os.path.exists(SUBMISSION_META_FILE_PATH):
        shutil.copy(
            SUBMISSION_BASE_META_FILE_PATH,
            SUBMISSION_META_FILE_PATH)

    return SUBMISSION_META_FILE_PATH


def open_submission_meta_file(sprint_slug):
    SUBMISSION_META_FILE_PATH = get_submission_meta_file_path(sprint_slug)
    os.system("vi %s" % SUBMISSION_META_FILE_PATH)


def read_submission_meta_file(sprint_slug):
    SUBMISSION_META_FILE_PATH = get_submission_meta_file_path(sprint_slug)
    if not os.path.exists(SUBMISSION_META_FILE_PATH):
        open_submission_meta_file(sprint_slug)

    f = open(SUBMISSION_META_FILE_PATH, 'r')
    content = f.read()
    f.close()

    title_string = get_subheading_str("Project Title")
    tags_string = get_subheading_str("Tags")
    description_string = get_subheading_str("Project Description")
    demo_link_string = get_subheading_str("Demo Link")
    video_link_string = get_subheading_str("Video Link")
    repo_link_string = get_subheading_str("Repository Link")
    instructions_string = get_subheading_str("Instructions to Run")

    title = get_subheading_value(content, title_string, tags_string)
    tags = get_subheading_value(content, tags_string, description_string)
    description = get_subheading_value(
        content, description_string, demo_link_string)
    demo_link = get_subheading_value(
        content, demo_link_string, video_link_string)
    video_link = get_subheading_value(
        content, video_link_string, repo_link_string)
    repo_link = get_subheading_value(
        content, repo_link_string, instructions_string)
    instructions = get_subheading_value(content, instructions_string)

    return {
        'title': title,
        'tags': tags,
        'description': description,
        'demo_link': demo_link,
        'video_link': video_link,
        'repo_link': repo_link,
        'instructions': instructions,
    }


def get_subheading_str(subheading):
    subheading += ":"
    subheading_underline = '-' * len(subheading)

    return "%s\n%s" % (subheading, subheading_underline)


def get_subheading_value(content, subheading, next_subheading=None):
    start_index = content.index(subheading) + len(subheading)

    if next_subheading:
        end_index = content.index(next_subheading)
    else:
        end_index = len(content)

    value = content[start_index:end_index]
    value = value.strip("\n")

    return value


def get_submission_file_paths(sprint_slug):
    # Create sprint specific dir if it doesn't exists
    SPRINT_PATH = os.path.join(HESPRINT_PATH, sprint_slug)
    if not os.path.exists(SPRINT_PATH):
        os.mkdir(SPRINT_PATH)

    FILES_FILE_PATH = os.path.join(SPRINT_PATH, SUBMISSION_FILES_FILE_NAME)
    if not os.path.exists(FILES_FILE_PATH):
        os.system('touch %s' % FILES_FILE_PATH)

    return FILES_FILE_PATH


def save_submission_file(sprint_slug, data):
    FILES_FILE_PATH = get_submission_file_paths(sprint_slug)
    f = open(FILES_FILE_PATH, 'r')
    current_data = f.read()
    if current_data:
        current_data = json.loads(current_data)
    else:
        current_data = {}

    print data

    for key, value in data.iteritems():
        current_data[key] = value

    current_data = json.dumps(current_data)
    f.close()

    f = open(FILES_FILE_PATH, 'w')
    f.write(current_data)
    f.close()


def submission_file_values(sprint_slug):
    FILES_FILE_PATH = get_submission_file_paths(sprint_slug)

    f = open(FILES_FILE_PATH, 'r')
    current_data = f.read()
    if current_data:
        current_data = json.loads(current_data)
    else:
        current_data = {}

    files = {}
    for file_type, file_path in current_data.iteritems():
        files[file_type] = {
            'file_name': file_path.split('/')[-1],
            'content': open(file_path, 'rb').read(),
        }

    return files
