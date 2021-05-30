from django.contrib import admin
from .models import Info, AWARE_Page, BlackWord

admin.site.register(Info)
admin.site.register(AWARE_Page)
admin.site.register(BlackWord)
admin.site.site_header = 'Aware Admin Panel'