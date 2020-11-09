import os
from glob import glob

from django.conf import settings


def retrieve_xml_files():
    print(os.getcwd())
    # TODO cambiar a variable de entorno
    patents_path = settings.PATENTS_PATH
    paths = [y for x in os.walk(patents_path) for y in glob(os.path.join(x[0], '*.xml'))]
    return paths