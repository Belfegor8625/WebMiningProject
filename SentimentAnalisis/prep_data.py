import xml.etree.ElementTree
from nltk.tokenize import word_tokenize
import re


def parse_xml_for_comments(xml_name):
    e = xml.etree.ElementTree.parse(xml_name).getroot()
    sentences = []
    for a_type in e.findall('row'):
        sentences.append(a_type.get('Text'))
    return sentences


def parse_xml_for_title_with_post_and_tag(xml_name):
    e = xml.etree.ElementTree.parse(xml_name).getroot()
    titles_and_tags = []
    for a_type in e.findall('row'):
        try:
            tags = a_type.get('Tags')
            text = a_type.get('Title').lower() + " " + a_type.get('Body')[3:-5].lower()
            text = word_tokenize(text)
            tup = (text, [match for match in re.findall(r'[a-zA-Z]{2,}', tags, re.MULTILINE)])
        except:
            continue
        titles_and_tags.append(tup)
    return titles_and_tags


def parse_xml_for_title_with_post(xml_name):
    e = xml.etree.ElementTree.parse(xml_name).getroot()
    texts = []
    for a_type in e.findall('row'):
        try:
            text = a_type.get('Title').lower() + " " + a_type.get('Body')[3:-5].lower()
            text = word_tokenize(text)
        except:
            continue
        texts.append(text)
    return texts


def parse_xml_for_tags_and_count(xml_name):
    e = xml.etree.ElementTree.parse(xml_name).getroot()
    tags = {}
    for a_type in e.findall('row'):
        tag = a_type.get('TagName')
        tags[tag] = int(a_type.get('Count'))
    return tags


def merge_text(titles_and_tags):
    all_text = ''
    for data in titles_and_tags:
        all_text += data[0]
    return all_text
