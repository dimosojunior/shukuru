from django.contrib import admin
from project1.models import * 

#class ItemAdmin(admin.ModelAdmin):
   # prepopulated_fields = {'slug': ('title',)}
    #list_display = ['title', 'price', 'discount_price']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display=['title','slug','available','created','updated','price']
    list_filter=['available','created','updated']
    list_editable=['price','available']
    prepopulated_fields={'slug':('title',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['name','slug']
    prepopulated_fields={'slug':('name',)}
   
admin.site.register(OrderItem)
admin.site.register(Order)

admin.site.register(ImageSlider)
admin.site.register(CeoImage)
admin.site.register(BackgroundImage)
admin.site.register(OurImages)
admin.site.register(AboutHeaderImage)
admin.site.register(AboutImageOfParagraph)


admin.site.register(Customer)