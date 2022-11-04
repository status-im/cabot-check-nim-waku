from django import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from cabot.cabotapp.models import StatusCheck
from cabot.cabotapp.views import (CheckCreateView, CheckUpdateView,
                                  StatusCheckForm, base_widgets)

from .models import NimWakuStatusCheck


class NimWakuStatusCheckForm(StatusCheckForm):
    symmetrical_fields = ('service_set', 'instance_set')

    class Meta:
        model = NimWakuStatusCheck
        fields = (
            'name',
            'address',
            'log_level',
            'proto_relay',
            'proto_store',
            'proto_filter',
            'proto_lightpush',
            'timeout',
            'frequency',
            'active',
            'importance',
            'debounce',
        )

        widgets = dict(**base_widgets)
        widgets.update({
            'address': forms.TextInput(attrs={
                'style': 'width: 100%',
                'placeholder': '/dns4/node.example.org/tcp/1234/p2p/16Uiu2HA...',
            }),
            'log_level': forms.Select(attrs={
                'data-rel': 'chosen',
            }),
        })


class NimWakuCheckCreateView(CheckCreateView):
    model = NimWakuStatusCheck
    form_class = NimWakuStatusCheckForm


class NimWakuCheckUpdateView(CheckUpdateView):
    model = NimWakuStatusCheck
    form_class = NimWakuStatusCheckForm


def duplicate_check(request, pk):
    pc = StatusCheck.objects.get(pk=pk)
    npk = pc.duplicate()
    return HttpResponseRedirect(reverse('update-nimwaku-check', kwargs={'pk': npk}))
