

from backend.app.api.v1.auth.repository import UserRepository
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from backend.app.core.security import create_access_token, hash_password, verify_password
from backend.app.models.user import User, UserCreate

class UserAlreadyExistsError(Exception):
    pass

class DatabaseError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register(self, user_create: UserCreate) -> User:
        if self.repository.get_by_email(user_create.email):
            raise UserAlreadyExistsError("Email ya registrado")

        user = User(
            hashed_password=hash_password(user_create.password),
            **user_create.model_dump(exclude={"password"})
        )

        try:
            return self.repository.create(user=user)
        except IntegrityError:
            raise UserAlreadyExistsError("Conflicto de integridad: email ya existe")
        except SQLAlchemyError:
            raise DatabaseError("Error interno al crear el usuario")
    
    def login(self, email: str, password: str) -> str:
        user = self.repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Credenciales invalidas")

        token = create_access_token(sub=str(user.id))
        return token