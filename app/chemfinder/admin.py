from django.contrib import admin
from .models import Inventor, Patent, NER


class InventorAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']
    list_display_links = ['name', ]
    search_fields = ['name']


class PatentAdmin(admin.ModelAdmin):
    list_display = ['document_number', 'title', 'created_date']
    list_display_links = ['document_number', 'title']
    search_fields = ['document_number', 'title']


class NERAdmin(admin.ModelAdmin):
    list_display = ['text', 'label', 'ner_type']
    list_display_links = ['text', 'label', 'ner_type']
    search_fields = ['text', 'label', 'ner_type']


admin.site.register(Inventor, InventorAdmin)
admin.site.register(Patent, PatentAdmin)
admin.site.register(NER, NERAdmin)
