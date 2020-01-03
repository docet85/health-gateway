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
import logging

from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse, HttpResponseRedirect

from urllib.parse import urlparse
from urllib.parse import parse_qs

from django.utils.crypto import get_random_string
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from djangosaml2.utils import get_custom_setting

from hgw_frontend.models import ConfirmationCode, FlowRequest, Channel
from hgw_frontend import settings

logger = logging.getLogger('hgw_frontend.flow_request')


def view_profile(request):
    return HttpResponse("Home sweet home")


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'flow-requests': reverse('flow-requests-list', request=request, format=format)
    })


def saml_redirect_failures(request, *args, **kwargs):
    # redirect the user to the view where he came from
    default_relay_state = get_custom_setting('ACS_DEFAULT_REDIRECT_URL',
                                             settings.LOGIN_REDIRECT_URL)

    import traceback
    errstr = traceback.format_exc().splitlines()

    logger.debug('Collected SAML2 failure')
    try:
        saml2_err = (errstr[-2].split(': ')[0])
        if saml2_err.find('saml2') < 0:
            error_status = 'unknown'
        else:
            error_status = saml2_err.split('.')[-1]
    except IndexError:
        error_status = 'unknown'

    relay_state = request.POST.get('RelayState', default_relay_state)

    parsed_relay_state_url = urlparse(relay_state)
    try:
        callback = parse_qs(parsed_relay_state_url.query)['callback_url'][0]
        fr_confirm_code = parse_qs(parsed_relay_state_url.query)['confirm_id'][0]
    except (IndexError, KeyError):
        raise SuspiciousOperation('Missing callback_url or confirm_id in querystring. This should not be.')

    return _abort_flow_request_at_idp_step(fr_confirm_code, callback, result_status_message=error_status)


def abort_saml_login(request, *args, **kwargs):
    return _abort_flow_request_at_idp_step(request.GET['confirm_id'], request.GET['callback_url'])


def _abort_flow_request_at_idp_step(fr_confirm_code, callback, result_status_message='idp_aborted'):
    cc = ConfirmationCode.objects.get(code=fr_confirm_code)

    flow_request = cc.flow_request

    flow_request.status = FlowRequest.DELETE_REQUESTED
    flow_request.save()

    if flow_request.channel_set.all().count() > 0:
        for ch in flow_request.channel_set.all():
            logger.debug("Marking channels as aborted")
            ch.status = Channel.IDP_ABORTED
            ch.save()
    else:
        for source in flow_request.sources.all():
            Channel.objects.create(channel_id=get_random_string(32), flow_request=flow_request,
                                   source=source, status=Channel.IDP_ABORTED)

    output_success = False

    logger.debug('Redirecting to the original callback url: %s', callback)

    return HttpResponseRedirect('{}?process_id={}&success={}&status={}'.format(
        callback, cc.flow_request.process_id, json.dumps(output_success), result_status_message))
