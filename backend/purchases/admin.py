from django.contrib import admin
from django.forms import BaseModelFormSet, BaseModelForm

from purchases.models import BeerPurchase
from ratings.models import Rating


class RatingInline(admin.StackedInline):
    model = Rating
    extra = 0
    fk_name = 'beer_purchase'
    fields = (
        # beer is derived from parent BeerPurchase
        'added_by',
        'room',
        'color',
        'foam',
        'smell',
        'taste',
        'opinion',
        'note',
        'is_published'
    )

    def has_view_or_change_permission(self, request, obj=None):
        return False


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
    inlines = [RatingInline]

    def save_formset(self, request, form: BaseModelForm, formset: BaseModelFormSet, change: bool) -> None:
        obj: BeerPurchase = form.instance

        for form in formset.extra_forms:
            # derive rated beer from parent BeerPurchase model,
            # so that we do not need to select it manually
            if isinstance(form.instance, Rating):
                form.instance.beer = obj.beer

        super().save_formset(request, form, formset, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        form_field = super().formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'beer':
            form_field.queryset = form_field.queryset.select_related('brewery').order_by('name')

        elif db_field.name == 'sold_to':
            form_field.queryset = form_field.queryset.order_by('username')

        return form_field
