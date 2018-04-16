import urllib.error
import sys
from bs4 import BeautifulSoup

import utils
import ranking
import graph

printInConsole = False
saveToFile = False

writeHref = False
checkInDepth = False
showGraph = False
showPageRank = False

writeScriptLink = False
writeImgLink = False

writeText = False
writeCosSimilarity = False

allSitesWordRankings = {}
allSubsitesUrlGraphs = {}
allUrlGraphs = {}

if sys.argv[1] == '-site' and sys.argv[2] != '':
    urlList = utils.url_setter()
    main_urls = urlList[:]
    file_names = []
    depth_value = 0
    subsite_url_list = []
    for parameter in sys.argv:
        if parameter == '-console':
            printInConsole = True

        if parameter == '-file':
            file_names = utils.create_file_name_list(urlList)
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

        if parameter == '-pr':
            showPageRank = True
    last_url_in_current_level = urlList[-1]
    for url in urlList:
        if url in urlList[:urlList.index(url)]:
            continue
        if printInConsole:
            print("\n\n" + url)
        try:
            f = urllib.request.urlopen(url)
            content = f.read()
        except ValueError as v:
            print("Read error: " + str(url))
            print(v)
            continue
        except urllib.error.HTTPError as http_error:
            print(http_error)
            print("For url: " + url)
            utils.remove_url(url, urlList, allSubsitesUrlGraphs)
            continue
        except urllib.error.URLError as url_error:
            print(url_error)
            print("For url: " + url)
            utils.remove_url(url, urlList, allSubsitesUrlGraphs)
            continue
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
                utils.save_file(file_names[urlList.index(url)], byteTextTable)

        if writeScriptLink:
            if printInConsole:
                print("\nscript src: \n")
            byteTextTable = []
            soup = BeautifulSoup(content, 'html.parser')
            inputTag = soup.findAll('script')
            for tag in inputTag:
                if tag.has_attr("src"):
                    byteTextTable.append(tag['src'].encode('utf-8'))
                    if printInConsole:
                        print(tag['src'])
            if saveToFile:
                utils.save_file(file_names[urlList.index(url)], byteTextTable)

        if writeHref or checkInDepth:
            if printInConsole and writeHref:
                print("\na href: \n")
            byteTextTable = []
            subsite_url_list = []
            url_list_for_graph = []
            soup = BeautifulSoup(content, 'html.parser')
            inputTag = soup.findAll('a')
            for tag in inputTag:
                if tag.has_attr("href"):
                    if 'https://' not in tag["href"] and 'http://' not in tag["href"] and \
                            '#' not in tag["href"] and '@' not in tag["href"] and '.pdf' not in tag["href"] and \
                            '//' not in tag['href']:
                        tag = utils.subsite_full_url_maker(url, tag["href"])
                        if depth_value > 0:
                            subsite_url_list.append(tag)
                    else:
                        tag = tag['href']
                    if '#' not in tag and '@' not in tag and '.pdf' not in tag:
                        if showGraph:
                            url_list_for_graph.append(tag)
                        if writeHref:
                            byteTextTable.append(tag.encode('utf-8'))
                        if printInConsole and writeHref:
                            print(tag)
            if saveToFile and writeHref:
                utils.save_file(file_names[urlList.index(url)], byteTextTable)
            if depth_value > 0:
                urlList += url_list_for_graph
                if saveToFile:
                    for url_filename in subsite_url_list:
                        str_filename = str(url_filename)
                        for char in [':', '/', '\\', '*', '?', '"', '<', '>', '|']:
                            str_filename = str_filename.replace(char, '.')
                        file_names.append(str_filename + ".txt")
                if url not in allSubsitesUrlGraphs.keys():
                    allSubsitesUrlGraphs[url] = subsite_url_list
                else:
                    allSubsitesUrlGraphs[url] += subsite_url_list
                if showGraph:
                    if url not in allUrlGraphs.keys():
                        allUrlGraphs[url] = url_list_for_graph
                    else:
                        allUrlGraphs[url] += url_list_for_graph

        if writeText or writeCosSimilarity:
            soup = BeautifulSoup(content, 'html.parser')
            [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
            visible_text = soup.getText()
            byteTextTable = []
            wordRanking = ranking.word_finder_and_ranking(visible_text)
            if writeCosSimilarity and url not in allSitesWordRankings.keys():
                allSitesWordRankings[url] = wordRanking
            sortedWordRankingDictionary, byteTextTable = ranking.sort_ranking(wordRanking)
            if writeText:
                for word in byteTextTable:
                    if printInConsole:
                        print(word.decode('utf-8'))
                    if saveToFile:
                        utils.save_file(file_names[urlList.index(url)], byteTextTable)
        if url == last_url_in_current_level:
            depth_value -= 1
            last_url_in_current_level = urlList[-1]
        try:
            f.close()
        except ValueError:
            print("Value Error")
    if writeCosSimilarity:
        if checkInDepth:
            allSitesWordRankings = ranking.concatenate_subsites(allSitesWordRankings, allSubsitesUrlGraphs, main_urls)
        ranking.cosinus_similarity(allSitesWordRankings, main_urls)
    if showGraph:
        pr_graph = graph.make_graph(allUrlGraphs, "my_graph.png")
        if showPageRank:
            graph.show_page_rank(pr_graph)
    #TODO: przerobić graf na domeny; sprawdzać na ostatnich podstonach czy maą odniesienia do stron sprawdzonych wcześniej
    # -pr - page ranking (wykład) utworzyć bazę danych (np firebase)
    # zrobić własną stronę z id użytkownika i 5 przycisków (rejestrowane kliknięcie - kto kliknął)
else:
    print("The first argument should be '-site'\n" +
          "The second should be '-console' or -file\n" +
          "Then additional arguments like '-text', '-a', '-script', '-img'")
