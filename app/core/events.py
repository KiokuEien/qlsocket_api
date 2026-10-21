from sqlalchemy import event, select

from app.models.product import Product
from app.utils.generators import generate_sku
from app.core.exceptions import GenerationError

@event.listens_for(Product, 'before_insert')
def generate_sku_event(mapper, connection, target) -> None:
    if not target.sku:
        for _ in range(10):
            sku = generate_sku()
            exists = connection.execute(
                select(Product).where(Product.sku == sku)
            ).first()

            if exists is None:
                target.sku = sku
                return
        raise GenerationError(message='Failed to generate a unique SKU after 10 attempts')