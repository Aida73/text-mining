from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions, status
from .models import *
import json
from django.http import JsonResponse
from .utils import *
import pandas as pd

# Create your views here.


@permission_classes((permissions.AllowAny,))
class DatasetCorrectionView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):

        if 'file' not in request.data:
            raise ParseError("Empty content")

        f = request.data['file']
        target = request.data['target']
        #nom = f.name
        #typeFile = nom.split(".")[1]
        corrected_dataset = correct_target(f, target)

        print(corrected_dataset.head())

        return Response({"file": corrected_dataset}, status=status.HTTP_201_CREATED)

# on R install xml2
# @api_view(['POST'])
# @csrf_exempt
# def data_correction(request):
#     if request.method == "POST":
#         dataset = request.Files['dataset_file']
#         column_target = request.data['target']
#         print(dataset)
#         print(column_target)
#         corrected_dataset = correct_target(dataset, column_target)
#         return Response({"corrected": corrected_dataset})
#     return Response({"error": "erreur"})