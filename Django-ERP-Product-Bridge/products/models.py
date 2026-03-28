from django.db import models
#from decimal import Decimal


# Create your models here.
class Product(models.Model):
    external_id = models.IntegerField(unique=True)
    code = models.CharField(max_length=100 , unique=True)
    description = models.TextField(max_length=200,blank=True,unique=True)
    name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=100, blank=True , unique=True)
    retail_price = models.FloatField()#DecimalField(max_digits=10, decimal_places=2,default=0, blank=True, null=True)
    wholesale_price = models.FloatField()#DecimalField(max_digits=10, decimal_places=2,default=0, blank=True, null=True)
    discount = models.FloatField()#DecimalField(max_digits=10, decimal_places=2,default=0, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    # @property
    # def final_price(self):
    #      return self.retail_price * (Decimal("1") - Decimal(self.discount) / Decimal("100"))

    def __str__(self):
        return f"""Product Info:
                    External ID:{self.external_id} code: {self.code}
                    description:{self.description} name: {self.name}
                    barcode:{self.barcode} retail price: {self.retail_price} wholesale price: {self.wholesale_price}
                    discount:{self.discount} updated at:{self.updated_at}"""