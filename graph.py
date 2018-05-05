import networkx as nx
import matplotlib.pyplot as plt
import operator


def draw_graph(graph_dict, file_name):
    graph = nx.DiGraph()
    for key, values in graph_dict.items():
        for value in values:
            graph.add_edge(key, value)
    nx.draw(graph, with_labels=True)
    # plt.savefig(file_name)  # or
    plt.show()
    return graph


def show_page_rank(graph):
    sorted_pagerank = sorted(nx.pagerank(graph).items(), key=operator.itemgetter(1), reverse=True)
    print(sorted_pagerank)
