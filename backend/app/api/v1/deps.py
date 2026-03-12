
from fastapi.security import OAuth2PasswordBearer

ouath2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")