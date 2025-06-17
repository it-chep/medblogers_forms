from django.urls import path

from business_forms.views import (
    health_check,
    MedblogersPreEntryView, SpasiboMedblogersPreEntryView,
    NationalBlogersAssociationView, SpasiboNationalBlogersAssociationView,
    ExpressMedblogerView, SpasiboExpressMedblogerView, NeuroMedblogerView, SpasiboNeuroMedblogerView,
)

urlpatterns = [
    path("health/", health_check),

    path("spasibo_neuro_medbloger/", SpasiboNeuroMedblogerView.as_view(), name="spasibo_neuro_medbloger"),
    path("neuro_medbloger/", NeuroMedblogerView.as_view(), name="neuro_medbloger"),

    path("spasibo_express_medbloger/", SpasiboExpressMedblogerView.as_view(), name="spasibo_express_medbloger"),
    path("express_medbloger/", ExpressMedblogerView.as_view(), name="express_medbloger"),

    path('spasibo_national_medbloger/', SpasiboNationalBlogersAssociationView.as_view(), name='spasibo_national_medbloger'),
    path('national_medbloger/', NationalBlogersAssociationView.as_view(), name='national_medbloger'),

    path('spasibo_medbloger/', SpasiboMedblogersPreEntryView.as_view(), name='spasibo_medbloger'),
    path('', MedblogersPreEntryView.as_view(), name='medblogers_form'),
]
