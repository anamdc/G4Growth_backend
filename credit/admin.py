from django.contrib import admin
from .models import Credit, Referrer_referee
# Register your models here.

# admin.site.register(Credit)
# admin.site.register(Referrer_referee)

@admin.register(Credit)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'userid', 'date', 'amount', 'referee')


@admin.register(Referrer_referee)
class PostAdmin(admin.ModelAdmin):
    list_display = ('referrer_id', 'referee_id', 'level')