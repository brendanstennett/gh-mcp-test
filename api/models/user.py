from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()  # pyright: ignore[reportAny]

class User(SQLAlchemyBaseUserTableUUID, Base):  # pyright: ignore[reportUntypedBaseClass]
    pass
