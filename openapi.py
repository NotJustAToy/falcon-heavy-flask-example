# Copyright 2020 Not Just A Toy Corp.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging

from falcon_heavy.contrib.flask.decorators import FlaskAbstractOpenAPIDecorator
from falcon_heavy.contrib.parsers import JSONParser
from falcon_heavy.contrib.renderers import JSONRenderer
from falcon_heavy.contrib.responses import OpenAPIResponse
from falcon_heavy.contrib.operations import OpenAPIOperations


logger = logging.getLogger(__name__)


# Implement all abstract methods
class OpenAPIDecorator(FlaskAbstractOpenAPIDecorator):

    def _handle_not_found(self, request, instance, exception):
        logger.error("Operation not found", exc_info=exception)
        return OpenAPIResponse(status_code=404)

    def _handle_parse_error(self, request, operation, instance, exception):
        logger.error("Caught an error during request parsing", exc_info=exception)
        return OpenAPIResponse(status_code=500)

    def _handle_render_error(self, request, operation, instance, exception):
        logger.error("Caught an error during response rendering", exc_info=exception)

    # This method evoked if a request not passed authorization.
    def _handle_authorization_failed(self, request, operation, instance, reasons):
        pass

    # Security methods must return ``None`` or reason that describes why the request is not authorized.
    # Just pass these methods for authorize any request.
    def _apply_api_key_security(self, request, instance, key, scopes, context):
        pass

    def _apply_http_security(self, request, instance, scheme, token, scopes, context, bearer_format=None):
        pass

    def _apply_oauth2_security(self, request, instance, flows, scopes, context):
        pass

    def _apply_open_id_connect_security(self, request, instance, open_id_connect_url, scopes, context):
        pass

    def _handle_invalid_request(self, request, operation, instance, exception):
        logger.exception("Invalid request", exc_info=exception)
        return OpenAPIResponse(status_code=400)

    def _handle_invalid_response(self, request, operation, instance, exception):
        logger.exception("Invalid response", exc_info=exception)

    def _handle_exception(self, request, instance, exception):
        logger.exception("Caught an exception", exc_info=exception)
        return OpenAPIResponse(status_code=500)


# Load operations from specification
operations = OpenAPIOperations.from_file(os.path.join(os.path.dirname(__file__), 'petstore.yaml'))

# Instantiate decorator
openapi = OpenAPIDecorator(operations, parsers=(JSONParser(),), renderers=(JSONRenderer(),))
