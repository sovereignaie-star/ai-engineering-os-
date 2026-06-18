class BaseAdapter:
    def __init__(self, config):
        self.config = config

    def execute_task(self, task):
        raise NotImplementedError
