import json
from django.apps import apps
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers import *


class DataManipulation(viewsets.ModelViewSet):
    def create(self, request):
        post_successful = True
        over_all_result_ok = []
        over_all_result_nok = []
        sorted_json = sort_json_data(request.data, get_model_ordering())
        for item in sorted_json:
            model_type = list(item.keys())[0]
            model_values = list(item.values())[0]
            result = serialize_model(model_type, model_values)
            if result[0] is False:
                post_successful = False
                add_result_into_dict(over_all_result_nok, model_type, result)
            else:
                add_result_into_dict(over_all_result_ok, model_type, result)
        if post_successful:
            return Response({"status": over_all_result_ok}, status=status.HTTP_201_CREATED)
        return Response({"status": over_all_result_nok}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            models = apps.get_app_config('api').get_models()

            for model in models:
                model.objects.all().delete()

            return Response({"status": "All data has been deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"status": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ListModelView(APIView):
    def get(self, request, model_name):
        try:
            model_class = apps.get_model(app_label='api', model_name=model_name)
            query = model_class.objects.all()
            if query.exists():
                serializer_class = SerializersLink().get_serializer_class(model_name)
                serializer = serializer_class(query, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"status": f"no data for '{model_name}'"}, status=status.HTTP_404_NOT_FOUND)
        except LookupError as e:
            return Response({"status": str(e)}, status=status.HTTP_404_NOT_FOUND)


class DetailModelView(APIView):
    def get(self, request, model_name, item_id):
        try:
            model_class = apps.get_model(app_label="api", model_name=model_name)
            query = model_class.objects.filter(id=item_id)
            if query.exists():
                serializer_class = SerializersLink().get_serializer_class(model_name)
                serializer = serializer_class(query, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"status": f"no data for '{model_name}' with id: '{item_id}'"},
                                status=status.HTTP_404_NOT_FOUND)
        except LookupError as e:
            return Response({"status": str(e)}, status=status.HTTP_404_NOT_FOUND)


def get_model_ordering():
    model_ordering = [
        'AttributeName', 'AttributeValue', 'Attribute',
        'Product', 'ProductAttributes', 'Image',
        'ProductImage', 'Catalog'
    ]
    return model_ordering


def sort_json_data(json_data, model_ordering):
    sorted_list = []
    for process in model_ordering:
        for item in json_data:
            if list(item.keys())[0] == process:
                sorted_list.append(item)
    return sorted_list


def add_result_into_dict(over_all_result, model_type, result):
    over_all_result.append(
        {
            "model_type": model_type,
            "result": result[0],
            "message": result[1]
        }
    )
    return over_all_result


def serialize_model(model_type, model_values):
    serializer_class = SerializersLink().get_serializer_class(model_type)
    if serializer_class:
        serializer = serializer_class(data=model_values)
        if serializer.is_valid():
            serializer.save()
            return True, f"Json data '{model_values}' for model '{model_type}' are correct according serializer"
        else:

            return False, f"Invalid json data '{model_values}' input in model type: '{model_type}'"
    else:
        return False, f"Not implemented model type: '{model_type}'"


class SerializersLink:
    def __init__(self):
        self._map_dict = {
            "AttributeName": AttributeNameSerializer,
            "AttributeValue": AttributeValueSerializer,
            "Attribute": AttributeSerializer,
            "Product": ProductSerializer,
            "ProductAttributes": ProductAttributesSerializer,
            "Image": ImageSerializer,
            "ProductImage": ProductImageSerializer,
            "Catalog": CatalogSerializer,
        }

    def get_serializer_class(self, model_name):
        if model_name in self._map_dict:
            return self._map_dict[model_name]
        return False
