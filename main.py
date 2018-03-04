import urllib.request
import sys
from bs4 import BeautifulSoup

printInConsole = False
saveToFile = False

writeText = False
writeHref = False
writeScriptLink = False
writeImgLink = False

for parameter in sys.argv:
    if (parameter == '-console'):
        printInConsole = True
    
    if (parameter == '-file' and sys.argv[4] != ''):
        saveToFile = True

    if (parameter == '-text'):
        writeText = True

    if (parameter == '-a'):
        writeHref = True

    if  (parameter == '-script'):
        writeScriptLink = True

    if (parameter == '-img'):
        writeImgLink = True


if (sys.argv[1] == '-site' and sys.argv[2] != ''):
    opener = urllib.request.FancyURLopener({})
    f = opener.open(sys.argv[2])
    content = f.read()

    if (printInConsole):
        print(content)

    if (saveToFile):
        file = open(sys.argv[4],'wb')
        file.write(content)
        file.close()

    if (writeImgLink):
        print("\n\nimg src: \n")
        soup = BeautifulSoup(content, 'html.parser')
        inputTag = soup.findAll('img')
        for tag in inputTag:
            if (tag.has_attr("src")):
                print(tag['src'])

    if (writeScriptLink):
        print("\n\nscript src: \n")
        soup = BeautifulSoup(content, 'html.parser')
        inputTag = soup.findAll('script') 
        for tag in inputTag:
            if (tag.has_attr("src")):
                print(tag['src'])

    if (writeHref):
        print("\n\na href: \n")
        soup = BeautifulSoup(content, 'html.parser')
        inputTag = soup.findAll('a') 
        for tag in inputTag:
            if (tag.has_attr("href")):
                print(tag['href'])

    if (writeText):
        soup = BeautifulSoup(content, 'html.parser')
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
        visible_text = soup.getText()
        print(tag['href'])