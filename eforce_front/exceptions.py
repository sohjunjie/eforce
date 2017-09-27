class AuthenticationError(Exception):
    def __init__(self, error):
        # super(AuthenticationError, self).__init__(message)
        self.error = error


class UpdateCrisisCMOError(Exception):
    def __init__(self, error):
        # super(AuthenticationError, self).__init__(message)
        self.error = error


class UpdateCrisisEFHQError(Exception):
    def __init__(self, error):
        # super(AuthenticationError, self).__init__(message)
        self.error = error
