import requests
import yaml

from config import ApiConfig
from logger import Logger

logger = Logger()


def read_conf():
    try:
        with open("conf.yaml", "r") as conf:
            try:
                configs = yaml.load(conf)
                for key, value in configs.items():
                    print(key, value)
                logger.write_log("info", 'Load configuration succeed!')
            except yaml.YAMLError as exc:
                logger.write_log('debug', exc)
    except Exception as e:
        logger.write_log('debug', str(e.__str__()))


def search(page, search_key=None):
    try:
        ids = []
        payload = {'page': page, "search": search_key}
        r = requests.get(ApiConfig.SEARCH_ENDPOINT, params=payload)
        data = r.json()['data']
        deals = data['deals']
        for deal in deals:
            ids.append(deal['id'])
        return ids
    except Exception as e:
        logger.write_log("DEBUG", str(e))
        return None
