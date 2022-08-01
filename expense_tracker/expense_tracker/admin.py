from django.contrib import admin
from .models import Profile, Expense, Category


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'limit_flag', 'limit')
    list_display_links = ['user']
    search_fields = ['user']


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'category', 'date', 'name', 'amount')
    list_display_links = ('user', 'category', 'name')
    search_fields = ('user', 'date', 'category', 'amount')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'name')
    list_display_links = ('pk', 'user', 'name')
    search_fields = ('user', 'name')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category, CategoryAdmin)
