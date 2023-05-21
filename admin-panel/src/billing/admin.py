from django.contrib import admin

from billing.models import Subscription, SubscriptionFilmwork
from movies.models import Filmwork


class FilmworkSubscriptionInline(admin.TabularInline):
    model = SubscriptionFilmwork
    autocomplete_fields = ['subscription_id']
    search_fields = ['filmwork_id__name']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    readonly_fields = ('created_by',)
    list_display = ('name', 'periodic_type', 'cost', 'charge_type')
    inlines = (FilmworkSubscriptionInline,)
    search_fields = ('name', )

    def save_model(self, request, obj, form, change):
        if not change:  # if the object is being created, set created_by
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
