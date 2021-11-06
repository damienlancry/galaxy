import json
import re
from typing import Dict, Tuple

import requests
from bs4 import BeautifulSoup

from galaxy.cartography.cartographer import Cartographer

headers = {
    "authority": "www.youtube.com",
}


class YoutubeCartographer(Cartographer):
    """Cartographer for YouTube."""

    @classmethod
    def get_node(cls, recommdendation_json: dict) -> Tuple[str, str, str]:
        """
        Get node from recommendation json.

        :param recommdendation_json: recommendation json
        :type recommdendation_json: dict
        :return: node
        :rtype: dict
        """
        return (
            cls.get_url(recommdendation_json),
            cls.get_title(recommdendation_json),
            cls.get_channel(recommdendation_json),
        )

    @staticmethod
    def get_url(recommendation_json: Dict) -> str:
        """
        Get url from recommendation json.

        :param recommendation_json: recommendation json
        :type recommendation_json: Dict
        :return: url
        :rtype: str
        """
        return recommendation_json["compactVideoRenderer"]["videoId"]

    @staticmethod
    def get_title(recommendation_json: Dict) -> str:
        """
        Get title from recommendation json.

        :param recommendation_json: recommendation json
        :type recommendation_json: Dict
        :return: title
        :rtype: str
        """
        return recommendation_json["compactVideoRenderer"]["title"]["simpleText"]

    @staticmethod
    def get_channel(recommendation_json: Dict) -> str:
        """
        Get channel from recommendation json.

        :param recommendation_json: recommendation json
        :type recommendation_json: Dict
        :return: channel
        :rtype: str
        """
        return recommendation_json["compactVideoRenderer"]["longBylineText"]["runs"][0][
            "text"
        ]

    @staticmethod
    def get_recommended(data):
        """
        Get recommended from data.

        :param data: data
        :type data: [type]
        :return: [description]
        :rtype: [type]
        """
        try:
            return data["contents"]["twoColumnWatchNextResults"]["secondaryResults"][
                "secondaryResults"
            ]["results"][1]["itemSectionRenderer"]["contents"]
        except KeyError:
            return data["contents"]["twoColumnWatchNextResults"]["secondaryResults"][
                "secondaryResults"
            ]["results"]

    @staticmethod
    def get_recommendations(url: str):
        """
        Get recommendations from url.

        :param url: [description]
        :type url: [type]
        :return: [description]
        :rtype: [type]
        """
        response = requests.get(
            "https://www.youtube.com/watch", headers=headers, params=(("v", url),)
        )
        soup = BeautifulSoup(response.text, "html.parser")
        data = soup.find("script", string=re.compile("ytInitialData"))
        data = data.text[:-1].replace("var ytInitialData = ", "").strip()
        data = json.loads(data)
        recommendations = YoutubeCartographer.get_recommended(data)
        return [
            YoutubeCartographer.get_node(recommendation)
            for recommendation in recommendations
            if "compactVideoRenderer" in recommendation
        ]
