import requests
import re
import json
from urllib.parse import urljoin

headers = {
    'authority': 'www.youtube.com',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-full-version': '"95.0.4638.54"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-platform': '"macOS"',
    'sec-ch-ua-platform-version': '"11.6.0"',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-bitness': '"64"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'service-worker-navigation-preload': 'true',
    'x-client-data': 'CI22yQEIpbbJAQjBtskBCKmdygEI4v7KAQjr8ssBCO/yywEInvnLAQjnhMwBCLWFzAEI/4XMAQjLicwBCPyKzAE=',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cookie': 'VISITOR_INFO1_LIVE=j9gfxkdSd1w; LOGIN_INFO=AFmmF2swRQIhAN8kJQLdB8gReS-wgvbetuIA62q9bJhGG5MX3oikQsWZAiB7VS8uYwFGMptr9PwVXeWD5j2hCHSw1KF-ODs-W6SIoQ:QUQ3MjNmemFRWGFfRXBjT2d3RFhIRjBBd0txak1reUE3X1J6NWF4d1UxWFl1Mkw3bjlFNGQ1UWFBWDBfanZqaWNFLWJEcG1qNWNzOEZ4S0dYUTllUTk1aGVXdzFmOS1pQmlqWjFERGRMM3RSWVA5Ul8xWWc3NEdNb2JBWmk0R0xsU1dMYk9qekRBa010QmZzNjUzUWhpME9CQnlHSjJ2aktR; HSID=ACXKNIr-wBlYlT-l7; SSID=AnpEr1rrYr3ZmNxIk; APISID=LF8SMvSJ78qzyRcH/ADXW4SCXAFVkStFqc; SAPISID=EU3Xbu3ZO_U77IlB/ALcbnFBgfzy0r_mHE; __Secure-1PAPISID=EU3Xbu3ZO_U77IlB/ALcbnFBgfzy0r_mHE; __Secure-3PAPISID=EU3Xbu3ZO_U77IlB/ALcbnFBgfzy0r_mHE; SID=DQiC_R3AJBaBBCgOMmDC4mjAJy7n3XZGRfbmZGMtVUGS9CpF7aNiTiDZf0tSTccIiAIvkA.; __Secure-1PSID=DQiC_R3AJBaBBCgOMmDC4mjAJy7n3XZGRfbmZGMtVUGS9CpFzS4GlYUpZlNgeuQSEhwPsA.; __Secure-3PSID=DQiC_R3AJBaBBCgOMmDC4mjAJy7n3XZGRfbmZGMtVUGS9CpF1GPcNzU3dRkJwkFhZtQJtg.; YSC=0gdSWvc0m3s; PREF=tz=Asia.Singapore&f6=40000000&f4=4000000; SIDCC=AJi4QfEyT4v1GYzx8QlXRzlodBOpt9fIDuiDtJwQGYzCEB4OBai_brflidQKOy9jcO7AG_bMs6s; __Secure-3PSIDCC=AJi4QfH5q68d9w6r2eNJGVKFz-y5eAVwIW3ZFm0z7gN43BMTvB2lCagD8aINPgWzZ_s2NbL6naU',
}

params = (
    ('v', 'hYBl_KSIKNM'),
    ('ab_channel', 'HugoD\xE9crypte-Actusdujour'),
)

def channelVideos(videoURL):
	# videoURL = 'https://www.youtube.com/' + channel
	# desktop browser useragent is required, otherwise youtube doesn't send the ytInitialData

	# attempt to find the data at least 3 times
	# because sometimes youtube mysteriously decides to send the bot-page for us
	for _ in range(3):
		res = requests.get('https://www.youtube.com/watch', headers=headers, params=params)
		# res = requests.get(videoURL, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/321 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36'})
		# print(res.text)

		# tear out the json initalization data found in the page
		match = re.search(r'window\["ytInitialData"\]\s*=\s*(.*);\s*window\["ytInitialPlayerResponse"\]', res.text, re.MULTILINE)
		if match:
			json_data = match.group(1)
			data = json.loads(json_data)
			# print('got data:', data)
			tabs = data['contents']['twoColumnBrowseResultsRenderer']['tabs']
			for tab in tabs:
				if tab.get('tabRenderer') is not None and tab['tabRenderer']['title'] == "Videos":
					videos_tab = tab
					break
			else:
				raise Exception('no video tab found in ytInitialData')

			video_items = videos_tab['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['gridRenderer']['items']
			videos = []
			for video_item in video_items:
				# print ('video:', video_item)

				title = video_item['gridVideoRenderer']['title']['simpleText']
				if video_item['gridVideoRenderer'].get('publishedTimeText') is not None:
					age = video_item['gridVideoRenderer']['publishedTimeText']['simpleText']
				else:
					age = '?'
				url = video_item['gridVideoRenderer']['navigationEndpoint']['webNavigationEndpointData']['url']
				link = urljoin(videoURL, url)

				# print('title:', title)
				# print('age:', age)
				# print('url:', url, link)

				# ignore videos with an unknown date
				if age != '?':
					videos.append({ 'link': link, 'title': title, 'age': age })

			return videos
		# else:
		# 	print('failed to find ytInitialData')

	raise Exception('failed to find ytInitialData')

if __name__ == "__main__":
	videos = channelVideos("https://www.youtube.com/watch?v=Np695V8lzeg")
	breakpoint()