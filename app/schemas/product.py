from pydantic import BaseModel, Field, condecimal, conint


class ProductBase(BaseModel):
    name: str = Field(
        ..., min_length=1, description="El nombre del producto es obligatorio"
    )
    description: str
    price: condecimal(gt=0) = Field(
        ..., gt=0, description="El precio debe ser mayor que 0"
    )
    stock: conint(gt=0) = Field(..., ge=0, description="El stock no puede ser negativo")

    # @validator("name")
    # def name_must_not_be_empty(cls, v):
    #     if not v.strip():
    #         raise ValueError("El nombre del producto no puede estar vacío")
    #     return v


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
