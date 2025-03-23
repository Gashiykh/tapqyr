from pydantic import BaseModel


class CategoryBase(BaseModel):
    pass


class CategoryCreate(BaseModel):
    name: str