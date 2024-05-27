from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from sqlalchemy.future import select
from app.db import User, async_session_maker
from admin.service import get_or_create_access_token, get_access_token, delete_access_token
from app.config import context


class AdminAuth(AuthenticationBackend):
    session = async_session_maker()

    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        result = await self.session.execute(select(User).where(User.email == email))
        user = result.scalar()
        if not user:
            return False
        valid = context.verify(password, user.hashed_password)
        if not valid:
            return False
        else:
            access_token = await get_or_create_access_token(self.session, user)
            request.session.update({"token": access_token})
            return user.is_superuser


    async def logout(self, request: Request) -> bool:
        token = request.session.get("token")
        request.session.clear()
        await delete_access_token(self.session, token)
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        return await get_access_token(self.session, token)
    
authentication_backend = AdminAuth(secret_key='SECRET')
