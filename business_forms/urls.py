from django.urls import path

from business_forms.views import (
    MedblogersPreEntryView, SpasiboMedblogersPreEntryView,
    NationalBlogersAssociationView, SpasiboNationalBlogersAssociationView,
)

urlpatterns = [
    path('spasibo_national_medbloger/', SpasiboNationalBlogersAssociationView.as_view(), name='spasibo_national_medbloger'),
    path('national_medbloger/', NationalBlogersAssociationView.as_view(), name='national_medbloger'),
    path('spasibo_medbloger/', SpasiboMedblogersPreEntryView.as_view(), name='spasibo_medbloger'),
    path('', MedblogersPreEntryView.as_view(), name='medblogers_form'),
]
