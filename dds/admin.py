from django.contrib import admin
from .models import Type, Category, Transaction, Status, Subcategory

# Register your models here.
@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type')
    list_filter = ('type',)
    search_fields = ('name', 'type__name')

admin.site.register(Transaction)
admin.site.register(Status)
admin.site.register(Subcategory)