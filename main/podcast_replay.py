import os
import time
from email.utils import parsedate
from datetime import datetime, timedelta
import json
from fastapi import FastAPI, HTTPException, Response
import xml.etree.ElementTree as ET
import requests

app = FastAPI()

def read_config() -> dict:
    """ Read the configuration JSON file from config/podcast-replay.json
    
    The configuration file is a JSON containing an dict with the podcast ID as key and a dict as value.
    The value has the following keys:
    - url: the podcast feed URL
    - date: the start date of the re-release in the format YYYY-MM-DD
    - rate: the number of days between re-releases
    - skip: the number of episodes to skip
    """
    working_dir = os.path.dirname(os.path.realpath(__file__))
    config_file = os.path.join(working_dir, "..", "config", "podcast-replay.json")
    
    with open(config_file, 'r') as file:
        return json.load(file)


def get_date(item: ET.Element) -> datetime:
    date_element = item.find('pubDate')
    timestamp = parsedate(date_element.text)
    return datetime.fromtimestamp(time.mktime(timestamp))


def transform_podcast(feed_str: str, podcast: dict, now: datetime=None) -> ET.Element:
    now = now or datetime.now()

    ET.register_namespace('atom',"http://www.w3.org/2005/Atom")
    ET.register_namespace('content',"http://purl.org/rss/1.0/modules/content/")
    ET.register_namespace('itunes',"http://www.itunes.com/dtds/podcast-1.0.dtd")

    feed_root = ET.fromstring(feed_str)

    # build the parent map for the XML
    parent_map = {c: p for p in feed_root.iter() for c in p}

    startdate = datetime.strptime(podcast['date'], '%Y-%m-%d')
    rate: int = podcast['rate']
    skip: int = podcast['skip']

    latestdate = datetime.now()

    # from the original feed, remove the first n episodes
    channel_element = feed_root.find('channel')

    episodes = channel_element.findall('item')
    # sort episodes by date
    episodes.sort(key=get_date)

    skipped_episodes = episodes[:skip]
    for episode in skipped_episodes:
        parent_map[episode].remove(episode)

    # for the remaining episodes in the original feed, adjust the publication date, so it seems that
    # the episodes are released as indicated in the config
    for index, episode in enumerate(episodes[skip:]):
        new_publication_date = startdate + timedelta(days=index * rate)
        if new_publication_date < now:
            pub_date_element = episode.find('pubDate')
            pub_date_element.text = new_publication_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
            latestdate = new_publication_date
        else:
            # date is in the future - remove the episode
            parent_map[episode].remove(episode)

    # update the build date
    channel_element.find('lastBuildDate').text = latestdate.strftime('%a, %d %b %Y %H:%M:%S GMT')

    # return the modified feed as XML
    return feed_root


@app.head('/podcast/{name}')
async def service_head(name: str):
    return Response(media_type="application/xml")


@app.get('/podcast/{name}')
async def service(name: str):
    """ Main entry point of the service """

    # read the configuration file
    config = read_config()

    # get the podcast
    if name not in config:
        raise HTTPException(status_code=404, detail=f'Podcast with id {name} not found')
    podcast = config[name]

    # original feed URL
    feed_url = podcast['url']
    
    # GET the feed URL via HTTP GET
    response = requests.get(feed_url)

    # get XML payload of the response
    xml_payload = response.text

    modified_feed = transform_podcast(xml_payload, podcast)
    xml_result = ET.tostring(modified_feed, xml_declaration=True, encoding="utf-8")

    return Response(content=xml_result, media_type="application/xml")
