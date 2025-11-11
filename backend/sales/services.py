from django.db import models, transaction

class ProductServices:
    @staticmethod
    def update_quantity(product, diff):
        with transaction.atomic():
            product.quantity = models.F('quantity') + diff
            product.save()
