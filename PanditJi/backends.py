from django.contrib.auth.backends import BaseBackend
from .models import UserAccount, People, Pandit

class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        # Check against UserAccount
        user_account = UserAccount.objects.filter(email=username).first()
        if user_account.is_superuser==True:
            if user_account and user_account.check_password(password):
                return user_account

        # Check against People
        people = People.objects.filter(email=username).first()
        if user_account.is_people==True:
            if people and people.check_password(password):
                return people

        # Check against Pandit
        pandit = Pandit.objects.filter(email=username).first()
        if user_account.is_pandit==True:
            if pandit and pandit.check_password(password):
                return pandit

        return None

    def get_user(self, user_id):
        try:
            return UserAccount.objects.get(pk=user_id)
        except UserAccount.DoesNotExist:
            return None
