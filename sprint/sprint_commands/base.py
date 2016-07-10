class BaseSprintCommand(object):
    """
    Base sprint command.
    """

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

    def run(self):
        raise NotImplementedError()
