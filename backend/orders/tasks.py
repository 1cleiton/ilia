import logging
import os

import celery
import requests
from django.db import transaction

from orders.models import Product


@celery.shared_task
def import_products() -> int:
    logger = logging.getLogger("import_products")
    logger.info("Iniciando a importação de produtos")

    url = os.environ.get("MOCKAPI_URL")
    if not url:
        logger.error("MOCKAPI_URL environment variable is not set")
        return 0

    response = requests.get(f"{url}/products")
    if response.status_code != 200:
        logger.error(f"Falha ao importar produtos: {response.status_code}")
        return 0

    products = response.json()
    logger.info(f"Encontrados {len(products)} produtos na API")

    existing_products = set(Product.objects.values_list("id", flat=True))
    logger.info(
        f"Existem {len(existing_products)} produtos já cadastrados no banco de dados"
    )

    new_products = []

    for p in products:
        if int(p["id"]) not in existing_products:
            new_products.append(
                Product(
                    id=p["id"],
                    name=p["name"],
                    description=p["description"],
                    price=p["price"],
                    available_quantity=p["available_quantity"],
                    image=p["image"],
                )
            )

    if new_products:
        logger.info(f"Encontrados {len(new_products)} novos produtos para importar")
        with transaction.atomic():
            Product.objects.bulk_create(new_products)
            return len(new_products)

    logger.info("Nenhum novo produto para importar")
    return 0
