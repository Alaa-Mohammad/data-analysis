from django.db import models
from django.utils.html import format_html

class Product(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='products', default='no_picture.png')
    price = models.FloatField(help_text='in US dollars $')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}-{self.created.strftime('%d/%m/%Y')}"

    def image_tag(self):
        return format_html('<img src="/media/{}" style="width:40px; height:40px; border-radius:50%"/> '.format(self.image))