import requests
import os
import shutil
import time
from openpyxl import load_workbook
from config import ApiConfig
from logger import Logger

logger = Logger()


class Deal:
    PENDING = 'pending'

    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs.pop('id', None)
        if 'title' in kwargs:
            self.title = kwargs.pop('title', None)
        if 'price' in kwargs:
            self.price = kwargs.pop('price', None)
        if 'promotion_price' in kwargs:
            self.promotion_price = kwargs.pop('promotion_price', None)
        if 'discount' in kwargs:
            self.discount = kwargs.pop('discount', None)
        if 'shipment_method' in kwargs:
            self.shipment_method = kwargs.pop('shipment_method', None)
        if 'estimated_shipping_cost' in kwargs:
            self.estimated_shipping_cost = kwargs.pop('estimated_shipping_cost', None)
        if 'expire_date' in kwargs:
            self.expire_date = kwargs.pop('expire_date', None)
        if 'amazon_url' in kwargs:
            self.amazon_url = kwargs.pop('amazon_url', None)
        if 'time_remaining' in kwargs:
            self.time_remaining = kwargs.pop('time_remaining', None)
        if 'image_path' in kwargs:
            self.image_path = kwargs.pop('image_path', None)
        if 'sell_price' in kwargs:
            self.sell_price = kwargs.pop('sell_price', None)
        if 'request_status' in kwargs:
            self.request_status = kwargs.pop('request_status', None)
        else:
            self.request_status = self.PENDING
        if 'coupon_code' in kwargs:
            self.coupon_code = kwargs.pop('coupon_code', None)
        else:
            self.coupon_code = ""
        if 'profit' in kwargs:
            self.profit = kwargs.pop('profit', None)
        else:
            self.profit = 0

    def __create_img_dir__(self):
        try:
            file_path = ApiConfig.IMAGES_DIR + str(self.id)
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            return file_path
        except OSError as e:
            logger.write_log("DEBUG", str(e))

    def __get_img__(self, url):
        try:
            file_name = self.image_path + "/" + url.split("/")[-1]
            response = requests.get(url, stream=True)
            with open(file_name, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
        except Exception as e:
            logger.write_log("DEBUG", str(e))

    def __get_expire_time__(self):
        time_remaining = self.time_remaining.split(" ")
        day = time_remaining[0]
        hours = int(time_remaining[2])
        minutes = int(time_remaining[4])
        time_remaining_epoch = (int(day) * 24 * 60 * 60 + int(hours) * 60 * 60 + int(minutes) * 60)
        now = time.time()
        expire_epoch = now + time_remaining_epoch
        expire_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expire_epoch))
        return expire_time

    def __to_array_(self):
        return [self.id, self.title, self.price, self.promotion_price, self.sell_price, self.discount,
                self.shipment_method, self.estimated_shipping_cost, self.profit, self.amazon_url, self.image_path,
                self.expire_date,
                self.time_remaining, self.request_status, self.coupon_code]

    def __get_sell_price__(self):
        return ApiConfig.PROFIT_PERCENTAGE * (
            self.price - 100 * self.promotion_price / 85) + 100 * self.promotion_price / 85

    def __get_profit__(self):
        return self.sell_price - (0.15 * self.sell_price + self.promotion_price)

    def get_details(self):
        try:
            payload = {'promotion_id': self.id}
            r = requests.get(ApiConfig.DETAIL_DEAL_ENPOINT, params=payload)
            data = r.json()['data']
            deal = data['deal']
            self.title = deal['title']
            self.price = float(deal['price'])
            self.promotion_price = float(deal['promotion_price'])
            self.discount = deal['discount']
            self.shipment_method = deal['shipment_method']
            self.estimated_shipping_cost = deal['estimated_shipping_cost']
            self.time_remaining = deal['time_remaining']
            self.amazon_url = deal['amazon_url']
            self.expire_date = self.__get_expire_time__()
            self.sell_price = round(self.__get_sell_price__(), 2)
            self.profit = round(self.__get_profit__(), 2)
            img_urls = deal['additional_images']
            img_urls.append(deal['amazon_image_url'])
            img_dir = self.__create_img_dir__()
            self.image_path = img_dir
            for url in img_urls:
                self.__get_img__(url)
        except Exception as e:
            logger.write_log("DEBUG", str(e))

    def request(self, token):
        try:
            headers = {'Authorization': 'Bearer {0}'.format(token)}
            payload = {'promotion_id': self.id}
            r = requests.post(ApiConfig.DEAL_REQUEST, headers=headers, data=payload)
            if r.status_code == 200:
                logger.write_log("INFO", '{0} Request succeed!'.format(self.id))
                return 1
            else:
                logger.write_log("WARNING", 'Item {0} have not request succeed!'.format(self.id))
                return 0
        except Exception as e:
            logger.write_log("DEBUG", str(e))
            return -1

    def save(self, file=ApiConfig.OUTPUT):
        try:
            wb = load_workbook(file)
            ws = wb.active
            ws.append(self.__to_array_())
            wb.save(filename=file)
        except Exception as e:
            logger.write_log('debug', str(e))
