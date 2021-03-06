from django.contrib import admin
from .models import Subscriber, Alert, Keyword, PasteId


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


@admin.register(Subscriber)
class Subscriber(admin.ModelAdmin):
    list_display = ['user_rec', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user_rec']


@admin.register(Alert)
class Alert(admin.ModelAdmin):
    list_display = ['id', 'keyword', 'url', 'status', 'created_at']
    list_filter = ('keyword', ('status', custom_titled_filter('Active Status')))
    search_fields = ['id', 'url', 'keyword']

    def make_disable(self, request, queryset):
        rows_updated = queryset.update(status=False)

        if rows_updated == 1:
            message_bit = "1 alert was"
        else:
            message_bit = "%s alerts were" % rows_updated
        self.message_user(request, "%s successfully marked as disable." % message_bit)

    make_disable.short_description = "Disable selected alerts"

    def make_enable(self, request, queryset):
        rows_updated = queryset.update(status=True)

        if rows_updated == 1:
            message_bit = "1 alert was"
        else:
            message_bit = "%s alerts were" % rows_updated
        self.message_user(request, "%s successfully marked as enable." % message_bit)

    make_enable.short_description = "Enable selected alerts"

    actions = [make_disable, make_enable]


@admin.register(Keyword)
class Keyword(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']


@admin.register(PasteId)
class PasteId(admin.ModelAdmin):
    list_display = ['paste_id', 'created_at']
    list_filter = ['created_at']
    search_fields = ['paste_id']
