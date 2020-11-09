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

    @staticmethod
    def wipe_inventors():
        Inventor.objects.all().delete()

    @staticmethod
    def retrieve_all_inventors():
        return Inventor.objects.values()

    @staticmethod
    def get_inventions(inventor_name):
        inventor = Inventor.objects.get(name=inventor_name)
        filtered_values = (
            "file_name", "country", "document_number", "kind", "date", "title", "abstract", "description")
        return Patent.objects.filter(
            inventors={"name": inventor_name, "address": inventor.address}).values(*filtered_values)


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

    @staticmethod
    def retrieve_patents_details():
        filtered_values = (
            "file_name", "country", "document_number", "kind", "date", "title", "abstract", "description")
        return Patent.objects.values(*filtered_values)

    @staticmethod
    def wipe_patents():
        InventorManager.wipe_inventors()
        Patent.objects.all().delete()


class NERManager:
    @staticmethod
    def create(data):
        if not NER.objects.filter(text=data[0], label=data[1], ner_type="NER").exists():
            return NER.objects.create(text=data[0], label=data[1], ner_type="NER")

    @staticmethod
    def list_ners():
        return NER.objects.filter(ner_type="NER").values()

    @staticmethod
    def wipe_ners():
        NER.objects.filter(ner_type="NER").delete()


class ChemNERManager:
    @staticmethod
    def create(data):
        if not NER.objects.filter(text=data[0], label=data[1], ner_type="ChemNER").exists():
            NER.objects.create(text=data[0], label=data[1], ner_type="ChemNER")

    @staticmethod
    def list_ners():
        return NER.objects.filter(ner_type="ChemNER").values()

    @staticmethod
    def wipe_chemners():
        NER.objects.filter(ner_type="ChemNER").delete()


class TrainedNERManager:
    @staticmethod
    def create(data):
        if not NER.objects.filter(text=data[0], label=data[1], ner_type="TrainedNER").exists():
            NER.objects.create(text=data[0], label=data[1], ner_type="TrainedNER")

    @staticmethod
    def list_ners():
        return NER.objects.filter(ner_type="TrainedNER").values()

    @staticmethod
    def wipe_trained_ners():
        NER.objects.filter(ner_type="TrainedNER").delete()


class GodManager:
    @staticmethod
    def wipe_database():
        InventorManager.wipe_inventors()
        PatentManager.wipe_patents()
        NERManager.wipe_ners()
        ChemNERManager.wipe_chemners()
        TrainedNERManager.wipe_trained_ners()
