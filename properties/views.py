from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import Property
from .serializers import PropertySerializer


@cache_page(60 * 15)
@vary_on_cookie
@api_view(["GET"])
def property_list(request):
    properties = Property.objects.all()
    serializer = PropertySerializer(properties, many=True)
    return Response(serializer.data)
