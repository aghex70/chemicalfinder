import spacy


class NLPProcessor:
    def __init__(self, model):
        self._model = model if model else "en_core_sci_sm"
        self._processor = spacy.load(self._model)

    def tokenize(self, text):
        _doc = self._processor(text)
        tokens = [token.text for token in _doc]
        return tokens

    def retrieve_verbs(self, text):
        _doc = self._processor(text)
        verbs = list(set([token.lemma_ for token in _doc if token.pos_ == "VERB"]))
        return verbs


class NERGenerator(NLPProcessor):
    def __init__(self):
        super().__init__("en_core_web_sm")

    def generate_named_entities(self, data):
        text = f'{data["abstract"]} {data["description"]}'
        _doc = self._processor(text)
        named_entities = [(entity.text, entity.label_) for entity in _doc.ents]
        return named_entities


class ChemNERGenerator(NLPProcessor):
    def __init__(self):
        # TModel consisting of biomedical data in order to improve entity generation
        super().__init__("en_core_sci_sm")

    def generate_named_entities(self, data):
        text = f'{data["abstract"]} {data["description"]}'
        _doc = self._processor(text)
        named_entities = [(entity.text, entity.label_) for entity in _doc.ents]
        return named_entities


class TrainedNERGenerator:
    def __init__(self, model_path):
        self._processor = spacy.load(model_path)
        self.matcher = None

    def generate_named_entities(self, data):
        text = f'{data["abstract"]} {data["description"]}'
        _doc = self._processor(text)
        named_entities = [(entity.text, entity.label_) for entity in _doc.ents]
        return named_entities
