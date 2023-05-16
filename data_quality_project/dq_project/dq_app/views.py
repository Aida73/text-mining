from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions, status
from drf_yasg.utils import swagger_auto_schema

from .models import *
from .utils import *
import pandas as pd
import pickle


# Create your views here.


@permission_classes((permissions.AllowAny,))
@swagger_auto_schema(operation_description="partial_update description override", responses={404: 'slug not found'})
class DatasetCorrectionView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):

        if 'file' not in request.data:
            raise ParseError("Empty content")

        f = request.data['file']
        data = pd.read_json(f)
        target = request.data['target']
        corrected_dataset = correct_target(data, target)
        print(corrected_dataset.head())
        # print(data.columns, target)
        return Response({'data': corrected_dataset}, status=status.HTTP_201_CREATED)

# on R install xml2


@permission_classes((permissions.AllowAny,))
class DatasetCategorizationView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):

        if 'data' not in request.data:
            raise ParseError("Empty content")

        f = request.data['data']
        target = request.data['target']
        elements = request.data['elements']
        liste_elements = elements.split(" ")
        data = pd.read_json(f)
        categorized_dataset = find_categories(data, target, liste_elements)
        print(elements.split(" "))
        return Response({"data": categorized_dataset}, status=status.HTTP_201_CREATED)
