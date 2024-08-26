from datetime import datetime, timezone

from sqlalchemy import MetaData, Column, Integer, String, TIMESTAMP, ForeignKey, JSON
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def aware_utcnow():
    return datetime.now(timezone.utc)


def naive_utcnow():
    return aware_utcnow().replace(tzinfo=None)


metadata = MetaData()

# roles = Table(
#     "roles",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String, nullable=False),
#     Column("permissions", JSON),
# )
#
# users = Table(
#     "users",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("email", String, nullable=False),
#     Column("username", String, nullable=False),
#     Column("password", String, nullable=False),
#     Column("registered_at", TIMESTAMP, default=naive_utcnow()),
#     Column("role_id", Integer, ForeignKey("roles.id")),
# )


class roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    permissions = Column(JSON)


class users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=naive_utcnow())
    role_id = Column(Integer, ForeignKey("roles.id"))
