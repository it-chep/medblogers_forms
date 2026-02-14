import ast
import json

import requests
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from django.conf import settings

from business_forms.forms import MedblogersPreEntryForm, NationalBlogersAssociationForm, ExpressMedblogerForm, \
    NeuroMedblogerForm, SMMForm, SpeecadocForm
from business_forms.models import BusinessForm, MedblogersPreEntry, NationalBlogersAssociation, ExpressMedbloger, \
    NeuroMedbloger, SMMSpecialists, Speecadoc
from business_forms.utils import format_phone_number, get_site_url
from clients.sheets.dto import ExpressMedblogerData, NeuroMedblogerData, SmmSpecialistData, SpeecadocData


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
            self.call_api_method(form.cleaned_data["name"], form.cleaned_data["phone"])
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


class ExpressMedblogerView(TemplateView, BaseForm):
    template_name = 'business_forms/express_medbloger_form.html'
    form_class = ExpressMedblogerForm
    form_method = "diagnosty_push_notification"
    admins = [settings.DIAGNOSTY_CHAT_ID]
    client = settings.SPREADSHEET_CLIENT

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        content_type = ContentType.objects.get_for_model(ExpressMedbloger)
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
            self.client.create_diagnosty_row(ExpressMedblogerData.from_model(instance))
            result.update({"success": True, "redirect_url": get_site_url() + reverse("spasibo_express_medbloger")})
        else:
            result.update({"errors": form.errors})

        return JsonResponse(result)


class SpasiboExpressMedblogerView(TemplateView):
    template_name = 'business_forms/spasibo_express_medbloger_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        content_type = ContentType.objects.get_for_model(ExpressMedbloger)
        context["business_form_settings"] = BusinessForm.objects.filter(content_type=content_type).first()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)


class NeuroMedblogerView(TemplateView, BaseForm):
    template_name = 'business_forms/neuro_medbloger_form.html'
    form_class = NeuroMedblogerForm
    form_method = "neuro_push_notification"
    admins = [settings.VOVA_CHAT_ID]
    client = settings.SPREADSHEET_CLIENT

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        content_type = ContentType.objects.get_for_model(NeuroMedbloger)
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
                "doctor_tg_phone_link": instance.tg_phone_link,
                "doctor_tg_username_link": instance.tg_username_link,
                "doctor_tg_username": instance.tg_username,
                "doctor_name": instance.name,
                "doctor_phone": format_phone_number(instance.phone),
                "doctor_wa_link": instance.wa_link
            }
            self.call_api_method(data)
            self.client.create_neuro_row(NeuroMedblogerData.from_model(instance))
            result.update({"success": True, "redirect_url": get_site_url() + reverse("spasibo_neuro_medbloger")})
        else:
            result.update({"errors": form.errors})

        return JsonResponse(result)


class SpasiboNeuroMedblogerView(TemplateView):
    template_name = 'business_forms/spasibo_neuro_medbloger_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        content_type = ContentType.objects.get_for_model(NeuroMedbloger)
        context["business_form_settings"] = BusinessForm.objects.filter(content_type=content_type).first()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)


class SMMView(TemplateView, BaseForm):
    template_name = 'business_forms/smm_form.html'
    form_class = SMMForm
    form_method = "smm_push_notification"
    admins = [settings.VOVA_CHAT_ID]
    client = settings.SPREADSHEET_CLIENT

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        content_type = ContentType.objects.get_for_model(SMMSpecialists)
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
            instance = form.save(commit=False)

            social_networks_str = form.cleaned_data['social_networks']
            try:
                social_networks_list = ast.literal_eval(social_networks_str)
                social_networks_list = json.loads(social_networks_list[0])
            except (ValueError, SyntaxError):
                social_networks_list = []
            if len(form.data.get("social_networks_another", "")) != 0:
                social_networks_list.append(form.data.get("social_networks_another", ""))

            selected_social_networks = [
                SMMSpecialists.SOCIAL_NETWORKS_MAPPING.get(value, value)
                for value in social_networks_list
            ]
            instance.social_networks = ', '.join(selected_social_networks)

            your_experience_str = form.cleaned_data['your_experience']
            try:
                your_experience_list = ast.literal_eval(your_experience_str)
                your_experience_list = json.loads(your_experience_list[0])
            except (ValueError, SyntaxError):
                your_experience_list = []
            if len(form.data.get("your_experience_another", "")) != 0:
                your_experience_list.append(form.data.get("your_experience_another", ""))

            selected_experiences = [
                SMMSpecialists.YOUR_EXPERIENCE_MAPPING.get(value, value)
                for value in your_experience_list
            ]
            instance.your_experience = ', '.join(selected_experiences)

            instance.save()

            data = {"doctor_tg_username": instance.tg_username_link, }
            self.call_api_method(data)
            self.client.create_smm_row(SmmSpecialistData.from_model(instance))
            result.update({"success": True, "redirect_url": get_site_url() + reverse("spasibo_smm")})
        else:
            result.update({"errors": form.errors})

        return JsonResponse(result)


class SpasiboSMMView(TemplateView):
    template_name = 'business_forms/spasibo_smm_from.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        content_type = ContentType.objects.get_for_model(SMMSpecialists)
        context["business_form_settings"] = BusinessForm.objects.filter(content_type=content_type).first()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)


class SpeecadocView(TemplateView, BaseForm):
    template_name = 'business_forms/speecadoc_form.html'
    form_class = SpeecadocForm
    form_method = "speecadoc_push_notification"
    admins = [settings.DIAGNOSTY_CHAT_ID]
    client = settings.SPREADSHEET_CLIENT

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        content_type = ContentType.objects.get_for_model(Speecadoc)
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
            self.client.create_speecadoc_row(SpeecadocData.from_model(instance))
            result.update({"success": True, "redirect_url": get_site_url() + reverse("spasibo_speecadoc")})
        else:
            result.update({"errors": form.errors})

        return JsonResponse(result)


class SpasiboSpeecadocView(TemplateView):
    template_name = 'business_forms/spasibo_speecadoc_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        content_type = ContentType.objects.get_for_model(Speecadoc)
        context["business_form_settings"] = BusinessForm.objects.filter(content_type=content_type).first()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
