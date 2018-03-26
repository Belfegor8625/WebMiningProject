import operator
import re
import math

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
    byte_text_table = []
    for key, value in sorted_word_ranking_dictionary:
        byte_text_table.append((str(value) + " " + key).encode('utf-8'))
    return sorted_word_ranking_dictionary, byte_text_table


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




