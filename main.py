import urllib.request
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

writeScriptLink = False
writeImgLink = False

writeText = False
writeCosSimilarity = False

allSitesWordRankings = []
allSubsitesUrlGraphs = {}

if sys.argv[1] == '-site' and sys.argv[2] != '':
    opener = urllib.request.FancyURLopener({})
    urlList = utils.url_setter()
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

    last_url_in_current_level = urlList[-1]
    for url in urlList:
        if printInConsole:
            print("\n\n" + url)
        try:
            f = opener.open(url)
            content = f.read()
        except IOError:
            print("Read error")
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
            soup = BeautifulSoup(content, 'html.parser')  # czy trzeba dorabiać początki adresów stron? przykład allegro
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
                        if writeHref:
                            byteTextTable.append(tag.encode('utf-8'))
                        if printInConsole and writeHref:
                            print(tag)
            if saveToFile and writeHref:
                utils.save_file(file_names[urlList.index(url)], byteTextTable)
            if depth_value > 0:
                urlList += subsite_url_list
                if url not in allSubsitesUrlGraphs.keys():
                    allSubsitesUrlGraphs[url] = subsite_url_list
                else:
                    allSubsitesUrlGraphs[url] += subsite_url_list

        if writeText or writeCosSimilarity:
            soup = BeautifulSoup(content, 'html.parser')
            [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
            visible_text = soup.getText()
            byteTextTable = []
            wordRanking = ranking.word_finder_and_ranking(visible_text)
            allSitesWordRankings.append(wordRanking)
            sortedWordRankingDictionary, byteTextTable = ranking.sort_ranking(wordRanking)
            for word in byteTextTable:
                if printInConsole and writeText:
                    print(word.decode('utf-8'))
                if saveToFile and writeText:
                    utils.save_file(file_names[urlList.index(url)], byteTextTable)
        if url == last_url_in_current_level:
            depth_value -= 1
            last_url_in_current_level = urlList[-1]
        f.close()
    if writeCosSimilarity:
        ranking.cosinus_similarity(allSitesWordRankings)
    if showGraph:
        graph.make_graph(allSubsitesUrlGraphs, "my_graph.png")
    # -cos do poprawy
    # -pr - page ranking (wykład) utworzyć bazę danych

    # zrobić własną stronę z id użytkownika i 5 przycisków (rejestrowane kliknięcie - kto kliknął)
else:
    print("The first argument should be '-site'\n" +
          "The second should be '-console' or -file\n" +
          "Then additional arguments like '-text', '-a', '-script', '-img'");
