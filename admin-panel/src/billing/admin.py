from django.contrib import admin

from billing.models import Subscription, SubscriptionFilmwork, Transaction, FundsOnHold, Balance


class FilmworkSubscriptionInline(admin.TabularInline):
    model = SubscriptionFilmwork
    autocomplete_fields = ['subscription_id']
    search_fields = ['filmwork_id__name']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    readonly_fields = ('created_by', 'payment_gw_product_id', 'payment_gw_price_id', 'all_time_cost', )
    list_display = ('name', 'description', 'cost', 'duration', 'all_time_cost', )
    inlines = (FilmworkSubscriptionInline,)
    search_fields = ('name',)

    def save_model(self, request, obj, form, change):
        if not change:  # if the object is being created, set created_by
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid', 'user_uuid', 'cost', 'timestamp', 'type')


@admin.register(FundsOnHold)
class FundsOnHoldAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid', 'user_uuid', 'cost', 'timestamp', 'type')


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid', 'user_uuid', 'balance', 'timestamp_offset')
    search_fields = ('user_uuid', 'timestamp_offset')
