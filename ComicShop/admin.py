from django.contrib import admin
from ComicShop.models import Comic, UserProfile, ShoppingCart, ComicInOrder


# Register your models here.


class ComicAdmin(admin.ModelAdmin):
    list_display = ('name', 'publisher', 'author', 'quantity_in_stock', 'price',)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return obj and request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return obj and request.user.is_superuser


admin.site.register(Comic, ComicAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname')

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return obj and request.user == obj.user or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return obj and request.user == obj.user or request.user.is_superuser


admin.site.register(UserProfile, UserProfileAdmin)


class BoughtComicsInline(admin.TabularInline):
    model = ComicInOrder
    extra = 0


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('dedicated_user',)
    exclude = ('dedicated_user',)
    inlines = [
        BoughtComicsInline,
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.dedicated_user = request.user
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return obj and request.user == obj.dedicated_user or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return obj and request.user == obj.dedicated_user or request.user.is_superuser


admin.site.register(ShoppingCart, ShoppingCartAdmin)
