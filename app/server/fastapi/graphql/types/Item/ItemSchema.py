from typing import Optional, List

import strawberry
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from strawberry.types import Info

from app.server.database.database import async_session_maker
from app.server.database.models import Item
from app.server.fastapi.graphql.types.User.UserSchema import UserSchema


@strawberry.type
class ItemSchema:
    id: int
    
    name: str
    description: Optional[str]
    
    user_id: int
    
    @strawberry.field
    async def user(self, info: Info) -> UserSchema:
        return await info.context['user_loader'].load(self.user_id)

    @staticmethod
    def from_db_instance(db_instance: Item) -> "ItemSchema":
        return ItemSchema(
            id=db_instance.id,
            name=db_instance.name,
            description=db_instance.description,
            user_id=db_instance.user
        )


async def get_all_items(user_id: Optional[int] = None) -> List[ItemSchema]:
    async with async_session_maker() as session:
        statement = select(Item).where(user_id is None or Item.user == user_id)
        db_items = (await session.execute(statement)).scalars().all()

        items = [ItemSchema.from_db_instance(db_item) for db_item in db_items]

        return items


async def create_item(name: str, description: Optional[str], user_id: int) -> Optional[ItemSchema]:
    async with async_session_maker() as session:
        try:
            db_item = Item(
                name=name,
                description=description,
                user=user_id
            )
            session.add(db_item)
            await session.commit()
        except IntegrityError:
            return None

        item = ItemSchema.from_db_instance(db_item)

        return item


async def update_item(id: int, name: str, description: Optional[str], user_id: int) -> Optional[ItemSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(Item).where(Item.id == id and Item.user == user_id)
            db_item = (await session.execute(statement)).scalars().one()
            db_item.name = name
            db_item.description = description
            db_item.user = user_id
            await session.commit()
        except (NoResultFound, IntegrityError):
            return None

        item = ItemSchema.from_db_instance(db_item)

        return item


async def delete_item(id: int, user_id: int) -> Optional[ItemSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(Item).where(Item.id == id and Item.user == user_id)
            db_item = (await session.execute(statement)).scalars().one()
            await session.delete(db_item)
            await session.commit()
        except NoResultFound:
            return None

        item = ItemSchema.from_db_instance(db_item)

        return item
