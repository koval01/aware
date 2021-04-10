from django.contrib import admin
from .models import Post, Quote, Facts, Info, Statistic, AWARE_Page

admin.site.register(Post)
admin.site.register(Quote)
admin.site.register(Facts)
admin.site.register(Info)
admin.site.register(AWARE_Page)
admin.site.register(Statistic)
