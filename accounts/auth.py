from django.contrib.auth import get_user_model

class EmailAuthBackend(object):
    # authenticate using email address
    def authenticate(self, request, username=None, password=None):
        try:
            User = get_user_model()
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None
        
    def get_user(self, user_id):
        try:
            User = get_user_model()
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
            