import time

from openpyxl import load_workbook

from config import ApiConfig
from logger import Logger
from model.deal import Deal
from jump_send import login, get_requests, search

logger = Logger()


def get_deals_requested(token):
    page = 1
    result = []
    while page is not None:
        json = get_requests(token, page=page)
        deal_requests = json['data']['deal_requests']
        page = json['data']['next_page']
        for deal in deal_requests:
            promotion_id = deal['promotion_id']
            coupon_code = deal['coupon_code']
            if coupon_code is not None:
                result.append((promotion_id, coupon_code))
        time.sleep(2)
    return result


def request_deal(max_page, token):
    for i in range(1, max_page):
        ids = search(i)
        for _id in ids:
            deal = Deal(id=_id)
            deal.request(token)
            time.sleep(1)
            print("Done {0}".format(_id))


def save_deal(deals):
    for d in deals:
        print("Start for id {0}".format(d[0]))
        id = d[0]
        coupon = d[1]
        deal = Deal(id=id, coupon_code=coupon)
        deal.get_details()
        deal.request(token)
        deal.save(ApiConfig.OUTPUT2)


if __name__ == '__main__':
    # Step1: Login to get token
    # Step2: Send request to approve and get code
    # Step3: Send request to get deals were approved
    # Step4: From deals approved send request to get details
    # """Step-1"""
    token = login()
    # """Step-2"""
    request_deal(10, token)
    # """Step-3"""
    deals = get_deals_requested(token)
    # """Step-4"""
    save_deal(deals)
