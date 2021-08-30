from django.contrib import admin

from .models import Info, AWSE_Page, BlackWord, Banner

admin.site.register(Info)
admin.site.register(AWSE_Page)
admin.site.register(BlackWord)
admin.site.register(Banner)
admin.site.site_header = 'AWSE Admin Panel'
