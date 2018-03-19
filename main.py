import urllib.request
import sys
import re
import os
import operator
import math
from bs4 import BeautifulSoup

printInConsole = False
saveToFile = False

writeHref = False
writeScriptLink = False
writeImgLink = False

writeText = False
writeCosSimilarity = False

allSitesWordRankings = []


def consolePrint(printInConsole, text):
    if printInConsole == True and writeText == True:
        print(text.decode('utf-8'))
    elif printInConsole == True:
        print(text)


def saveFile(byteTextTable, file):
    file = open(file, 'wb')
    for text in byteTextTable:
        file.write(text + os.linesep.encode('utf-8'))
    file.close()


def createFileNameList(urlList):
    filenames = []
    for i in range(1, len(list) + 1):
        try:
            filename = sys.argv[sys.argv.index('-file') + i]
            if filename.startswith('-'):
                filename = 'default' + str(i) + '.txt'
        except IndexError:
            filename = 'default' + str(i) + '.txt'
        filenames.append(filename)
    return filenames


def wordFinderAndRanking(text, byteTextTable):
    wordRankingDictionary = {}
    for match in re.findall(r'[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]{2,}', text, re.MULTILINE):
        if not match.lower() in wordRankingDictionary.keys():
            wordRankingDictionary[match.lower()] = 1
        else:
            wordRankingDictionary[match.lower()] += 1

    return wordRankingDictionary


def sortRanking(wordRankingDictionary):
    sortedWordRankingDictionary = sorted(wordRankingDictionary.items(), key=operator.itemgetter(1), reverse=True)
    for key, value in sortedWordRankingDictionary:
        byteTextTable.append((str(value) + " " + key).encode('utf-8'))
    return sortedWordRankingDictionary


def cosinusSimilarity(allSitesWordRankings):
    allSimilarities = []
    for i in range(len(allSitesWordRankings)):
        currentCompRanking1 = allSitesWordRankings[i]
        for key, value in currentCompRanking1.items():
            currentCompRanking1[key] = [value, 0]
        globalDict = currentCompRanking1  # 'slowo' = [w pierwszym rankingu, w drugim rankingu]
        for j in range(i + 1, len(allSitesWordRankings)):
            currentCompRanking2 = allSitesWordRankings[j]
            for key2, value2 in currentCompRanking2.items():
                if key2 in globalDict.keys():
                    globalDict[key2] = [globalDict[key2][0], value2]
                else:
                    globalDict[key2] = [0, value2]

            sumOfSquares1 = 0.0
            sumOfSquares2 = 0.0
            productOfValues = 0.0
            for key, value in globalDict.items():
                sumOfSquares1 += value[0] ** 2
                sumOfSquares2 += value[1] ** 2
                productOfValues += value[0] * value[1]
            dictVectorLength1 = math.sqrt(sumOfSquares1)
            dictVectorLength2 = math.sqrt(sumOfSquares2)
            allSimilarities.append(productOfValues / (dictVectorLength1 * dictVectorLength2))
    print('Cosinus similarity = ' + str(allSimilarities))


def urlSetter():
    urls = []
    urlCounter = 0
    while True:
        url = sys.argv[urlCounter + 2]
        if url.startswith('-'):
            break
        if url.endswith(',') and ',' in url[:-1]:
            url = url[:-1]
            newUrls = url.split(',')
            for elem in newUrls:
                if ('https://' or 'http://') not in elem:
                    elem = addUrlBeginning(elem)
                urls.append(elem)
            splitSize = len(newUrls)
            urlCounter += splitSize
        elif url.endswith(','):
            url = url[:-1]
            if 'https://' not in url and 'http://' not in url:
                url = addUrlBeginning(url)
            urls.append(url)
            urlCounter += 1
        elif ',' in url:
            newUrls = url.split(',')
            for elem in newUrls:
                if ('https://' or 'http://') not in elem:
                    elem = addUrlBeginning(elem)
                urls.append(elem)
            splitSize = len(newUrls)
            urlCounter += splitSize
        else:
            if 'https://' not in url and 'http://' not in url:
                url = addUrlBeginning(url)
            urls.append(url)
            urlCounter += 1
    return urls


def addUrlBeginning(shortUrl):
    fullUrl = 'http://' + shortUrl
    return fullUrl


if sys.argv[1] == '-site' and sys.argv[2] != '':
    opener = urllib.request.FancyURLopener({})
    urlList = urlSetter()
    print(urlList)
    filenames = []
    for parameter in sys.argv:
        if parameter == '-console':
            printInConsole = True

        if parameter == '-file':
            filenames = createFileNameList(urlList)
            print(filenames)
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

    for url in urlList:
        print(url)
        f = opener.open(url)
        content = f.read()

        if writeImgLink:
            print("\n\nimg src: \n")
            byteTextTable = []
            soup = BeautifulSoup(content, 'html.parser')
            inputTag = soup.findAll('img')
            for tag in inputTag:
                if tag.has_attr("src"):
                    byteTextTable.append(tag['src'].encode('utf-8'))
                    consolePrint(printInConsole, tag['src'])
            if saveToFile:
                saveFile(byteTextTable, filenames[urlList.index(url)])

        if writeScriptLink:
            print("\n\nscript src: \n")
            byteTextTable = []
            soup = BeautifulSoup(content, 'html.parser')  # czy trzeba dorabiać początki adresów stron? przykład allegro
            inputTag = soup.findAll('script')
            for tag in inputTag:
                if tag.has_attr("src"):
                    byteTextTable.append(tag['src'].encode('utf-8'))
                    consolePrint(printInConsole, tag['src'])
            if saveToFile:
                saveFile(byteTextTable, filenames[urlList.index(url)])

        if writeHref:
            print("\n\na href: \n")
            byteTextTable = []
            soup = BeautifulSoup(content, 'html.parser')
            inputTag = soup.findAll('a')
            for tag in inputTag:
                if tag.has_attr("href"):
                    byteTextTable.append(tag['href'].encode('utf-8'))
                    consolePrint(printInConsole, tag['href'])
            if saveToFile:
                saveFile(byteTextTable, filenames[urlList.index(url)])

        if writeText:
            soup = BeautifulSoup(content, 'html.parser')
            [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
            visible_text = soup.getText()
            byteTextTable = []
            wordRanking = wordFinderAndRanking(visible_text, byteTextTable)
            allSitesWordRankings.append(wordRanking)
            sortedWordRankingDictionary = sortRanking(wordRanking)
            for word in byteTextTable:
                consolePrint(printInConsole, word)
                if saveToFile:
                    saveFile(byteTextTable, filenames[urlList.index(url)])
        f.close()
    if writeCosSimilarity and writeText:
        cosinusSimilarity(allSitesWordRankings)
    # -depth np 2; glebokosc odczytu podstron strony
    # -cos miara cosinusowa
    # -graph - graf skierowany podstron strony
    # -pr - page ranking (wykład) utworzyć bazę danych

    # zrobić własną stronę z id użytkownika i 5 przycisków (rejestrowane kliknięcie - kto kliknął)
else:
    print("The first argument should be '-site'\n" +
          "The second should be '-console' or -file\n" +
          "Then additional arguments like '-text', '-a', '-script', '-img'");
