class AuthBackend:
    def login(self, user):
        raise NotImplementedError

    def logout(self):
        raise NotImplementedError

    def get_current_user(self):
        raise NotImplementedError
