from typing import Optional, List

import strawberry
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from strawberry.types import Info

from app.server.database.database import async_session_maker
from app.server.database.models import RequiredEquipment
from app.server.fastapi.graphql.types.User.UserSchema import UserSchema
from app.server.fastapi.graphql.types.Item.ItemSchema import ItemSchema
from app.server.fastapi.graphql.types.Discipline.DisciplineSchema import DisciplineSchema


@strawberry.type
class RequiredEquipmentSchema:
    id: int
    
    amount: int
    
    user_id: int
    item_id: int
    discipline_id: int
    
    @strawberry.field
    async def user(self, info: Info) -> UserSchema:
        return await info.context['user_loader'].load(self.user_id)

    @strawberry.field
    async def item(self, info: Info) -> ItemSchema:
        return await info.context['item_loader'].load(self.item_id)

    @strawberry.field
    async def discipline(self, info: Info) -> DisciplineSchema:
        return await info.context['discipline_loader'].load(self.discipline_id)

    @staticmethod
    def from_db_instance(db_instance: RequiredEquipment) -> "RequiredEquipmentSchema":
        return RequiredEquipmentSchema(
            id=db_instance.id,
            amount=db_instance.amount,
            user_id=db_instance.user,
            item_id=db_instance.item,
            discipline_id=db_instance.discipline
        )


async def get_all_required_equipments(user_id: Optional[int] = None) -> List[RequiredEquipmentSchema]:
    async with async_session_maker() as session:
        statement = select(RequiredEquipment).where(user_id is None or RequiredEquipment.user == user_id)
        db_required_equipments = (await session.execute(statement)).scalars().all()

        required_equipments = [RequiredEquipmentSchema.from_db_instance(db_required_equipment) for db_required_equipment in db_required_equipments]

        return required_equipments


async def create_required_equipment(amount: int, user_id: int, item_id: int, discipline_id: int) -> Optional[RequiredEquipmentSchema]:
    async with async_session_maker() as session:
        try:
            db_required_equipment = RequiredEquipment(
                amount=amount,
                user=user_id,
                item=item_id,
                discipline=discipline_id
            )
            session.add(db_required_equipment)
            await session.commit()
        except IntegrityError:
            return None

        required_equipment = RequiredEquipmentSchema.from_db_instance(db_required_equipment)

        return required_equipment


async def update_required_equipment(id: int, amount: int, user_id: int, item_id: int, discipline_id: int) -> Optional[RequiredEquipmentSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(RequiredEquipment).where(RequiredEquipment.id == id and RequiredEquipment.user == user_id)
            db_required_equipment = (await session.execute(statement)).scalars().one()
            db_required_equipment.amount = amount
            db_required_equipment.user = user_id
            db_required_equipment.item = item_id
            db_required_equipment.discipline = discipline_id
            await session.commit()
        except (NoResultFound, IntegrityError):
            return None

        required_equipment = RequiredEquipmentSchema.from_db_instance(db_required_equipment)

        return required_equipment


async def delete_required_equipment(id: int, user_id: int) -> Optional[RequiredEquipmentSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(RequiredEquipment).where(RequiredEquipment.id == id and RequiredEquipment.user == user_id)
            db_required_equipment = (await session.execute(statement)).scalars().one()
            await session.delete(db_required_equipment)
            await session.commit()
        except NoResultFound:
            return None

        required_equipment = RequiredEquipmentSchema.from_db_instance(db_required_equipment)

        return required_equipment
