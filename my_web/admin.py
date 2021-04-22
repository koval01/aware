from django.contrib import admin
from .models import Quote, Facts, Info, AWARE_Page

admin.site.register(Quote)
admin.site.register(Facts)
admin.site.register(Info)
admin.site.register(AWARE_Page)
admin.site.site_header = 'AWARE Admin Panel'