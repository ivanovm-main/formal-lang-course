from dataclasses import dataclass
from os import PathLike

import cfpq_data
import networkx as nx


@dataclass
class GraphInfo:
    n_nodes: int
    n_edges: int
    labels: set[str]


def get_graph_info_by_name(graph_name: str) -> GraphInfo:
    graph = cfpq_data.graph_from_csv(cfpq_data.download(graph_name))
    n_nodes = graph.number_of_nodes()
    n_edges = graph.number_of_edges()
    labels = set([label for _, _, label in graph.edges(data="label")])  # None if no label
    labels.discard(None)
    return GraphInfo(n_nodes, n_edges, labels)


def create_two_cycles_graph(first_cycle_n_nodes: int,
                            second_cycle_n_nodes: int,
                            labels: tuple[str, str],
                            file_path: str | PathLike[str]) -> nx.MultiDiGraph:
    graph = cfpq_data.labeled_two_cycles_graph(n=first_cycle_n_nodes, m=second_cycle_n_nodes, labels=labels)

    pydot_graph = nx.drawing.nx_pydot.to_pydot(graph)
    pydot_graph.write_raw(file_path)

    return graph
