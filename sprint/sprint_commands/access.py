
from utils import log, send_request
from utils import print_sprint_details

from constants import BColors


from sprint_commands.base import BaseSprintCommand


class Access(BaseSprintCommand):
    """
    sprint `access` command
    """
    namespace = 'access'

    def run(self):
        sprint_slug = self.options.get('<sprint_slug>', None)

        if not sprint_slug:
            log("Enter the hackathon slug to access the hackathon.",
                {'line_color': BColors.WARNING})
            return

        url = "{sprint_slug}/access/"
        response = send_request(url, sprint_slug=sprint_slug)

        if not response:
            return

        msg = ("Access set to {sprint_slug}.\n")
        msg_ctx = {
            'line_color': BColors.OKBLUE,
            'sprint_slug': sprint_slug
        }
        log(msg, msg_ctx)

        print_sprint_details(response.json())
