# In content_analyzer/admin.py
from django.contrib import admin
from .models import ContentSource, ContentItem, Topic

admin.site.register(ContentSource)
admin.site.register(ContentItem)
admin.site.register(Topic)