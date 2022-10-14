from django.contrib import admin
from .models import Position, Sale, CSV
from import_export import resources
from import_export.admin import ExportActionMixin
from import_export.fields import Field

class SaleResource(resources.ModelResource):
    customer=Field()
    customer=Field()
    positions=Field()
    created=Field()

    class Meta:
        model=Sale
        fields=('id','transaction_id','positions','total_price','customer','salesman','created')
        export_order= fields
    
    def dehydrate_customer(self,obj):
        return str(obj.customer.name)
    
    def dehydrate_salesman(self,obj):
        return str(obj.salesman.user.username)

    def dehydrate_positions(self,obj):
        position_list= (' , '.join((item.product.name,str(item.quantity))) for item in obj.positions.all())
        str_list=' |'.join(position_list)
        return str_list

    def dehydrate_created(self,obj):
        return obj.created.strftime('%d-%M-%Y')    

    
    
    
class SaleAdmin(ExportActionMixin,admin.ModelAdmin):
    resource_class=SaleResource
    
    
admin.site.register(Position)
admin.site.register(Sale,SaleAdmin)
admin.site.register(CSV)