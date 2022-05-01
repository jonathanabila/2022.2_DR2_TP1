from enum import Enum
from typing import Optional

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base

from constants import SQL_ALCHEMY_URL

engine = create_engine(SQL_ALCHEMY_URL, future=True)
session = Session(engine)

declarative_base = declarative_base()


class ContainerType(Enum):
    BASIC = "BASIC"
    REFRIGERATED = "REFRIGERATED"
    TWO_FLOOR = "TWO_FLOOR"
    HALF = "HALF"


class Container(declarative_base):
    __tablename__ = "containers"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    type = sqlalchemy.Column(sqlalchemy.Enum(ContainerType))
    volume = sqlalchemy.Column(sqlalchemy.Integer)

    def is_refrigerated(self):
        return self.type == ContainerType.REFRIGERATED


class ContainerRepository:
    type: ContainerType

    def __init__(self, app_session: Optional[sqlalchemy.orm.scoped_session] = None):
        self.app_session = app_session or session

    def get_by_id(self, container_id: int):
        return self.app_session.query(Container).filter_by(id=container_id).first()

    def add(self, container: Container):
        self.app_session.add(container)
        self.app_session.commit()

    def get_all(self):
        return self.app_session.query(Container).all()

    def delete_by_id(self, container_id: int):
        self.app_session.query(Container).filter_by(id=container_id).delete()
        self.app_session.commit()

    def update(self, container: Container):
        self.app_session.query(Container).filter_by(id=container.id).update(
            container.__dict__
        )
        self.app_session.commit()

    def get_by_type(self):
        return self.app_session.query(Container).filter_by(type=self.type).all()


class BasicContainerRepository(ContainerRepository):
    type = ContainerType.BASIC


class RefrigeratedContainerRepository(ContainerRepository):
    type = ContainerType.REFRIGERATED


class TwoFloorContainerRepository(ContainerRepository):
    type = ContainerType.TWO_FLOOR


if __name__ == "__main__":
    print("Upgrading database...")
    import os

    os.system("alembic upgrade head")
    print("Database upgraded.")

    # Add containers
    BasicContainerRepository().add(Container(type=ContainerType.BASIC, volume=100))
    RefrigeratedContainerRepository().add(
        Container(type=ContainerType.REFRIGERATED, volume=200)
    )
    TwoFloorContainerRepository().add(
        Container(type=ContainerType.TWO_FLOOR, volume=300)
    )

    # Get Refrigerated containers
    containers = RefrigeratedContainerRepository().get_by_type()

    for container in containers:
        print(container.__dict__, container.is_refrigerated())
