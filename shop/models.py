from datetime import timezone
from django.utils import timezone
from django.db import models
from django.urls import reverse
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=100, db_index=True)
    slug=models.SlugField(max_length=100, db_index=True)
    description=models.TextField()

    class Meta:
        ordering=('name',)
        verbose_name='category'
        verbose_name_plural='categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',args=[self.slug])

# клас Product -> таблиця shop_product
class Product(models.Model):
    category = models.ForeignKey('Category', related_name='products',on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('name',)
        index_together = (('id', 'name'),)


# db_table='product'

    def __str__(self):
        return self.name
