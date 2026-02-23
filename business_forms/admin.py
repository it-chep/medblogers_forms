from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group

from business_forms.models import MedblogersPreEntry, BusinessForm, NastavnichestvoPreEntry, ExpressMedbloger, \
    NeuroMedbloger, SMMSpecialists, MedSMM


class MedblogersPreEntryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'timestamp', 'colored_status', 'name', 'email', 'phone', 'formatted_tg_username_link',
        'formatted_tg_phone_link', 'formatted_instagram_link', 'formatted_wa_link', 'description'
    )
    list_filter = ('status', 'timestamp')

    readonly_fields = (
        'name', 'email', 'phone', 'formatted_tg_username_link', 'formatted_tg_phone_link', 'formatted_instagram_link',
        'formatted_wa_link', 'tg_username', 'instagram_username', 'policy_agreement'
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


class ExpressMedblogerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'email', 'phone', 'formatted_tg_username_link',
        'formatted_tg_phone_link', 'formatted_instagram_link', 'formatted_wa_link'
    )
    readonly_fields = ('name', 'email', 'phone', 'tg_username', 'instagram_username')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class NeuroMedblogerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'email', 'phone', 'formatted_tg_username_link',
        'formatted_tg_phone_link', 'formatted_wa_link'
    )
    readonly_fields = ('name', 'email', 'phone', 'tg_username',)

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
            model__in=['medblogerspreentry', 'nastavnichestvopreentry', 'nationalblogersassociation',
                       'expressmedbloger', 'neuromedbloger']
        )
        return form


class SMMSpecialistsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'specialization', 'user_contact',
        'formatted_user_contact',
    )
    readonly_fields = ('formatted_user_contact',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(MedblogersPreEntry, MedblogersPreEntryAdmin)
admin.site.register(NastavnichestvoPreEntry, NastavnichestvoPreEntryAdmin)
admin.site.register(BusinessForm, BusinessFormAdmin)
admin.site.register(ExpressMedbloger, ExpressMedblogerAdmin)
admin.site.register(NeuroMedbloger, NeuroMedblogerAdmin)
admin.site.register(SMMSpecialists, SMMSpecialistsAdmin)


class MedSMMAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'timestamp', 'name', 'email', 'phone', 'formatted_tg_username_link',
        'formatted_instagram_link',
    )
    list_filter = ('timestamp',)
    readonly_fields = (
        'name', 'email', 'phone', 'tg_username', 'instagram_username',
        'formatted_tg_username_link', 'formatted_instagram_link',
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(MedSMM, MedSMMAdmin)

admin.site.unregister(Group)
