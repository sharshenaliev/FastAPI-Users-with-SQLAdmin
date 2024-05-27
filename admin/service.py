from secrets import token_hex
from datetime import datetime
from sqlalchemy.future import select
from app.db import AccessToken


async def get_or_create_access_token(session, user):
    result = await session.execute(select(AccessToken).where(AccessToken.user_id == user.id))
    query = result.scalar()
    if not query:
        query = AccessToken(token=token_hex(43), created_at=datetime.now(), user_id=user.id)
        session.add(query)
        await session.commit()
    return query.token

async def get_access_token(session, token):
    result = await session.execute(select(AccessToken).where(AccessToken.token == token))
    access_token = result.scalar()
    if access_token:
        return True
    else:
        return False

async def delete_access_token(session, token):
    result = await session.execute(select(AccessToken).where(AccessToken.token == token))
    access_token = result.scalar()
    await session.delete(access_token)
    await session.commit()
    return True
