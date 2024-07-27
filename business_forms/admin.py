from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group

from business_forms.models import MedblogersPreEntry, BusinessForm, NastavnichestvoPreEntry


class MedblogersPreEntryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'timestamp', 'colored_status', 'name', 'email', 'phone', 'formatted_tg_username_link',
        'formatted_tg_phone_link', 'formatted_instagram_link', 'description'
    )
    list_filter = ('status', 'timestamp')

    readonly_fields = (
        'name', 'email', 'phone', 'formatted_tg_username_link', 'formatted_tg_phone_link', 'formatted_instagram_link',
        'tg_username', 'instagram_username', 'policy_agreement'
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class NastavnichestvoPreEntryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'status', 'name', 'email', 'phone', 'instagram_username',
    )
    list_filter = ('status', 'timestamp')

    readonly_fields = ('name', 'email', 'phone', 'tg_username', 'instagram_username')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class BusinessFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('content_type',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['content_type'].queryset = ContentType.objects.filter(
            model__in=['medblogerspreentry', 'nastavnichestvopreentry'])
        return form


admin.site.register(MedblogersPreEntry, MedblogersPreEntryAdmin)
admin.site.register(NastavnichestvoPreEntry, NastavnichestvoPreEntryAdmin)
admin.site.register(BusinessForm, BusinessFormAdmin)

admin.site.unregister(Group)
