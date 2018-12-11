class BaseConfig:
    LOGGING_DIR = './logs/'
    IMAGES_DIR = '/Users/sangnd/PycharmProjects/untitled/images/'
    OUTPUT = '/Users/sangnd/PycharmProjects/untitled/output/jump_send.xlsx'
    OUTPUT2 = '/Users/sangnd/PycharmProjects/untitled/output/jump_send_cp.xlsx'


class ApiConfig(BaseConfig):
    SEARCH_ENDPOINT = 'https://api.jumpsend.com/api/deals?min_price=0&max_price=20&min_discount=50&max_discount=100&country_code=US&direction=desc&order_by=promotions.bumped_at&categories[]=Automotive&categories[]=Baby&categories[]=Books&categories[]=Clothing&categories[]=Electronics&categories[]=Grocery%20%26%20Gourmet%20Food2&categories[]=Health%20%26%20Personal%20Care&categories[]=Home%20Goods&categories[]=Jewelry&categories[]=Music&categories[]=Musical%20Instruments&categories[]=Office&categories[]=Patio,%20Lawn%20%26%20Garden&categories[]=Pet%20Supplies&categories[]=Shoes&categories[]=Sports%20%26%20Outdoors&categories[]=Supplements&categories[]=Toys%20%26%20Games'
    DETAIL_DEAL_ENPOINT = 'https://api.jumpsend.com/api/deal'
    DEAL_REQUEST = 'https://api.jumpsend.com/api/deal_request'
    TOKEN = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaG9wcGVyX2lkIjoxNjA3MjYsInRva2VuIjoiZmM4NjcwMDkxMmRjODgxZjFhMDU5MzBkYzFjMTUwZDEiLCJleHAiOjE1NDQ3NTM5NDEsImlhdCI6MTU0NDE0OTE0MSwiaXNzIjoianVtcHNlbmRfYXBpIiwiYXVkIjoiY2xpZW50In0.2pnvjorhhsgMBisx9L-ziX_ymY2_o4KV9_O1itA4zMI'
    ADD_PERSENT = 0.4
    MAX_PAGE = 5
    PROFIT_PERCENTAGE = 1 / 2


class JsConfig(BaseConfig):
    DEBUG = True
    LOGIN_ENDPOINT = 'https://api.jumpsend.com/api/sessions_create'
    EMAIL = 'sangnd.it@gmail.com'
    PASSWORD = 'ali33team'
    MIX_PANEL_ID = '1677233c440a2f-0c5269f085c127-35667407-13c680-1677233c4413e3'
    REQUESTED = 'https://api.jumpsend.com/api/deal_requests'
