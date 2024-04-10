from django.contrib import admin
from django.conf import settings
from django.utils.safestring import mark_safe

from .models import SingleTokenAccess

@admin.register(SingleTokenAccess)
class SingleTokenAccessAdmin(admin.ModelAdmin):
    list_display = ('slug','contact','link_edit', 'link_show')
    readonly_fields = ("create_date",)

    def link_edit(self,obj):
        return mark_safe("<a href='"+settings.SITE_URL+'/cms/edit/'+obj.slug+"?token="+obj.token+"' >Edit</a>")

    def link_show(self,obj):
        return mark_safe("<a href='"+settings.SITE_URL+'/'+obj.slug+"' >Show</a>")
