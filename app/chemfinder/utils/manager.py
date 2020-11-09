#TODO develop
from datetime import datetime
from ..models import (
    Inventor,
    Patent,
    NER,
)


class InventorManager:
    @staticmethod
    def get_or_create(data):
        if Inventor.objects.filter(name=data["name"], address=data["address"]).exists():
            inventor = Inventor.objects.filter(name=data["name"], address=data["address"])[0]
        else:
            inventor = Inventor.objects.create(name=data["name"], address=data["address"])

        return inventor


class PatentManager:
    @staticmethod
    def get_or_create(data):
        patent = Patent.objects.filter(
            file_name=data["file_name"], country=data["country"], document_number=data["doc-number"],
            kind=data["kind"], date=data["date"], title=data["title"], abstract=data["abstract"],
            description=data["description"])

        if patent.exists():
            patent = patent[0]
        else:
            patent = Patent.objects.create(
                file_name=data["file_name"], country=data["country"], document_number=data["doc-number"],
                kind=data["kind"], date=data["date"], title=data["title"], abstract=data["abstract"],
                description=data["description"], inventors=data["inventors"], created_date=datetime.now())

        return patent

    @staticmethod
    def retrieve_all_patents():
        return Patent.objects.all()


class NERManager:
    @staticmethod
    def create(data):
        if not NER.objects.filter(text=data[0], label=data[1], ner_type="NER").exists():
            return NER.objects.create(text=data[0], label=data[1], ner_type="NER")

    # TODO
    @staticmethod
    def retrieve_all_patents():
        return Patent.objects.all()


class ChemNERManager:
    @staticmethod
    def create(data):
        if not NER.objects.filter(text=data[0], label=data[1], ner_type="ChemNER").exists():
            NER.objects.create(text=data[0], label=data[1], ner_type="ChemNER")

    @staticmethod
    def retrieve_all_patents():
        return Patent.objects.all()


class TrainedNERManager:
    @staticmethod
    def create(data):
        if not NER.objects.filter(text=data[0], label=data[1], ner_type="TrainedNER").exists():
            NER.objects.create(text=data[0], label=data[1], ner_type="TrainedNER")

    @staticmethod
    def retrieve_all_patents():
        return Patent.objects.all()
