import urllib.request
import sys
import re
import os
import operator
from bs4 import BeautifulSoup

printInConsole = False
saveToFile = False

writeText = False
writeHref = False
writeScriptLink = False
writeImgLink = False

byteTextTable = []
wordRankingDictionary = {}

for parameter in sys.argv:
    if (parameter == '-console'):
        printInConsole = True

    if (parameter == '-file' and sys.argv[4] != ''):
        saveToFile = True

    if (parameter == '-text'):
        writeText = True

    if (parameter == '-a'):
        writeHref = True

    if (parameter == '-script'):
        writeScriptLink = True

    if (parameter == '-img'):
        writeImgLink = True


def consolePrint(printInConsole, text):
    text.decode('utf-8')
    if (printInConsole == True):
        print(text)


def saveFile(saveToFile, byteTextTable):
    if (saveToFile):
        file = open(sys.argv[4], 'wb')
        for text in byteTextTable:
            file.write(text + os.linesep.encode('utf-8'))
        file.close()


def wordFinderAndRanking(text, byteTextTable):
    wordRankingDictionary = {}
    for match in re.findall(r'[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]{2,}', text, re.MULTILINE):
        if not match.lower() in wordRankingDictionary.keys():
            wordRankingDictionary[match.lower()] = 1
        else:
            wordRankingDictionary[match.lower()] += 1
    sortedRanking = sorted(wordRankingDictionary.items(), key=operator.itemgetter(1), reverse=True)
    for key, value in sortedRanking:
        byteTextTable.append((str(value) + " " + key).encode('utf-8'))


if (sys.argv[1] == '-site' and sys.argv[2] != ''):
    opener = urllib.request.FancyURLopener({})
    f = opener.open(sys.argv[2])
    content = f.read()
    # dodać funkcjonalność zapisu o domyślnej nazwie i zapisu tylko tego co niezbędne

    """""if (saveToFile):
        file = open(sys.argv[4], 'wb')
        file.write(content)
        file.close()"""""

    if (writeImgLink):
        print("\n\nimg src: \n")
        byteTextTable = []
        soup = BeautifulSoup(content, 'html.parser')
        inputTag = soup.findAll('img')
        for tag in inputTag:
            if (tag.has_attr("src")):
                byteTextTable.append(tag['src'].encode('utf-8'))
                consolePrint(printInConsole, tag['src'])
        saveFile(saveToFile, byteTextTable)

    if (writeScriptLink):
        print("\n\nscript src: \n")
        byteTextTable = []
        soup = BeautifulSoup(content, 'html.parser')  # czy trzeba dorabiać początki adresó stron? przykład allegro
        inputTag = soup.findAll('script')
        for tag in inputTag:
            if (tag.has_attr("src")):
                byteTextTable.append(tag['src'].encode('utf-8'))
                consolePrint(printInConsole, tag['src'])
        saveFile(saveToFile, byteTextTable)

    if (writeHref):
        print("\n\na href: \n")
        byteTextTable = []
        soup = BeautifulSoup(content, 'html.parser')
        inputTag = soup.findAll('a')
        for tag in inputTag:
            if (tag.has_attr("href")):
                byteTextTable.append(tag['href'].encode('utf-8'))
                consolePrint(printInConsole, tag['href'])
        saveFile(saveToFile, byteTextTable)

    if (writeText):
        soup = BeautifulSoup(content, 'html.parser')
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
        visible_text = soup.getText()
        byteTextTable = []
        wordFinderAndRanking(visible_text, byteTextTable)
        for word in byteTextTable:
            consolePrint(printInConsole, word)
        saveFile(saveToFile, byteTextTable)
else:
    print("The first argument should be '-site'\n" +
          "The second should be '-console' or -file\n" +
          "Then additional arguments like '-text', '-a', '-script', '-img'");
