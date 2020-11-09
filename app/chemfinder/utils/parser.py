from datetime import datetime
from lxml import etree


class Parser:
    def __init__(self, path):
        self._file_path = path


class XMLParser(Parser):

    def __init__(self, path):
        self._root = None
        super().__init__(path=path)

    def parse_document(self):
        self._root = etree.parse(self._file_path)
        metadata = self.parse_metadata()
        data = self.parse_data()
        parsed_data = {**metadata, **data}
        return parsed_data

    def parse_metadata(self):
        metadata = {_data.tag: _data.text for _metadata in self._root.find("//publication-reference").getchildren()
                    for _data in _metadata.getchildren()}
        metadata["file_name"] = self._file_path.split("/")[-1]
        try:
            metadata["date"] = datetime.strftime(datetime.strptime(metadata["date"], "%Y%m%d"), "%Y-%m-%d")
        except (ValueError, TypeError):
            metadata["date"] = None
        return metadata

    def parse_data(self):
        title = self._root.find("//invention-title").text
        abstract = "".join([elem for elem in self._root.xpath("//abstract/p/text()") if elem.strip()])
        description = [elem for elem in self._root.xpath("//description/p/text() | //description/heading/text()")]
        inventors_info = [inventor.getchildren() for inventor in self._root.findall("//inventors/inventor/addressbook")]
        inventors = []
        for inventor in inventors_info:
            name = inventor[0].text
            address = inventor[1].getchildren()[0].text
            inventor = {"name": name, "address": address}
            inventors.append(inventor)

        data = {
            "title": title,
            "abstract": abstract,
            "description": "".join(description),
            "inventors": inventors,
            "chemicals": [],
        }
        return data
