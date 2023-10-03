from werkzeug.routing import Rule

import config
from app import app


app.url_rule_class = lambda path, **options: Rule(config.URL_PREFIX + path, **options)


PRODUCTS = '/products/'
PRODUCT_CREATE = '/products/create/'
SINGLE_PRODUCT = '/products/{product_id}'
UPDATE_PRODUCT = '/products/{product_id}'
INVENTORY_STATUS = '/inventory/status/'
UPDATE_PRODUCT_INVENTORY = '/inventory/update/{product_id}'
INVENTORY_TRACK_HISTORY = '/inventory-history'
CREATE_SALE = '/sales/create'
GET_SALES = '/sales/'
ANALYZE_REVENUE = '/revenue/analysis/'
REVENUE_COMPARISON = '/revenue/comparison/'
SALES_FILTER= '/sales/filter/'
CREATE_CATEGORY = '/category/create'
GET_CATEGORIES = '/categories/'
UPDATE_CATEGORY = '/category/{category_id}'
