from typing import Any, Dict

from src.contexts.inventary.products.application import (
    ProductCreatorRequestDTO,
)
from src.contexts.inventary.products.domain import (
    Product,
    ProductDescription,
    ProductName,
    ProductPrice,
    ProductStatus,
    ProductStock,
)
from src.contexts.inventary.shared.domain import ProductId
from tests.shared.utils import FakerData


class ProductMother:
    def __init__(self, faker_provider: object = FakerData) -> None:
        self.faker_provider = faker_provider.faker_data

    @staticmethod
    def create(*, data: Dict[str, Any]) -> Product:
        return Product(
            id=ProductId(data["id"]),
            name=ProductName(data["name"]),
            status=ProductStatus(data["status"]),
            stock=ProductStock(data["stock"]),
            description=ProductDescription(data["description"]),
            price=ProductPrice(data["price"]),
        )

    def create_random_valid(self) -> Product:
        random_valid_product_data = {
            "id": self.faker_data.uuid4(),
            "name": self.faker_data.name(),
            "status": self.faker_data.random_element(elements=(1, 0)),
            "stock": self.faker_data.pyint(max_value=100),
            "description": self.faker_data.paragraph(nb_sentences=1),
            "price": self.faker_data.pyfloat(
                right_digits=2, positive=True, min_value=1.0, max_value=1000.0
            ),
        }
        return self.create(data=random_valid_product_data)

    def create_from_product_creator_request_dto(
        self,
        *,
        product_creator_request_dto: ProductCreatorRequestDTO,
    ) -> Product:
        data = {
            "id": product_creator_request_dto.id,
            "name": product_creator_request_dto.name,
            "status": product_creator_request_dto.status,
            "stock": product_creator_request_dto.stock,
            "description": product_creator_request_dto.description,
            "price": product_creator_request_dto.price,
        }
        return self.create(data=data)