from django.contrib.auth import login, authenticate
from django.http import HttpRequest
from users.models import User
from django.core.exceptions import ValidationError


class UserService:
    """Manage business logic for users domain."""

    model = User

    @classmethod
    def register_user(cls, email: str, password: str, first_name=None, last_name=None):
        """Create a new user in the database."""

        user = cls.model.objects.create_user(email=email, password=password)
        user.profile.first_name = first_name
        user.profile.last_name = last_name
        user.profile.save()

        return user

    @classmethod
    def login_user(cls, request: HttpRequest, user: User):
        """Creates a new user session."""
        request.user = None

        return login(request, user)

    @classmethod
    def authenticate_user(
        cls, request: HttpRequest, username_or_email: str, password: str
    ) -> User:
        """Verify user credentials, return user if valid."""

        if "@" in username_or_email:
            user = cls.model.objects.get(profile__email=username_or_email)
        else:
            user = cls.model.objects.get(username=username_or_email)

        auth_user = authenticate(request, username=user.username, password=password)

        if auth_user is None:
            raise ValidationError("Invalid user credentials.")

        return user
