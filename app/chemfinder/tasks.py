from __future__ import absolute_import, unicode_literals
import logging
from django.conf import settings
import celery
from celery import chain, shared_task, task
from celery import exceptions as celery_exceptions
from patentparser.celery import app

from .utils import (
    parser,
    manager,
    processor,
    trainer,
    helper,
)


tz = 'Europe/Madrid'
logger = logging.getLogger('msd')


class HandlerTask(celery.Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        if self.request.retries != self.max_retries:
            countdown = self.default_retry_delay ** (self.request.retries + 1)
            logger.error(exc)
            logger.error(f"Error occurred in {self.name} task. Proceeding to retry in {countdown} seconds.")
            self.retry(countdown)
        else:
            logger.error(exc)
            logger.error(f"Error occurred in {self.name} task. Max retries reached.")


@shared_task(base=HandlerTask, bind=True, max_retries=3, default_retry_delay=20, queue='chemfinder')
def initiate_parsing(self):
    # Proceed to retrieve all xml paths to be parsed
    xml_paths = helper.retrieve_xml_files()

    for filepath in xml_paths:
        try:
            parsing = chain(
                parse_patent.s(filepath) |
                persist_patent.s()).apply_async()
                # persist_patent.s() |
                # generate_ner.s() |
                # persist_ner.s()).apply_async()
                # generate_chemner.s(),
                # persist_chemner.s().apply_async()

        # TODO
        except Exception as exc:
            logger.error(f"[ERROR] on global task: {exc}")

    return "Started patent parsing"


@shared_task(base=HandlerTask, bind=True, max_retries=3, default_retry_delay=20, queue='chemfinder')
def parse_patent(self, filepath):
    xml_parser = parser.XMLParser(filepath)
    parsed_patent = xml_parser.parse_document()
    return parsed_patent


@shared_task(base=HandlerTask, bind=True, max_retries=3, default_retry_delay=20, queue='chemfinder')
def persist_patent(self, data):
    inventor_manager = manager.InventorManager()
    patent_manager = manager.PatentManager()

    # Persist inventors
    persisted_inventors = [inventor_manager.get_or_create(inventor) for inventor in data["inventors"]]
    data["inventors"] = persisted_inventors

    # Persist patent
    patent = patent_manager.get_or_create(data)

    unrecognized_data = {
        "abstract": patent.abstract,
        "description": patent.description,
    }
    return unrecognized_data


@shared_task(base=HandlerTask, bind=True, max_retries=3, default_retry_delay=20, queue='chemfinder')
def generate_ner(self, data):
    ner_generator = processor.NERGenerator()
    entities = ner_generator.generate_named_entities(data)
    return entities


@shared_task(base=HandlerTask, bind=True, max_retries=3, default_retry_delay=20, queue='chemfinder')
def persist_ner(self, data):
    # Persist NER
    ner_manager = manager.NERManager()
    for ner in data:
        ner_manager.create(ner)


@shared_task(base=HandlerTask, bind=True, max_retries=3, default_retry_delay=20, queue='chemfinder')
def generate_chemner(self, generator, data):
    entities = generator.generate_named_entities(data)
    persist_chemner(entities)
    return entities


@shared_task(base=HandlerTask, bind=True, max_retries=3, default_retry_delay=20, queue='chemfinder')
def persist_chemner(self, data):
    # Persist ChemNER
    ner_manager = manager.ChemNERManager()
    for ner in data:
        ner_manager.create(ner)


@shared_task(base=HandlerTask, bind=True, max_retries=3, default_retry_delay=20, queue='chemfinder')
def train_ner(self):
    ner_trainer = trainer.ModelTrainer(settings.TRAIN_DATA_PATH)
    data = ner_trainer.generate_training_data()
    ner_trainer.train_entity_recognizer(train_data=data)


@shared_task(base=HandlerTask, bind=True, max_retries=3, default_retry_delay=20, queue='chemfinder')
def generate_trained_ner(self, generator, data):
    entities = generator.generate_named_entities(data)
    return entities


@shared_task(base=HandlerTask, bind=True, max_retries=3, default_retry_delay=20, queue='chemfinder')
def persist_trained_ner(self, data):
    # Persist TrainedNER
    trained_ner_manager = manager.TrainedNERManager()
    for ner in data:
        trained_ner_manager.create(ner)
