from abc import ABC, abstractmethod
from typing import Set, Tuple

import networkx as nx


class Cartographer(ABC):
    """Base Cartographer Class."""

    def __init__(self, initial_node: Tuple[str, str, str], depth: int):
        """
        Initialize instance of Cartographer class.

        :param initial_node: [description]
        :type initial_node:
        :param depth: [description]
        :type depth: [type]
        """
        self.depth = depth
        self.G = nx.Graph()
        self.seen: Set[str] = set()
        url, _, channel = initial_node
        self.queue = [(url, channel)]
        self.G.add_node(channel)

    def build_layer(self):
        """Build a layer of the graph."""
        prev_layer = list(self.G.nodes())
        for node in prev_layer:
            if node not in self.seen:
                self.seen.add(node)
                recommended = self.get_recommendations(node)
                for url, title, channel in recommended:
                    self.G.add_node(url, title=title, channel=channel)
                    self.G.add_edge(node, url)

    def build(self):
        """Build the graph."""
        for _ in range(self.depth):
            self.build_layer()

    def save(self, filename: str):
        """Save the graph in gexf format.

        :param filename: name of the file to save the graph
        :type filename: str
        """
        nx.write_gexf(self.G, filename)

    def load(self, filename: str):
        """
        Load the graph from a gexf file.

        :param filename: name of the file to load the graph
        :type filename: str
        """
        self.G = nx.read_gexf(filename)

    @classmethod
    @abstractmethod
    def get_recommendations(node):
        """Get recommendations for a node.

        :param node: node to get recommendations for
        :type node:
        :return: list of recommendations
        :rtype: list
        """
        raise NotImplementedError
