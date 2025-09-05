from django.contrib import admin
from .models import Document

from django.utils.html import format_html

class DocumentAdmin(admin.ModelAdmin): 
    list_display = ('title','author', 'description', 'image_show', 'document_show_name', 'uploaded_at') 
    search_fields = ('title','author', 'description', 'document')
    list_filter = ('uploaded_at',)

    def image_show(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" style="max-width:100px; max-height:100px;" />')
        return "-"
    image_show.short_description = 'Image'

    def document_show_name(self, obj):
        if(obj.document):
            return format_html(f'<a href="{obj.document.url}" target="_blank">{obj.document.name.split("/")[-1]}</a>')
        return "-"
    document_show_name.short_description = 'Document'

admin.site.register(Document, DocumentAdmin)
