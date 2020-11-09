import logging

from rest_framework import viewsets, status
from rest_framework.response import Response
from django.conf import settings

from . import tasks, models
from .utils import parser, helper, trainer, processor, manager


class BaseViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._logger = logging.getLogger('msd')

    @property
    def logger(self):
        """Return logger"""
        return self._logger

    @logger.setter
    def logger(self, value):
        """Set logger"""
        self._logger = value


class PatentParserViewSet(BaseViewSet):
    """
    Viewset that retrieves job offers for all sources.
    """

    authentication_classes = []
    permission_classes = ()

    def list(self, request):
        patents = models.Patent.objects.all().values()
        return Response(data=patents, status=status.HTTP_200_OK)

    def create(self, request):
        # # Proceed to retrieve all xml paths to be parsed
        # Initialize the parsing process
        tasks.initiate_parsing.apply_async(countdown=0)
        return Response(status=status.HTTP_201_CREATED)


class NERViewSet(BaseViewSet):
    """
    Viewset that retrieves job offers for all sources.
    """

    authentication_classes = []
    permission_classes = ()

    def create(self, request):

        return Response(status=status.HTTP_201_CREATED)


class TrainedNERViewSet(BaseViewSet):
    """
    Viewset that retrieves job offers for all sources.
    """

    authentication_classes = []
    permission_classes = ()

    def train(self, request):
        import os
        print("PATH -----> ", os.getcwd())
        tasks.train_ner()
        return Response(status=status.HTTP_201_CREATED)

    def create(self, request):
        trained_ner_generator = processor.TrainedNERGenerator(settings.TRAINED_MODEL_DESTINATION_PATH)
        patents = manager.PatentManager.retrieve_all_patents()
        for i in range(len(patents)):
            patent_information = patents[i].values("abstract", "description")
            tasks.generate_trained_ner(trained_ner_generator, patent_information)
        return Response(status=status.HTTP_201_CREATED)



class AGPPatentViewSet(BaseViewSet):
    """
    Viewset that retrieves job offers for all sources.
    """

    authentication_classes = []
    permission_classes = ()
    # serializer_class = serializers.PositionQuerySerializer

    def create(self, request):
        # Proceed to retrieve all xml paths to be parsed
        xml_paths = helper.retrieve_xml_files()
        path = "chemfinder/patents/basf/uspat1_201831_back_80001_100000/agp.xml"
        parsed_xml = tasks.parse_xml(path)
        persisted_patent = tasks.persist_patent(parsed_xml)
        entities = tasks.generate_ner(persisted_patent)
        tasks.persist_ner(entities)
        return Response(status=status.HTTP_201_CREATED)

    def create_chemner(self, request):
        chem_ner_generator = processor.ChemNERGenerator()
        patents = manager.PatentManager.retrieve_all_patents()
        for i in range(len(patents)):
            patent_information = {
                "abstract": patents[i].abstract,
                "description": patents[i].description,
            }
            # patent_information = patents[i].values("abstract", "description")
            entities = tasks.generate_chemner(chem_ner_generator, patent_information)
            tasks.persist_chemner(entities)
        return Response(status=status.HTTP_201_CREATED)

    def create_trained_ner(self, request):
        trained_ner_generator = processor.TrainedNERGenerator(settings.TRAINED_MODEL_DESTINATION_PATH)
        patents = manager.PatentManager.retrieve_all_patents()
        for i in range(len(patents)):
            patent_information = {
                "abstract": patents[i].abstract,
                "description": patents[i].description,
            }
            entities = tasks.generate_trained_ner(trained_ner_generator, patent_information)
            tasks.persist_trained_ner(entities)
        return Response(status=status.HTTP_201_CREATED)

    def train(self, request):
        import os
        print("PATH -----> ", os.getcwd())
        tasks.train_ner()
        return Response(status=status.HTTP_201_CREATED)
