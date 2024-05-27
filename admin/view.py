from sqladmin import ModelView
from sqladmin._queries import Query
from starlette.requests import Request
from typing import Any
from app.db import User
from app.config import context


class UserAdmin(ModelView, model=User):
    column_searchable_list = [User.email]
    column_details_exclude_list = [User.hashed_password]
    form_args = dict(hashed_password=dict(label="Password", render_kw=dict(type="password"))) 

    async def update_model(self, request: Request, pk: str, data: dict) -> Any:
        if not context.identify(data['hashed_password']):
            password = context.hash(data['hashed_password'])
            data['hashed_password'] = password
        return await Query(self).update(pk, data, request)

    async def insert_model(self, request: Request, data: dict) -> Any:
        password = context.hash(data['hashed_password'])
        data['hashed_password'] = password
        return await Query(self).insert(data, request)
