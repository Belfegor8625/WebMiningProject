import networkx as nx
import matplotlib.pyplot as plt


def make_graph(graph_dict, file_name):
    graph = nx.Graph()
    for key, values in graph_dict.items():
        for value in values:
            graph.add_edge(key, value)
    nx.draw(graph, with_labels=True)
    # plt.savefig(file_name)  # or
    plt.show()
