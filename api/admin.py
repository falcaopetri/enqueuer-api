from django.contrib import admin

from .models import Queue, MediaService, Media

# Register your models here
admin.site.register(Queue)
admin.site.register(MediaService)
admin.site.register(Media)

