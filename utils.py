import os
import sys


def save_file(file, byte_text_table):
    file = open(file, 'wb')
    for text in byte_text_table:
        file.write(text + os.linesep.encode('utf-8'))
    file.close()


def create_file_name_list(url_list):
    file_names = []
    for i in range(1, len(url_list) + 1):
        try:
            filename = sys.argv[sys.argv.index('-file') + i]
            if filename.startswith('-'):
                filename = 'default' + str(i) + '.txt'
        except IndexError:
            filename = 'default' + str(i) + '.txt'
        file_names.append(filename)
    return file_names


def add_url_beginning(short_url):
    full_url = 'http://' + short_url
    return full_url


def subsite_full_url_maker(url, tag_str):
    url_parts = url.split('/')[:3]
    if tag_str.startswith('/'):
        subsite_url = str(url_parts[0]) + "//" + str(url_parts[2]) + tag_str
    else:
        subsite_url = str(url_parts[0]) + "//" + str(url_parts[2]) + '/' + tag_str
    return subsite_url


def url_setter():
    urls = []
    url_counter = 0
    while True:
        url = sys.argv[url_counter + 2]
        if url.startswith('-'):
            break
        if url.endswith(',') and ',' in url[:-1]:
            url = url[:-1]
            new_urls = url.split(',')
            for elem in new_urls:
                if ('https://' or 'http://') not in elem:
                    elem = add_url_beginning(elem)
                urls.append(elem)
            split_size = len(new_urls)
            url_counter += split_size
        elif url.endswith(','):
            url = url[:-1]
            if 'https://' not in url and 'http://' not in url:
                url = add_url_beginning(url)
            urls.append(url)
            url_counter += 1
        elif ',' in url:
            new_urls = url.split(',')
            for elem in new_urls:
                if ('https://' or 'http://') not in elem:
                    elem = add_url_beginning(elem)
                urls.append(elem)
            split_size = len(new_urls)
            url_counter += split_size
        else:
            if 'https://' not in url and 'http://' not in url:
                url = add_url_beginning(url)
            urls.append(url)
            url_counter += 1
    return urls


def remove_url(url, url_list, url_graph):
    for u in url_list:
        if url_graph.get(u) is not None:
            if url in url_graph.get(u):
                url_graph.get(u).remove(url)
                url_list.remove(url)


def make_domains(all_url_graph):
    domain_graph = {}
    for key, values in all_url_graph.items():
        key_domain_parts = key.split('/')[:3]
        domain_key = key_domain_parts[0] + "//" + key_domain_parts[2]
        for value in values:
            value_domain_parts = value.split('/')
            domain_value = value_domain_parts[0] + "//" + value_domain_parts[2]
            if domain_key not in domain_graph.keys():
                domain_graph[domain_key] = [domain_value]
            else:
                if domain_value not in domain_graph.get(domain_key):
                    domain_graph[domain_key] += [domain_value]
    return domain_graph
