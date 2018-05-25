import xml.etree.ElementTree


def parse_xml(xml_name):
    e = xml.etree.ElementTree.parse(xml_name).getroot()
    sentences = []
    for a_type in e.findall('row'):
        sentences.append(a_type.get('Text'))
    return sentences

