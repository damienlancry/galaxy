import requests
from abc import ABC
import networkx as nx
import json
import re
from bs4 import BeautifulSoup

headers = {
    'authority': 'www.youtube.com',
}


class BaseCartography(ABC):
    def __init__(self, initial_node, depth):
        self.depth = depth
        self.G = nx.Graph()
        self.seen = set()
        url, title, channel = initial_node
        self.G.add_node(url, title=title, channel=channel)

    def build_layer(self):
        prev_layer = list(self.G.nodes())
        for node in prev_layer:
            if node not in self.seen:
                self.seen.add(node)
                recommended = YoutubeCartography.get_recommendations(node)
                for url, title, channel in recommended:
                    self.G.add_node(url, title=title, channel=channel)
                    self.G.add_edge(node, url)

    def build(self):
        for _ in range(self.depth):
            self.build_layer()

    def save(self, filename):
        nx.write_gexf(self.G, filename)

    def load(self, filename):
        self.G = nx.read_gexf(filename)

class YoutubeCartography(BaseCartography):

    @classmethod
    def get_node(cls, recommdendation_json):
        return cls.get_url(recommdendation_json), cls.get_title(recommdendation_json), cls.get_channel(recommdendation_json)

    @staticmethod
    def get_url(recommendation_json):
        return recommendation_json["compactVideoRenderer"]["videoId"]

    @staticmethod
    def get_title(recommendation_json):
        return recommendation_json["compactVideoRenderer"]["title"]["simpleText"]

    @staticmethod
    def get_channel(recommendation_json):
        return recommendation_json["compactVideoRenderer"]["longBylineText"]["runs"][0]["text"]

    @staticmethod
    def get_recommended(data):
        try:
            return data["contents"]["twoColumnWatchNextResults"]["secondaryResults"]["secondaryResults"]["results"][1]["itemSectionRenderer"]["contents"]
        except KeyError:
            return data["contents"]["twoColumnWatchNextResults"]["secondaryResults"]["secondaryResults"]["results"]

    @staticmethod
    def get_recommendations(url):
        response = requests.get('https://www.youtube.com/watch', headers=headers, params=(("v", url),))
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find('script',string=re.compile('ytInitialData'))
        data = data.text[:-1].replace('var ytInitialData = ','').strip()
        data = json.loads(data)
        try:
            recommendations = YoutubeCartography.get_recommended(data)
        except:
            breakpoint()
        return [YoutubeCartography.get_node(recommendation) for recommendation in  recommendations if "compactVideoRenderer" in recommendation]



if __name__ == "__main__":
    depth = 2
    initial_node = 'Np695V8lzeg', "I cracked Youtube Algorithm", "ici Amy Plant"
    ytGraph = YoutubeCartography(initial_node=initial_node, depth=depth)
    ytGraph.build()
    ytGraph.save(f'iap.{depth}.gexf')


