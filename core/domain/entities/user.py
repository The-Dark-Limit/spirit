from core.value_objects.email import Email


class User:
    def __init__(self, email: Email):
        self.email = email
