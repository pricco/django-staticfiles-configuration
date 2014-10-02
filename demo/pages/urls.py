from django.conf.urls import url
from django.views.generic.base import TemplateView

from pages.views import HomeView


urlpatterns = [
    url(r'^$',
        HomeView.as_view(),
        name='home'),
]
