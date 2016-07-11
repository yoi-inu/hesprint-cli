import os

from utils import log, send_request
from utils import get_slug, print_submission_details
from utils import open_submission_meta_file, read_submission_meta_file
from utils import save_submission_file, get_submission_file_paths
from utils import get_submission_meta_file_path, submission_file_values

from constants import BColors

from sprint_commands.base import BaseSprintCommand


class Submission(BaseSprintCommand):
    """
    sprint `submission` command
    """
    namespace = 'submission'

    def run(self):
        self.sprint_slug = get_slug()

        submission_add = self.options.get("add", None)
        submission_show = self.options.get("show", None)
        submission_push = self.options.get("push", None)

        if submission_add:
            return self.add()

        if submission_show:
            return self.show()

        if submission_push:
            return self.push()

    def show(self):
        team_slug = self.options.get('<team_slug>', None)
        if team_slug:
            # show team submission info
            url = "{sprint_slug}/submission/{team_slug}/"
            response = send_request(url, sprint_slug=self.sprint_slug,
                                    team_slug=team_slug)
        else:
            # Show user team submission info
            url = "{sprint_slug}/submission/"
            response = send_request(url, sprint_slug=self.sprint_slug)

        if not response:
            return

        submission_data = response.json()
        print_submission_details(submission_data)

    def add(self):
        submission_add_theme = self.options.get("theme", None)
        submission_add_source = self.options.get("source", None)
        submission_add_presentation = self.options.get("presentation", None)

        if submission_add_theme:
            return self.add_theme()

        if submission_add_source:
            return self.add_source()

        if submission_add_presentation:
            return self.add_presentation()

        open_submission_meta_file(self.sprint_slug)
        log("Submission updated successfully. Push to sync with server",
            {'line_color': BColors.OKGREEN})

    def add_theme(self):
        pass

    def add_source(self):
        file_path = self.options.get('<file_path>', None)
        file_path = os.path.abspath(file_path)

        file_data = {
            'source': file_path,
        }
        save_submission_file(self.sprint_slug, file_data)

    def add_presentation(self):
        file_path = self.options.get('<file_path>', None)
        file_path = os.path.abspath(file_path)

        file_data = {
            'presentation': file_path,
        }
        save_submission_file(self.sprint_slug, file_data)

    def push(self):
        submission_data = read_submission_meta_file(self.sprint_slug)
        files_data = submission_file_values(self.sprint_slug)

        url = "{sprint_slug}/submission/push/"
        response = send_request(
            url, sprint_slug=self.sprint_slug,
            data=submission_data, files=files_data)

        if not response:
            return

        msg = (response.json()['message'])
        msg_ctx = {
            'line_color': BColors.OKGREEN,
        }
        log(msg, msg_ctx)
