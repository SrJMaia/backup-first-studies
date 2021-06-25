class Error(Exception):
    """Base class for other exceptions"""
    pass


class OnlyOneParamater(Error):
    
    def __init__(self, only_one, message="only_one isn't in ['open','high','low','close']"):
        self.salary = only_one
        self.message = message
        super().__init__(self.message)