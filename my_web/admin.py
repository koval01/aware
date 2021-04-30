from django.contrib import admin
from .models import Info, AWARE_Page

admin.site.register(Info)
admin.site.register(AWARE_Page)
admin.site.site_header = 'Aware Admin Panel'