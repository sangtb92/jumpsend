import requests
import yaml

from config import ApiConfig, JsConfig
from logger import Logger

logger = Logger()


def read_conf():
    try:
        with open("conf.yamld", "r") as conf:
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


def login():
    try:
        payload = {
            'email': JsConfig.EMAIL,
            'mixpanel_id': JsConfig.MIX_PANEL_ID,
            'password': JsConfig.PASSWORD
        }
        r = requests.post(JsConfig.LOGIN_ENDPOINT, data=payload)
        return r.json()['data']['access_token']
    except Exception as e:
        logger.write_log("DEBUG", str(e))
        return None


def get_requests(token, show_archived=False, page=1):
    try:
        headers = {
            'Authorization': 'Bearer {0}'.format(token)
        }
        payload = {'show_archived': show_archived, 'page': page, 'promotion_id': 200935}
        r = requests.get(JsConfig.REQUESTED, headers=headers, params=payload)
        return r.json()
    except Exception as e:
        logger.write_log("DEBUG", str(e))
        return None
