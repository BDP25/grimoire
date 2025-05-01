class AuthenticationError(Exception):
    """
    Custom exception for authentication errors.
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
