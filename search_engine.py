import database
import re
import operator


def sort_results(results):
    n = len(results[0].keys())
    items = []
    for i in range(1, n):
        items.append(list(results[0].keys())[i])
    results.sort(key=operator.itemgetter(*items), reverse=True)
    for result in results:
        print(str(result))


again = True
db = database.get_text_from_db()
while again:
    results = []
    search_keywords = input("What are you looking for??\n")
    search_keywords = search_keywords.split(" ")
    for url, data in db.items():
        url = database.get_url(url)
        for d_type, values in data.items():
            if d_type == "text":
                text = values.lower()
                result = dict()
                result['url'] = url
                for keyword in search_keywords:
                    for match in re.findall(keyword, text, re.MULTILINE):
                        if not match.lower() in result.keys():
                            result[keyword] = 1
                        else:
                            result[keyword] += 1
                    if keyword not in result.keys():
                        result[keyword] = 0
                if len(result.keys()) > len(search_keywords):
                    results.append(result)
    print(results)
    sort_results(results)
    repeat_search = input("Another search??\n(Y/N)\n")
    if repeat_search == "Y" or repeat_search == 'y':
        again = True
    else:
        again = False
