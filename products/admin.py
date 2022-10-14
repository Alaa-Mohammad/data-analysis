from django.contrib import admin
from django.forms import Field
from .models import Product
from import_export.admin import ImportExportMixin
from import_export import resources

class ProductResource(resources.ModelResource):
    image=Field()
    created=Field()
    class Meta:
        model=Product
        fields=['name','price','image','created']
    
    def dehydrate_image(self,obj):
        return obj.image.path
    def dehydrate_created(self,obj):
        return obj.created.strftime('%d-%M-%Y')      

    
class ProductAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class=ProductResource
    list_display=['name','price','created','image_tag']


admin.site.register(Product,ProductAdmin)