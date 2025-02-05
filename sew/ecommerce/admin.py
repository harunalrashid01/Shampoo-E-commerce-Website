from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Master)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['title1', 'subtitle', 'price', 'is_active', 'created_at', 'modified_at', 'created_by', 'modified_by']
    search_fields = ['title1', 'subtitle', 'description']

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user  # Set 'created_by' to the current admin user if it's a new record
        obj.modified_by = request.user  # Always set 'modified_by' to the current admin user
        obj.save()

admin.site.register(Offer, OfferAdmin)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Testimonial)
admin.site.register(Contact)
admin.site.register(Subscriber)
