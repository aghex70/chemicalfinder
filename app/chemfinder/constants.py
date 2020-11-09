from .utils import manager


TYPE_TO_NER_MANAGER = {
    "ner": manager.NERManager,
    "chemner": manager.ChemNERManager,
    "trained": manager.TrainedNERManager,
}