from django.contrib import admin

from purchases.models import BeerPurchase


@admin.register(BeerPurchase)
class BeerPurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'sold_to', 'beer', 'packaging',
        'volume_ml', 'price', 'purchased_at'
    )
    list_select_related = ('beer', 'sold_to')
    search_fields = (
        'beer__name', 'beer__style__name',
        'beer__brewery__name', 'sold_to__username'
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        form_field = super().formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'beer':
            form_field.queryset = form_field.queryset.order_by('name')

        elif db_field.name == 'sold_to':
            form_field.queryset = form_field.queryset.order_by('username')

        return form_field
