from django.contrib import admin
from .models import SingleTokenAccess

@admin.register(SingleTokenAccess)
class SingleTokenAccessAdmin(admin.ModelAdmin):
    readonly_fields = ("create_date",)
