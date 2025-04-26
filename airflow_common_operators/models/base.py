from pydantic import BaseModel as PydanticBaseModel

__all__ = ("BaseModel",)


class BaseModel(PydanticBaseModel):
    @property
    def params(self):
        return self.model_dump(exclude_unset=False)
