from users.application.services.user import UserService
from infrastructure.db.repositories.user import UserRepository


def get_user_service():
    return UserService(user_repository=UserRepository())