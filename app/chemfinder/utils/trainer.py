from __future__ import unicode_literals, print_function
import csv
import random
import warnings
from pathlib import Path

import spacy
from spacy.util import minibatch, compounding
from django.conf import settings


class ModelTrainer:

    def __init__(self, train_data_path, model=None):
        self._train_data_path = train_data_path
        self._model = model if model else "en_core_sci_sm"

        if model is not None:
            self._processor = spacy.load(model)  # load existing spaCy model
            print("Loaded model '%s'" % model)
        else:
            self._processor = spacy.blank("en")  # create blank Language class
            print("Created blank 'en' model")

    def generate_training_data(self):
        training_data = []
        with open(self._train_data_path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                compound_info = (0, len(row["COMPOUND"]), "COMPOUND")
                entities = ({"entities": [compound_info]})
                data = (row["COMPOUND"].strip(), entities)
                training_data.append(data)
        # Remove last line added (blank field)
        training_data.pop()
        return training_data

    def train_entity_recognizer(self, train_data, n_iter=1):
        """Set up the pipeline and train the entity recognizer."""

        # create the built-in pipeline components and add them to the pipeline
        # nlp.create_pipe works for built-ins that are registered with spaCy
        if "ner" not in self._processor.pipe_names:
            ner = self._processor.create_pipe("ner")
            self._processor.add_pipe(ner, last=True)
        # otherwise, get it so we can add labels
        else:
            ner = self._processor.get_pipe("ner")

        # add labels
        for _, annotations in train_data:
            for ent in annotations.get("entities"):
                ner.add_label(ent[2])

        # get names of other pipes to disable them during training
        pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
        other_pipes = [pipe for pipe in self._processor.pipe_names if pipe not in pipe_exceptions]
        # only train NER
        with self._processor.disable_pipes(*other_pipes), warnings.catch_warnings():
            # show warnings for misaligned entity spans once
            warnings.filterwarnings("once", category=UserWarning, module='spacy')

            self._processor.begin_training()
            # reset and initialize the weights randomly
            for itn in range(n_iter):
                random.shuffle(train_data)
                losses = {}
                # batch up the examples using spaCy's minibatch
                batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
                for batch in batches:
                    texts, annotations = zip(*batch)
                    self._processor.update(
                        texts,  # batch of texts
                        annotations,  # batch of annotations
                        drop=0.5,  # dropout - make it harder to memorise data
                        losses=losses,
                    )
                print("Losses", losses)
        # save model to output directory
        output_dir = Path(settings.TRAINED_MODEL_PATH)
        if not output_dir.exists():
            output_dir.mkdir()
        self._processor.to_disk(output_dir)
        print("Saved model to", output_dir)
