from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy
from .models import Post, Quote, Facts, Info, Statistic, AWARE_Page

admin.site.register(Post)
admin.site.register(Quote)
admin.site.register(Facts)
admin.site.register(Info)
admin.site.register(AWARE_Page)
admin.site.register(Statistic)

class MyAdminSite(AdminSite):
    site_title = ugettext_lazy('Q-Writer Admin Panel')
    site_header = ugettext_lazy('Q-Writer Admin Panel')
    index_title = ugettext_lazy('Q-Writer Admin Panel')


admin_site = MyAdminSite()
