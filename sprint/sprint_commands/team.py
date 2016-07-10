from utils import log, send_request
from utils import get_slug


from constants import BColors

from sprint_commands.base import BaseSprintCommand


class Team(BaseSprintCommand):
    """
    sprint `team` command
    """
    namespace = 'team'

    def run(self):
        sprint_slug = get_slug()
        team_slug = self.options.get('<team_slug>', None)

        if team_slug:
            # show team info
            url = "{sprint_slug}/team/{team_slug}/"
            response = send_request(url, sprint_slug=sprint_slug,
                                    team_slug=team_slug)
        else:
            url = "{sprint_slug}/team/"
            response = send_request(url, sprint_slug=sprint_slug)
            # Show user team info

        if not response:
            return

        print response.json()

        data = response.json()
        message = data.get('message', '')
        log(message, msg_ctx={})
