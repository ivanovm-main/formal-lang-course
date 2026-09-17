from unittest.mock import Mock

import cfpq_data
import networkx as nx
import pytest
from cfpq_data import graph_to_csv

from project.graph_utils import get_graph_info_by_name, GraphInfo, create_two_cycles_graph


class TestGetInfo:
    @staticmethod
    def test_nonexistent_file():
        with pytest.raises(FileNotFoundError):
            get_graph_info_by_name("nonexistent_graph")

    @staticmethod
    def test_empty_graph(monkeypatch, tmp_path):
        graph = nx.MultiDiGraph()
        csv_file_path = tmp_path / "graph.csv"
        graph_to_csv(graph, csv_file_path)

        monkeypatch.setattr(cfpq_data, "download", Mock(return_value=csv_file_path))

        expected_info = GraphInfo(0, 0, set())
        actual_info = get_graph_info_by_name("name")

        assert actual_info == expected_info

    @staticmethod
    def test_one_edge(monkeypatch, tmp_path):
        graph = nx.MultiDiGraph()
        graph.add_edge(1, 2, label="l")
        csv_file_path = tmp_path / "graph.csv"
        graph_to_csv(graph, csv_file_path)

        monkeypatch.setattr(cfpq_data, "download", Mock(return_value=csv_file_path))

        expected_info = GraphInfo(2, 1, {"l"})
        actual_info = get_graph_info_by_name("name")

        assert actual_info == expected_info

    @staticmethod
    def test_two_multi_edge(monkeypatch, tmp_path):
        graph = nx.MultiDiGraph()
        graph.add_edge(1, 2, label="a")
        graph.add_edge(1, 2, label="b")
        csv_file_path = tmp_path / "graph.csv"
        graph_to_csv(graph, csv_file_path)

        monkeypatch.setattr(cfpq_data, "download", Mock(return_value=csv_file_path))

        expected_info = GraphInfo(2, 2, {"a", "b"})
        actual_info = get_graph_info_by_name("name")

        assert actual_info == expected_info


class TestCreateTwoCyclesGraph:
    @staticmethod
    def test_creates_saves(tmp_path):
        csv_file_path = tmp_path / "graph.dot"
        graph = create_two_cycles_graph(3, 3, ("a", "b"), csv_file_path)

        assert csv_file_path.exists()

        actual_graph = nx.drawing.nx_pydot.read_dot(csv_file_path)

        assert nx.is_isomorphic(actual_graph, graph, edge_match=nx.isomorphism.categorical_node_match("label", None))
