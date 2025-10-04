from social.models import User

class PhoneAuthBackend:
    def authenticate(self, request, username=None, password=None):
        """
        Authenticate a user based on phone number and password.
        """
        try:
            user = User.objects.get(phone_number=username)
            if user.check_password(password):
                return user
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
