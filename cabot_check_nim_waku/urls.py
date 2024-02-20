from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from cabot.rest_urls import create_viewset, status_check_fields

from .views import (NimWakuCheckCreateView, NimWakuCheckUpdateView, duplicate_check)
from .models import NimWakuStatusCheck

api_router = DefaultRouter()
api_router.register(r'nim_waku_checks', create_viewset(
    arg_model=NimWakuStatusCheck,
    arg_fields=status_check_fields + (
        'address',
        'log_level',
        'proto_relay',
        'proto_store',
        'proto_filter',
        'proto_lightpush',
        'wss_cert',
        'wss_key',
    ),
))

urlpatterns = [

    url(r'^nimwakucheck/create/',
        view=NimWakuCheckCreateView.as_view(),
        name='create-nim-waku-check'),

    url(r'^nimwakucheck/update/(?P<pk>\d+)/',
        view=NimWakuCheckUpdateView.as_view(),
        name='update-nim-waku-check'),

    url(r'^nimwakucheck/duplicate/(?P<pk>\d+)/',
        view=duplicate_check,
        name='duplicate-nim-waku-check'),

    url(r'^api/', include(api_router.urls)),
]
