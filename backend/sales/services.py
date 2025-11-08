from django.db import models, transaction

def update_product_quantity(product, diff):
    with transaction.atomic():
        product.quantity = models.F('quantity') + diff
        product.save()
