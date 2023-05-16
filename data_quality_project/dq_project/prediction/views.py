from django.shortcuts import render, HttpResponse
import pickle
from my_transformers import predictors, spacy_tokenizer
from django.conf import settings
import os

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.decorators import permission_classes
from rest_framework import permissions, status

from .models import *
from dq_app.utils import read_dataset
import pandas as pd
import pickle


def load_model(text):
    MODEL_FILE = os.path.join(
        settings.MODELS, "model.pkl")
    model = pickle.load(open(MODEL_FILE, "rb"))
    return model['model'].predict([text])[0]


@permission_classes((permissions.AllowAny,))
class PredictionProfession(APIView):
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(operation_description="description")
    def post(self, request):

        if 'data' not in request.data:
            raise ParseError("Empty content")

        f = request.data['data']
        dataset = pd.read_json(f)
        if "profession" in dataset.columns:
            dataset['prediction'] = dataset['profession'].swifter.apply(
                load_model)
        return Response({"predicted_dataset": dataset}, status=status.HTTP_201_CREATED)
