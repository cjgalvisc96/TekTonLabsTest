import uuid

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator

from src.apps.inventary.api.dependecy_injection import InventaryContainer
from src.contexts.inventary.products.application import (
    ProductCreator,
    ProductCreatorRequestDTO,
)
from src.contexts.shared.domain import DomainConstants

router = APIRouter(prefix="/products", tags=["products"])


class ProductPostValidator(BaseModel):
    product_id: str
    name: str
    status: int
    stock: int
    description: str
    price: float

    @validator("product_id")
    def validate_product_id(cls, product_id):
        try:
            uuid.UUID(hex=product_id, version=DomainConstants["uuid_version"])
        except ValueError:
            raise ValueError("product_id need to be a valid uuid")
        return product_id

    @validator("status")
    def validate_status(cls, name):
        if status not in [1, 0]:
            raise ValueError("status needs to be 1 or 0")
        return name


class ProductPostController:
    @router.post("", status_code=status.HTTP_201_CREATED)
    @inject
    async def run(
        product: ProductPostValidator,
        product_creator: ProductCreator = Depends(
            Provide[InventaryContainer.products_package.product_creator]
        ),
    ):
        product_creator_request_dto = ProductCreatorRequestDTO(
            id=product.id, name=product.name, duration=product.duration
        )

        creator_result = await product_creator.run(
            request=product_creator_request_dto
        )
        if not creator_result:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": "Product already exists",
                },
            )
