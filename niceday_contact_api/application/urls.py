from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from application.views import ContactView

router = routers.DefaultRouter()

router.register('api/contacts', ContactView)

urlpatterns = [
    path('', include(router.urls))
]