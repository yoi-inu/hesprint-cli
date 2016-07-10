from utils import log, send_request
from utils import get_slug


from constants import BColors

from sprint_commands.base import BaseSprintCommand


class Regsiter(BaseSprintCommand):
    """
    sprint `register` command
    """
    namespace = 'register'

    def run(self):
        sprint_slug = self.options.get('<sprint_slug>', None)

        if not sprint_slug:
            sprint_slug = get_slug()
            if sprint_slug:
                log("Using sprint slug %s to register." % sprint_slug)
            else:
                log("Enter the sprint slug to access the hackathon.",
                    {'line_color': BColors.WARNING})
                return

        url = "{sprint_slug}/register/"
        response = send_request(url, sprint_slug=sprint_slug)
        if not response:
            return

        data = response.json()
        message = data.get('message', '')
        log(message, msg_ctx={})
