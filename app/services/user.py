from app.repositories.user import UserRepository
from app.schemas.user import UserResponse

class UserService:
    def __init__(self, db):
        self.repo = UserRepository(db)

    def create_user(self, user_data):
        return self.repo.create_user(user_data)

    def get_user(self, user_id: int):
        return self.repo.get_user(user_id)