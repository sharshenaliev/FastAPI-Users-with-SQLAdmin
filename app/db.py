from typing import AsyncGenerator
from sqlalchemy import Column, Integer, ForeignKey
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTable
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from app.config import context, ADMIN_PASSWORD, ADMIN_USERNAME


DATABASE_URL = "sqlite+aiosqlite:///./test.db"
Base: DeclarativeMeta = declarative_base()


class User(SQLAlchemyBaseUserTable, Base):
    id: int = Column(Integer, primary_key=True, autoincrement=True) 

class AccessToken(SQLAlchemyBaseAccessTokenTable, Base):
    user_id: int = Column(ForeignKey('user.id'), primary_key=True)

engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def create_superuser():
     async with async_session_maker() as session:
        result = await session.execute(select(User).where(User.email==ADMIN_USERNAME))
        exists = bool(result.scalar())
        if not exists:
            superuser = User(email=ADMIN_USERNAME, is_superuser=True, is_verified=True, 
                         hashed_password=context.hash(ADMIN_PASSWORD))
            session.add(superuser)
            await session.commit()
