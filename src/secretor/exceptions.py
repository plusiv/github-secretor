class NoTokenSet(Exception):
    def __str__(self):
        return 'No Github token has been set.'

class InvalidToken(Exception):
    def __str__(self):
        return 'This is an invalid Github Access Token.'
