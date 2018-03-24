import urllib.request
import sys
import re
import os
import operator
import math
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import networkx as nx

printInConsole = False
saveToFile = False

writeHref = False
checkInDepth = False
showGraph = False

writeScriptLink = False
writeImgLink = False

writeText = False
writeCosSimilarity = False

allSitesWordRankings = []
allSubsitesUrlGraphs = {}


def save_file(file):
    file = open(file, 'wb')
    for text in byteTextTable:
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


def word_finder_and_ranking(text):
    word_ranking_dictionary = {}
    for match in re.findall(r'[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]{2,}', text, re.MULTILINE):
        if not match.lower() in word_ranking_dictionary.keys():
            word_ranking_dictionary[match.lower()] = 1
        else:
            word_ranking_dictionary[match.lower()] += 1
    return word_ranking_dictionary


def sort_ranking(word_ranking_dictionary):
    sorted_word_ranking_dictionary = sorted(word_ranking_dictionary.items(), key=operator.itemgetter(1), reverse=True)
    for key, value in sorted_word_ranking_dictionary:
        byteTextTable.append((str(value) + " " + key).encode('utf-8'))
    return sorted_word_ranking_dictionary


def cosinus_similarity(all_sites_word_rankings):
    all_similarities = []
    for i in range(len(all_sites_word_rankings)):
        current_comp_ranking1 = all_sites_word_rankings[i]
        for key, value in current_comp_ranking1.items():
            current_comp_ranking1[key] = [value, 0]
        global_dict = current_comp_ranking1  # 'slowo' = [w pierwszym rankingu, w drugim rankingu]
        for j in range(i + 1, len(all_sites_word_rankings)):
            current_comp_ranking2 = all_sites_word_rankings[j]
            for key2, value2 in current_comp_ranking2.items():
                if key2 in global_dict.keys():
                    global_dict[key2] = [global_dict[key2][0], value2]
                else:
                    global_dict[key2] = [0, value2]

            sum_of_squares1 = 0.0
            sum_of_squares2 = 0.0
            product_of_values = 0.0
            for key, value in global_dict.items():
                sum_of_squares1 += value[0] ** 2
                sum_of_squares2 += value[1] ** 2
                product_of_values += value[0] * value[1]
            dict_vector_length1 = math.sqrt(sum_of_squares1)
            dict_vector_length2 = math.sqrt(sum_of_squares2)
            similarity = product_of_values / (dict_vector_length1 * dict_vector_length2)
            all_similarities.append(similarity)
            print("Cosinus similarity of site: " + str(i) + " and site: " + str(j) + " equals: " + str(similarity))


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


def save_graph(graph_dict, file_name):
    graph = nx.Graph()
    for key, values in graph_dict.items():
        for value in values:
            graph.add_edge(key, value)
    nx.draw(graph, with_labels=True)
    #plt.savefig(file_name)  # or
    plt.show()


if sys.argv[1] == '-site' and sys.argv[2] != '':
    opener = urllib.request.FancyURLopener({})
    urlList = url_setter()
    file_names = []
    depth_value = 0
    subsite_url_list = []
    for parameter in sys.argv:
        if parameter == '-console':
            printInConsole = True

        if parameter == '-file':
            file_names = create_file_name_list(urlList)
            saveToFile = True

        if parameter == '-text':
            writeText = True

        if parameter == '-cos':
            writeCosSimilarity = True

        if parameter == '-a':
            writeHref = True

        if parameter == '-script':
            writeScriptLink = True

        if parameter == '-img':
            writeImgLink = True

        if parameter == '-depth':
            checkInDepth = True
            depth_value = int(sys.argv[sys.argv.index('-depth') + 1])

        if parameter == '-graph':
            showGraph = True

    last_url_in_current_level = urlList[-1]
    for url in urlList:
        if printInConsole:
            print("\n\n" + url)
        f = opener.open(url)
        content = f.read()

        if writeImgLink:
            if printInConsole:
                print("\nimg src: \n")
            byteTextTable = []
            soup = BeautifulSoup(content, 'html.parser')
            inputTag = soup.findAll('img')
            for tag in inputTag:
                if tag.has_attr("src"):
                    byteTextTable.append(tag['src'].encode('utf-8'))
                if printInConsole:
                    print(tag['src'])
            if saveToFile:
                save_file(file_names[urlList.index(url)])

        if writeScriptLink:
            if printInConsole:
                print("\nscript src: \n")
            byteTextTable = []
            soup = BeautifulSoup(content, 'html.parser')  # czy trzeba dorabiać początki adresów stron? przykład allegro
            inputTag = soup.findAll('script')
            for tag in inputTag:
                if tag.has_attr("src"):
                    byteTextTable.append(tag['src'].encode('utf-8'))
                    if printInConsole:
                        print(tag['src'])
            if saveToFile:
                save_file(file_names[urlList.index(url)])

        if writeHref or checkInDepth:
            if printInConsole and writeHref:
                print("\na href: \n")
            byteTextTable = []
            subsite_url_list = []
            soup = BeautifulSoup(content, 'html.parser')
            inputTag = soup.findAll('a')
            for tag in inputTag:
                if tag.has_attr("href"):
                    if 'https://' not in tag["href"] and 'http://' not in tag["href"] and \
                            '#' not in tag["href"] and '@' not in tag["href"] and '.pdf' not in tag["href"] and \
                            '//' not in tag['href']:
                        tag = subsite_full_url_maker(url, tag["href"])
                        if depth_value > 0:
                            subsite_url_list.append(tag)
                            # if tag not in allSubsitesUrlGraphs.keys():
                            #     allSubsitesUrlGraphs[tag] = [url]
                            # else:
                            #     allSubsitesUrlGraphs[tag] += [url]
                    else:
                        tag = tag['href']
                    if '#' not in tag and '@' not in tag and '.pdf' not in tag and '//' not in tag:
                        if writeHref:
                            byteTextTable.append(tag.encode('utf-8'))
                        if printInConsole and writeHref:
                            print(tag)
            if saveToFile and writeHref:
                save_file(file_names[urlList.index(url)])
            if depth_value > 0:
                urlList += subsite_url_list
                if url not in allSubsitesUrlGraphs.keys():
                    allSubsitesUrlGraphs[url] = subsite_url_list
                else:
                    allSubsitesUrlGraphs[url] += subsite_url_list

        if writeText:
            soup = BeautifulSoup(content, 'html.parser')
            [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
            visible_text = soup.getText()
            byteTextTable = []
            wordRanking = word_finder_and_ranking(visible_text)
            allSitesWordRankings.append(wordRanking)
            sortedWordRankingDictionary = sort_ranking(wordRanking)
            for word in byteTextTable:
                if printInConsole:
                    print(word.decode('utf-8'))
                if saveToFile:
                    save_file(file_names[urlList.index(url)])
        if url == last_url_in_current_level:
            depth_value -= 1
            last_url_in_current_level = urlList[-1]
        f.close()
    if writeCosSimilarity and writeText:
        cosinus_similarity(allSitesWordRankings)
    if showGraph:
        save_graph(allSubsitesUrlGraphs, "my_graph.png")
    # -pr - page ranking (wykład) utworzyć bazę danych

    # zrobić własną stronę z id użytkownika i 5 przycisków (rejestrowane kliknięcie - kto kliknął)
else:
    print("The first argument should be '-site'\n" +
          "The second should be '-console' or -file\n" +
          "Then additional arguments like '-text', '-a', '-script', '-img'");
