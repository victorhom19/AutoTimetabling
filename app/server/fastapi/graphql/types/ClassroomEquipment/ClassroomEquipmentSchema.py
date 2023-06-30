from typing import Optional, List

import strawberry
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from strawberry.types import Info

from app.server.database.database import async_session_maker
from app.server.database.models import ClassroomEquipment
from app.server.fastapi.graphql.types.User.UserSchema import UserSchema
from app.server.fastapi.graphql.types.Item.ItemSchema import ItemSchema



@strawberry.type
class ClassroomEquipmentSchema:
    id: int
    
    amount: int
    
    user_id: int
    item_id: int
    classroom_id: int
    
    @strawberry.field
    async def user(self, info: Info) -> UserSchema:
        return await info.context['user_loader'].load(self.user_id)

    @strawberry.field
    async def item(self, info: Info) -> ItemSchema:
        return await info.context['item_loader'].load(self.item_id)


    @staticmethod
    def from_db_instance(db_instance: ClassroomEquipment) -> "ClassroomEquipmentSchema":
        return ClassroomEquipmentSchema(
            id=db_instance.id,
            amount=db_instance.amount,
            user_id=db_instance.user,
            item_id=db_instance.item,
            classroom_id=db_instance.classroom
        )


async def get_all_classroom_equipments(user_id: Optional[int] = None) -> List[ClassroomEquipmentSchema]:
    async with async_session_maker() as session:
        statement = select(ClassroomEquipment).where(user_id is None or ClassroomEquipment.user == user_id)
        db_classroom_equipments = (await session.execute(statement)).scalars().all()

        classroom_equipments = [ClassroomEquipmentSchema.from_db_instance(db_classroom_equipment) for db_classroom_equipment in db_classroom_equipments]

        return classroom_equipments


async def create_classroom_equipment(amount: int, user_id: int, item_id: int, classroom_id: int) -> Optional[ClassroomEquipmentSchema]:
    async with async_session_maker() as session:
        try:
            db_classroom_equipment = ClassroomEquipment(
                amount=amount,
                user=user_id,
                item=item_id,
                classroom=classroom_id
            )
            session.add(db_classroom_equipment)
            await session.commit()
        except IntegrityError:
            return None

        classroom_equipment = ClassroomEquipmentSchema.from_db_instance(db_classroom_equipment)

        return classroom_equipment


async def update_classroom_equipment(id: int, amount: int, user_id: int, item_id: int, classroom_id: int) -> Optional[ClassroomEquipmentSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(ClassroomEquipment).where(ClassroomEquipment.id == id and ClassroomEquipment.user == user_id)
            db_classroom_equipment = (await session.execute(statement)).scalars().one()
            db_classroom_equipment.amount = amount
            db_classroom_equipment.user = user_id
            db_classroom_equipment.item = item_id
            db_classroom_equipment.classroom = classroom_id
            await session.commit()
        except (NoResultFound, IntegrityError):
            return None

        classroom_equipment = ClassroomEquipmentSchema.from_db_instance(db_classroom_equipment)

        return classroom_equipment


async def delete_classroom_equipment(id: int, user_id: int) -> Optional[ClassroomEquipmentSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(ClassroomEquipment).where(ClassroomEquipment.id == id and ClassroomEquipment.user == user_id)
            db_classroom_equipment = (await session.execute(statement)).scalars().one()
            await session.delete(db_classroom_equipment)
            await session.commit()
        except NoResultFound:
            return None

        classroom_equipment = ClassroomEquipmentSchema.from_db_instance(db_classroom_equipment)

        return classroom_equipment
