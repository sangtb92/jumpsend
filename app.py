import time

from openpyxl import load_workbook

from config import ApiConfig
from logger import Logger
from model.deal import Deal
from jump_send import login, get_requests, search

logger = Logger()


def load_out(deals):
    try:
        ids = []
        for deal in deals:
            ids.append(deal[0])
        return ids
    except Exception as e:
        logger.write_log('debug', str(e))


def get_id_saved():
    try:
        wb = load_workbook(ApiConfig.OUTPUT)
        ws = wb.active
        return ws.iter_rows()
    except Exception as e:
        logger.write_log('debug', str(e))


if __name__ == '__main__':
    token = login()
    deals = []
    for i in range(1, 6):
        ids = search(i)
        for _id in ids:
            if _id in deals:
                continue
            deals.append(_id)
            deal = Deal(id=_id)
            deal.get_details()
            deal.request(token)
            deal.save()
            print("Done {0}".format(_id))
    # # page = 1
    # # while True:
    # #     print(page)
    # #     out = False
    # #     json = get_requests(token, page=page)
    # #     deal_requests = json['data']['deal_requests']
    # #     page = json['data']['next_page']
    # #     for deal in deal_requests:
    # #         promotion_id = deal['promotion_id']
    # #         if promotion_id in a:
    # #             out = True
    # #             print(deal['coupon_code'])
    # #             print(promotion_id)
    # #     if out:
    # #         break
    # deals = list(get_id_saved())
    # print(deals)
