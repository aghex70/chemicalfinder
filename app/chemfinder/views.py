import logging

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes
from drf_yasg.utils import swagger_auto_schema

from .utils import manager
from . import (
    tasks,
    models,
    serializers,
    constants
)


class BaseViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = ()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._logger = logging.getLogger('chemfinder')

    @property
    def logger(self):
        """Return logger"""
        return self._logger

    @logger.setter
    def logger(self, value):
        """Set logger"""
        self._logger = value

    def wipe_database(self, request):
        manager.TrainedNERManager.wipe_trained_ners()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PatentParserViewSet(BaseViewSet):
    """
    Viewset in charge of patents management.
    """

    def list(self, request):
        patents = models.Patent.objects.all().values()
        return Response(data=patents, status=status.HTTP_200_OK)

    def create(self, request):
        # Initialize the parsing process
        tasks.initiate_parsing.apply_async(countdown=0)
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request):
        manager.PatentManager.wipe_patents()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NERViewSet(BaseViewSet):
    """
    Viewset in charge of NERs management.
    """

    @swagger_auto_schema(query_serializer=serializers.NERSerializer)
    def list(self, request):
        serializer = serializers.NERSerializer(data=request.query_params)
        if not serializer.is_valid():
            self.logger.error(f"Validation error: {serializer.errors}")
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        ner_manager = constants.TYPE_TO_NER_MANAGER.get(serializer.validated_data.get("type"))
        ners = ner_manager.list_ners()
        return Response(data=ners, status=status.HTTP_200_OK)

    def train(self, request):
        tasks.train_ner.apply_async()
        return Response(status=status.HTTP_201_CREATED)

    def create_ner(self, request):
        patents = manager.PatentManager.retrieve_all_patents()
        for i in range(len(patents)):
            patent_information = {
                "abstract": patents[i].abstract,
                "description": patents[i].description,
            }
            tasks.ner_creation.apply_async((patent_information,), countdown=0)
        return Response(status=status.HTTP_201_CREATED)

    def create_chemner(self, request):
        patents = manager.PatentManager.retrieve_all_patents()
        for i in range(len(patents)):
            patent_information = {
                "abstract": patents[i].abstract,
                "description": patents[i].description,
            }
            tasks.chemner_creation.apply_async((patent_information,), countdown=0)
        return Response(status=status.HTTP_201_CREATED)

    def create_trained_ner(self, request):
        patents = manager.PatentManager.retrieve_all_patents()
        for i in range(len(patents)):
            patent_information = {
                "abstract": patents[i].abstract,
                "description": patents[i].description,
            }
            tasks.trained_ner_creation.apply_async((patent_information,), countdown=0)
        return Response(status=status.HTTP_201_CREATED)

    def destroy_ner(self, request):
        manager.NERManager.wipe_ners()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy_chemner(self, request):
        manager.ChemNERManager.wipe_chemners()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy_trained_ner(self, request):
        manager.TrainedNERManager.wipe_trained_ners()
        return Response(status=status.HTTP_204_NO_CONTENT)
