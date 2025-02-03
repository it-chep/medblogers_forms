import requests
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from django.conf import settings

from business_forms.forms import MedblogersPreEntryForm, NationalBlogersAssociationForm
from business_forms.models import BusinessForm, MedblogersPreEntry, NationalBlogersAssociation
from business_forms.utils import format_phone_number, get_site_url


def health_check(request):
    return JsonResponse({"status": "ok"}, status=200)


class BaseForm:
    form_method = ""
    client_id = 0

    def call_api_method(self, data: dict):
        for admin_id in self.admins:
            data["message"] = self.form_method
            data["client_id"] = admin_id
            requests.post(settings.SALEBOT_API_URL, json=data)


class MedblogersPreEntryView(TemplateView, BaseForm):
    template_name = 'business_forms/medbloggers_pre_entry_form.html'
    form_class = MedblogersPreEntryForm
    form_method = "docstar_push_notification"
    admins = [settings.ADMINS_CHAT_ID]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        content_type = ContentType.objects.get_for_model(MedblogersPreEntry)
        context["business_form_settings"] = BusinessForm.objects.filter(content_type=content_type).first()
        context["medblogers_form"] = self.form_class()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        result = {"success": False}

        if form.is_valid():
            instance = form.save()
            data = {
                "doctor_instagram_link": instance.instagram_link,
                "doctor_tg_phone_link": instance.tg_phone_link,
                "doctor_tg_username_link": instance.tg_username_link,
                "doctor_tg_username": instance.tg_username,
                "doctor_name": instance.name,
                "doctor_phone": format_phone_number(instance.phone),
                "doctor_wa_link": instance.wa_link
            }
            self.call_api_method(data)
            result.update({"success": True, "redirect_url": get_site_url() + reverse("spasibo_medbloger")})
        else:
            result.update({"errors": form.errors})

        return JsonResponse(result)


class SpasiboMedblogersPreEntryView(TemplateView):
    template_name = 'business_forms/spasibo_medbloggers_pre_entry_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        content_type = ContentType.objects.get_for_model(MedblogersPreEntry)
        context["business_form_settings"] = BusinessForm.objects.filter(content_type=content_type).first()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)


class NationalBlogersAssociationView(TemplateView, BaseForm):
    template_name = "business_forms/national_blogers_association_form.html"
    form_class = NationalBlogersAssociationForm
    form_method = "national_push_notification"
    admins = [settings.ADMINS_CHAT_ID]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        content_type = ContentType.objects.get_for_model(NationalBlogersAssociation)
        context["business_form_settings"] = BusinessForm.objects.filter(content_type=content_type).first()
        context["national_form"] = self.form_class()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        result = {"success": False}

        if form.is_valid():
            form.save()
            self.call_api_method(form.cleaned_data["name"], form.cleaned_data["phone_number"])
            result.update({"success": True, "redirect_url": get_site_url() + reverse("spasibo_national_medbloger")})

        else:
            result.update({"errors": form.errors})

        return JsonResponse(result)


class SpasiboNationalBlogersAssociationView(TemplateView):
    template_name = "business_forms/spasibo_national_blogers_association_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        content_type = ContentType.objects.get_for_model(NationalBlogersAssociation)
        context["business_form_settings"] = BusinessForm.objects.filter(content_type=content_type).first()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
