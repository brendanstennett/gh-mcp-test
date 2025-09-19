from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeVar, Protocol

T = TypeVar('T')

class ModelProtocol(Protocol):
    """Protocol for models that support model_dump method"""
    def model_dump(self, *, exclude_unset: bool = False, exclude: set[str] | None = None) -> dict[str, object]:
        ...

class BaseRepository:
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def update_model(self, existing_model: T, update_data_model: ModelProtocol, exclude: set[str]) -> T:
        """Update an existing model with data from another model"""
        update_data = update_data_model.model_dump(exclude_unset=True, exclude=exclude)
        for field, value in update_data.items():
            setattr(existing_model, field, value)

        await self.session.commit()
        await self.session.refresh(existing_model)
        return existing_model
