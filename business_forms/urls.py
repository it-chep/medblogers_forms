from django.urls import path

from business_forms.views import MedblogersPreEntryView, SpasiboMedblogersPreEntryView

urlpatterns = [
    path('spasibo_medbloger/', SpasiboMedblogersPreEntryView.as_view(), name='spasibo_medbloger'),
    path('', MedblogersPreEntryView.as_view(), name='medblogers_form')
]
