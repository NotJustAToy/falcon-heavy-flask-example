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

from flask import Flask

from falcon_heavy.contrib.flask.routing import rule
from falcon_heavy.contrib.responses import OpenAPIResponse, OpenAPIJSONResponse
from falcon_heavy.contrib.name_resolver import RuntimeNameResolver

from openapi import openapi, operations

app = Flask(__name__)


pets = [
    {
        'id': 1,
        'name': 'Max',
    },
    {
        'id': 2,
        'name': 'Rex',
    },
    {
        'id': 3,
        'name': 'Tom',
    },
]


def next_pet_id():
    return max([rec['id'] for rec in pets]) + 1


def get_pet_by_id(pet_id):
    for pet in pets:
        if pet['id'] == pet_id:
            return pet
    return None


@openapi
def listPets(request):
    limit = request.query_params.get('limit')
    if limit is not None:
        return OpenAPIJSONResponse(pets[:limit])
    return OpenAPIJSONResponse(pets)


@openapi
def createPets(request):
    pets.append({'id': next_pet_id(), 'name': request.content['name']})
    return OpenAPIResponse(status_code=201)


@openapi
def showPetById(request):
    pet_id = request.path_params['petId']
    pet = get_pet_by_id(pet_id)
    if pet is None:
        return OpenAPIResponse(status_code=404)

    return OpenAPIJSONResponse(pet)


resolver = RuntimeNameResolver('app')

# Set up routing according to specification
for path, mapping in operations.items():
    for method, operation in mapping.items():
        # In this example we use ``operationId`` property
        if operation.operation_id is None:
            continue

        view_func = resolver.resolve(operation.operation_id, silent=True)
        if view_func is None:
            continue

        app.add_url_rule(rule(path), view_func=view_func, methods=[method.upper()])


if __name__ == '__main__':
    app.run()
