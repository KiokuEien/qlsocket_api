from uuid import uuid4

def generate_sku() -> str:
    sku = f'{uuid4().hex[:10].upper()}'
    return sku