# Copyright (c) 2017-2018 CRS4
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE
# AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import json
import urllib.parse as urlparse
from urllib.parse import parse_qs

from django.http import HttpResponse, HttpResponseRedirect
from djangosaml2.utils import get_custom_setting, is_safe_url_compat

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from hgw_frontend import settings

import logging

from hgw_frontend.models import FlowRequest, ConfirmationCode

logger = logging.getLogger('hgw_frontend.flow_request')


def view_profile(request):
    return HttpResponse("Home sweet home")


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'flow-requests': reverse('flow-requests-list', request=request, format=format)
    })


def saml_redirect_failures(request, **kwargs):
    # redirect the user to the view where he came from
    default_relay_state = get_custom_setting('ACS_DEFAULT_REDIRECT_URL',
                                             settings.LOGIN_REDIRECT_URL)
    relay_state = request.POST.get('RelayState', default_relay_state)

    #TODO wrap with proper exception catch

    parsed_relay_state_url = urlparse.urlparse(relay_state)
    callback = parse_qs(parsed_relay_state_url.query)['callback_url'][0]

    fr_confirm_code = parse_qs(parsed_relay_state_url.query)['confirm_id'][0]

    return cancel_flow_request(fr_confirm_code, callback)


def saml_cancel_login(request, **kwargs):
    return cancel_flow_request(request.GET['confirm_id'], request.GET['callback_url'])


def cancel_flow_request(fr_confirm_code, callback):
    cc = ConfirmationCode.objects.get(code=fr_confirm_code)

    output_success = False
    state = 'aborted'

    logger.debug('Redirecting to the original callback url: %s', callback)

    return HttpResponseRedirect('{}?process_id={}&success={}&status={}'.format(
        callback, cc.flow_request.process_id, json.dumps(output_success), state))
