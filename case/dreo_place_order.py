# coding=utf-8

"""
@author: Lyle.Hong
@date: 2022/5/19 16:48
登录-下单-支付流程
"""
import time

import requests
from selenium.webdriver.common.by import By

from common.handle_db import HandleMySql


class SaveData:
    pass


class DreoPlaceOrder:
    """流程操作方法"""
    db = HandleMySql()

    def get_product(self, headers):
        """
        获取亚马逊产品库存
        :return:
        """
        url = "https://dreo-test.myshopify.com/api/2022-01/graphql.json"
        data = {
            "operationName": "QueryProductVariantQuantity",
            "variables": {
                "id": "gid://shopify/ProductVariant/42770312593635"
            },
            "query": "query QueryProductVariantQuantity($id: ID!) {\n  node(id: $id) {\n    ... on ProductVariant {\n      quantityAvailable\n      __typename\n    }\n    __typename\n  }\n}\n"
        }
        headers["x-shopify-storefront-access-token"] = "c0775b59f20c51dae115e073bd8ed3fd"
        resp = self.request_method(method="POST", headers=headers, url=url, data=data)
        return resp

    def get_customer_cart(self, headers, base_url):
        """
        获取购物车id
        :return:
        """
        cur_url = "/api/transaction/customer/cart?reloadFlag=false"
        url = base_url + cur_url
        resp = self.request_method(method="GET", headers=headers, url=url, data=None)
        setattr(SaveData, "cartNo", resp["data"]["cartNo"])
        return resp

    def active_customer(self, headers, base_url, email):
        """
        激活账号
        :return:
        """
        # 调激活接口
        cur_url = "/api/user/register/email/verify"
        url = base_url + cur_url
        self.request_method(headers, url, data={})
        # 数据库获取code码
        verifycode = self.db.search_one(
            "select v.verifycode from t_user t,t_user_verify v where t.id = v.id and email = '{}';".format(email))
        # code字段
        code = verifycode["verifycode"]
        # 再掉激活接口激活账号
        url = base_url + "/api/user/register/email/verify/code"
        data = {"code": code}
        resp = self.request_method(headers, url, data)
        return resp

    def add_shopping_card(self, headers, base_url):
        """
        添加商品至购物车
        :return:
        """
        if not getattr(SaveData, "cartNo", None):
            self.get_customer_cart(headers=headers, base_url=base_url)
            print("getattr last:", getattr(SaveData, "cartNo", None))

        url = "https://dreo-test.myshopify.com/api/2022-01/graphql.json"
        data = {
            "operationName": "checkoutLineItemsAdd",
            "variables": {
                "checkoutId": "{}".format(getattr(SaveData, "cartNo", None)),
                "lineItems": [
                    {
                        "variantId": "Z2lkOi8vc2hvcGlmeS9Qcm9kdWN0VmFyaWFudC80Mjc3MDMxMjU5MzYzNQ==",
                        "quantity": 1,
                        "customAttributes": [
                            {
                                "key": "Style",
                                "value": "Smart WiFi"
                            }
                        ]
                    }
                ]
            },
            "query": "mutation checkoutLineItemsAdd($lineItems: [CheckoutLineItemInput!]!, $checkoutId: ID!) {\n  checkoutLineItemsAdd(lineItems: $lineItems, checkoutId: $checkoutId) {\n    checkout {\n      ...Checkout\n      __typename\n    }\n    checkoutUserErrors {\n      code\n      field\n      message\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment Checkout on Checkout {\n  completedAt\n  createdAt\n  currencyCode\n  email\n  id\n  webUrl\n  shippingDiscountAllocations {\n    allocatedAmount {\n      amount\n      currencyCode\n      __typename\n    }\n    __typename\n  }\n  shippingLine {\n    ...ShippingRate\n    __typename\n  }\n  taxesIncluded\n  taxExempt\n  lineItemsSubtotalPrice {\n    amount\n    currencyCode\n    __typename\n  }\n  subtotalPriceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  totalDuties {\n    amount\n    currencyCode\n    __typename\n  }\n  totalPriceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  totalTaxV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  lineItems(first: 100) {\n    ...CheckoutLineItems\n    __typename\n  }\n  __typename\n}\n\nfragment ShippingRate on ShippingRate {\n  handle\n  priceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  title\n  __typename\n}\n\nfragment CheckoutLineItems on CheckoutLineItemConnection {\n  edges {\n    node {\n      ...CheckoutLineItem\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment CheckoutLineItem on CheckoutLineItem {\n  id\n  quantity\n  title\n  discountAllocations {\n    allocatedAmount {\n      ...MoneyV2\n      __typename\n    }\n    __typename\n  }\n  variant {\n    ...CartLineProductVariant\n    __typename\n  }\n  customAttributes {\n    key\n    value\n    __typename\n  }\n  __typename\n}\n\nfragment MoneyV2 on MoneyV2 {\n  amount\n  currencyCode\n  __typename\n}\n\nfragment CartLineProductVariant on ProductVariant {\n  availableForSale\n  compareAtPriceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  currentlyNotInStock\n  id\n  priceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  quantityAvailable\n  requiresShipping\n  selectedOptions {\n    name\n    value\n    __typename\n  }\n  sku\n  title\n  unitPrice {\n    amount\n    currencyCode\n    __typename\n  }\n  product {\n    ...Product\n    __typename\n  }\n  weight\n  weightUnit\n  image {\n    ...Image\n    __typename\n  }\n  __typename\n}\n\nfragment Product on Product {\n  availableForSale\n  compareAtPriceRange {\n    ... on ProductPriceRange {\n      maxVariantPrice {\n        ... on MoneyV2 {\n          amount\n          currencyCode\n          __typename\n        }\n        __typename\n      }\n      minVariantPrice {\n        ... on MoneyV2 {\n          amount\n          currencyCode\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  landingPage: metafield(namespace: \"product_fields\", key: \"landing_page\") {\n    ...Metafield\n    __typename\n  }\n  model: metafield(namespace: \"product_fields\", key: \"model\") {\n    ...Metafield\n    __typename\n  }\n  sellingPoints: metafield(\n    namespace: \"product_fields\"\n    key: \"product_selling_points\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  simpleDescription: metafield(namespace: \"product_fields\", key: \"description\") {\n    ...Metafield\n    __typename\n  }\n  whatIsInTheBox: metafield(\n    namespace: \"product_fields\"\n    key: \"what_is_in_the_box\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  specs: metafield(namespace: \"product_fields\", key: \"specs\") {\n    ...Metafield\n    __typename\n  }\n  faqs: metafield(namespace: \"product_fields\", key: \"faqs\") {\n    ...Metafield\n    __typename\n  }\n  manuals: metafield(namespace: \"product_fields\", key: \"manuals\") {\n    ...Metafield\n    __typename\n  }\n  amazonLink: metafield(namespace: \"product_fields\", key: \"amazon_link\") {\n    ...Metafield\n    __typename\n  }\n  description\n  descriptionHtml\n  handle\n  id\n  tags\n  productType\n  title\n  totalInventory\n  updatedAt\n  vendor\n  images(first: 100) {\n    edges {\n      node {\n        ...Image\n        transformedSrc(maxWidth: 400)\n        largeImageUrl: transformedSrc(maxWidth: 1440)\n        mediumImageUrl: transformedSrc(maxWidth: 992, crop: CENTER)\n        smallImageUrl: transformedSrc(maxWidth: 768)\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  variants(first: 100) {\n    ...ProductVariants\n    __typename\n  }\n  level_a_default_xl: metafield(\n    namespace: \"product_fields\"\n    key: \"level_a_default_xl\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_a_default_lg: metafield(\n    namespace: \"product_fields\"\n    key: \"level_a_default_lg\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_a_default_md: metafield(\n    namespace: \"product_fields\"\n    key: \"level_a_default_md\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_a_default_xs: metafield(\n    namespace: \"product_fields\"\n    key: \"level_a_default_xs\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_a_hover_xl: metafield(\n    namespace: \"product_fields\"\n    key: \"level_a_hover_xl\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_a_hover_lg: metafield(\n    namespace: \"product_fields\"\n    key: \"level_a_hover_lg\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_b_default_xl: metafield(\n    namespace: \"product_fields\"\n    key: \"level_b_default_xl\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_b_default_lg: metafield(\n    namespace: \"product_fields\"\n    key: \"level_b_default_lg\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_b_default_md: metafield(\n    namespace: \"product_fields\"\n    key: \"level_b_default_md\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_b_default_xs: metafield(\n    namespace: \"product_fields\"\n    key: \"level_b_default_xs\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_b_hover_xl: metafield(\n    namespace: \"product_fields\"\n    key: \"level_b_hover_xl\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_b_hover_lg: metafield(\n    namespace: \"product_fields\"\n    key: \"level_b_hover_lg\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  __typename\n}\n\nfragment Metafield on Metafield {\n  createdAt\n  description\n  id\n  key\n  namespace\n  type\n  updatedAt\n  value\n  __typename\n}\n\nfragment Image on Image {\n  altText\n  height\n  id\n  originalSrc\n  width\n  __typename\n}\n\nfragment ProductVariants on ProductVariantConnection {\n  edges {\n    node {\n      ...ProductVariant\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ProductVariant on ProductVariant {\n  availableForSale\n  compareAtPriceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  currentlyNotInStock\n  id\n  priceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  quantityAvailable\n  requiresShipping\n  selectedOptions {\n    name\n    value\n    __typename\n  }\n  sku\n  title\n  unitPrice {\n    amount\n    currencyCode\n    __typename\n  }\n  weight\n  weightUnit\n  image {\n    ...Image\n    __typename\n  }\n  __typename\n}\n"
        }
        return self.request_method(headers=headers, url=url, data=data)

    def add_address(self, headers, base_url):
        """
        添加默认收货地址
        :return:
        """
        cur_url = "/api/transaction/customer/address"
        url = base_url + cur_url
        data = {
            "firstName": "lytest",
            "lastName": "letest",
            "phone": "+12567157456",
            "address1": "test1111",
            "address2": "apartment2222",
            "city": "city3333",
            "country": "United States",
            "province": "New York",
            "zip": "10002",
            "isDefault": True,
            "provinceCode": "New York",
            "countryCode": "US"
        }
        return self.request_method(headers=headers, url=url, data=data)

    def create_order(self, headers, email):
        """
        shopify创建订单
        :return:
        """
        url = "https://dreo-test.myshopify.com/api/2022-01/graphql.json"
        data1 = {
            "operationName": "Cart",
            "variables": {
                "id": "{}".format(getattr(SaveData, "cartNo", None))
            },
            "query": "query Cart($id: ID!) {\n  node(id: $id) {\n    ...Checkout\n    __typename\n  }\n}\n\nfragment Checkout on Checkout {\n  completedAt\n  createdAt\n  currencyCode\n  email\n  id\n  webUrl\n  shippingDiscountAllocations {\n    allocatedAmount {\n      amount\n      currencyCode\n      __typename\n    }\n    __typename\n  }\n  shippingLine {\n    ...ShippingRate\n    __typename\n  }\n  taxesIncluded\n  taxExempt\n  lineItemsSubtotalPrice {\n    amount\n    currencyCode\n    __typename\n  }\n  subtotalPriceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  totalDuties {\n    amount\n    currencyCode\n    __typename\n  }\n  totalPriceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  totalTaxV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  lineItems(first: 100) {\n    ...CheckoutLineItems\n    __typename\n  }\n  __typename\n}\n\nfragment ShippingRate on ShippingRate {\n  handle\n  priceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  title\n  __typename\n}\n\nfragment CheckoutLineItems on CheckoutLineItemConnection {\n  edges {\n    node {\n      ...CheckoutLineItem\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment CheckoutLineItem on CheckoutLineItem {\n  id\n  quantity\n  title\n  discountAllocations {\n    allocatedAmount {\n      ...MoneyV2\n      __typename\n    }\n    __typename\n  }\n  variant {\n    ...CartLineProductVariant\n    __typename\n  }\n  customAttributes {\n    key\n    value\n    __typename\n  }\n  __typename\n}\n\nfragment MoneyV2 on MoneyV2 {\n  amount\n  currencyCode\n  __typename\n}\n\nfragment CartLineProductVariant on ProductVariant {\n  availableForSale\n  compareAtPriceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  currentlyNotInStock\n  id\n  priceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  quantityAvailable\n  requiresShipping\n  selectedOptions {\n    name\n    value\n    __typename\n  }\n  sku\n  title\n  unitPrice {\n    amount\n    currencyCode\n    __typename\n  }\n  product {\n    ...Product\n    __typename\n  }\n  weight\n  weightUnit\n  image {\n    ...Image\n    __typename\n  }\n  __typename\n}\n\nfragment Product on Product {\n  availableForSale\n  compareAtPriceRange {\n    ... on ProductPriceRange {\n      maxVariantPrice {\n        ... on MoneyV2 {\n          amount\n          currencyCode\n          __typename\n        }\n        __typename\n      }\n      minVariantPrice {\n        ... on MoneyV2 {\n          amount\n          currencyCode\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  landingPage: metafield(namespace: \"product_fields\", key: \"landing_page\") {\n    ...Metafield\n    __typename\n  }\n  model: metafield(namespace: \"product_fields\", key: \"model\") {\n    ...Metafield\n    __typename\n  }\n  sellingPoints: metafield(\n    namespace: \"product_fields\"\n    key: \"product_selling_points\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  simpleDescription: metafield(namespace: \"product_fields\", key: \"description\") {\n    ...Metafield\n    __typename\n  }\n  whatIsInTheBox: metafield(\n    namespace: \"product_fields\"\n    key: \"what_is_in_the_box\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  specs: metafield(namespace: \"product_fields\", key: \"specs\") {\n    ...Metafield\n    __typename\n  }\n  faqs: metafield(namespace: \"product_fields\", key: \"faqs\") {\n    ...Metafield\n    __typename\n  }\n  manuals: metafield(namespace: \"product_fields\", key: \"manuals\") {\n    ...Metafield\n    __typename\n  }\n  amazonLink: metafield(namespace: \"product_fields\", key: \"amazon_link\") {\n    ...Metafield\n    __typename\n  }\n  description\n  descriptionHtml\n  handle\n  id\n  tags\n  productType\n  title\n  totalInventory\n  updatedAt\n  vendor\n  images(first: 100) {\n    edges {\n      node {\n        ...Image\n        transformedSrc(maxWidth: 400)\n        largeImageUrl: transformedSrc(maxWidth: 1440)\n        mediumImageUrl: transformedSrc(maxWidth: 992, crop: CENTER)\n        smallImageUrl: transformedSrc(maxWidth: 768)\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  variants(first: 100) {\n    ...ProductVariants\n    __typename\n  }\n  level_a_default_xl: metafield(\n    namespace: \"product_fields\"\n    key: \"level_a_default_xl\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_a_default_lg: metafield(\n    namespace: \"product_fields\"\n    key: \"level_a_default_lg\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_a_default_md: metafield(\n    namespace: \"product_fields\"\n    key: \"level_a_default_md\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_a_default_xs: metafield(\n    namespace: \"product_fields\"\n    key: \"level_a_default_xs\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_a_hover_xl: metafield(\n    namespace: \"product_fields\"\n    key: \"level_a_hover_xl\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_a_hover_lg: metafield(\n    namespace: \"product_fields\"\n    key: \"level_a_hover_lg\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_b_default_xl: metafield(\n    namespace: \"product_fields\"\n    key: \"level_b_default_xl\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_b_default_lg: metafield(\n    namespace: \"product_fields\"\n    key: \"level_b_default_lg\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_b_default_md: metafield(\n    namespace: \"product_fields\"\n    key: \"level_b_default_md\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_b_default_xs: metafield(\n    namespace: \"product_fields\"\n    key: \"level_b_default_xs\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_b_hover_xl: metafield(\n    namespace: \"product_fields\"\n    key: \"level_b_hover_xl\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_b_hover_lg: metafield(\n    namespace: \"product_fields\"\n    key: \"level_b_hover_lg\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  __typename\n}\n\nfragment Metafield on Metafield {\n  createdAt\n  description\n  id\n  key\n  namespace\n  type\n  updatedAt\n  value\n  __typename\n}\n\nfragment Image on Image {\n  altText\n  height\n  id\n  originalSrc\n  width\n  __typename\n}\n\nfragment ProductVariants on ProductVariantConnection {\n  edges {\n    node {\n      ...ProductVariant\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ProductVariant on ProductVariant {\n  availableForSale\n  compareAtPriceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  currentlyNotInStock\n  id\n  priceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  quantityAvailable\n  requiresShipping\n  selectedOptions {\n    name\n    value\n    __typename\n  }\n  sku\n  title\n  unitPrice {\n    amount\n    currencyCode\n    __typename\n  }\n  weight\n  weightUnit\n  image {\n    ...Image\n    __typename\n  }\n  __typename\n}\n"
        }
        data2 = {
            "operationName": "CheckoutCreate",
            "variables": {
                "input": {
                    "email": "{}".format(email),
                    "shippingAddress": {
                        "address1": "test1111",
                        "address2": "apartment2222",
                        "city": "city3333",
                        "company": "",
                        "country": "United States",
                        "firstName": "lytest",
                        "lastName": "letest",
                        "phone": "+12567157456",
                        "province": "NY",
                        "zip": "10002"
                    },
                    "customAttributes": [
                        {
                            "key": "email",
                            "value": "{}".format(email)
                        }
                    ],
                    "lineItems": [
                        {
                            "quantity": 1,
                            "variantId": "Z2lkOi8vc2hvcGlmeS9Qcm9kdWN0VmFyaWFudC80Mjc3MDMxMjU5MzYzNQ=="
                        }
                    ]
                }
            },
            "query": "mutation CheckoutCreate($input: CheckoutCreateInput!, $queueToken: String) {\n  checkoutCreate(input: $input, queueToken: $queueToken) {\n    checkout {\n      ...Checkout\n      __typename\n    }\n    checkoutUserErrors {\n      code\n      field\n      message\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment Checkout on Checkout {\n  completedAt\n  createdAt\n  currencyCode\n  email\n  id\n  webUrl\n  shippingDiscountAllocations {\n    allocatedAmount {\n      amount\n      currencyCode\n      __typename\n    }\n    __typename\n  }\n  shippingLine {\n    ...ShippingRate\n    __typename\n  }\n  taxesIncluded\n  taxExempt\n  lineItemsSubtotalPrice {\n    amount\n    currencyCode\n    __typename\n  }\n  subtotalPriceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  totalDuties {\n    amount\n    currencyCode\n    __typename\n  }\n  totalPriceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  totalTaxV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  lineItems(first: 100) {\n    ...CheckoutLineItems\n    __typename\n  }\n  __typename\n}\n\nfragment ShippingRate on ShippingRate {\n  handle\n  priceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  title\n  __typename\n}\n\nfragment CheckoutLineItems on CheckoutLineItemConnection {\n  edges {\n    node {\n      ...CheckoutLineItem\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment CheckoutLineItem on CheckoutLineItem {\n  id\n  quantity\n  title\n  discountAllocations {\n    allocatedAmount {\n      ...MoneyV2\n      __typename\n    }\n    __typename\n  }\n  variant {\n    ...CartLineProductVariant\n    __typename\n  }\n  customAttributes {\n    key\n    value\n    __typename\n  }\n  __typename\n}\n\nfragment MoneyV2 on MoneyV2 {\n  amount\n  currencyCode\n  __typename\n}\n\nfragment CartLineProductVariant on ProductVariant {\n  availableForSale\n  compareAtPriceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  currentlyNotInStock\n  id\n  priceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  quantityAvailable\n  requiresShipping\n  selectedOptions {\n    name\n    value\n    __typename\n  }\n  sku\n  title\n  unitPrice {\n    amount\n    currencyCode\n    __typename\n  }\n  product {\n    ...Product\n    __typename\n  }\n  weight\n  weightUnit\n  image {\n    ...Image\n    __typename\n  }\n  __typename\n}\n\nfragment Product on Product {\n  availableForSale\n  compareAtPriceRange {\n    ... on ProductPriceRange {\n      maxVariantPrice {\n        ... on MoneyV2 {\n          amount\n          currencyCode\n          __typename\n        }\n        __typename\n      }\n      minVariantPrice {\n        ... on MoneyV2 {\n          amount\n          currencyCode\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  landingPage: metafield(namespace: \"product_fields\", key: \"landing_page\") {\n    ...Metafield\n    __typename\n  }\n  model: metafield(namespace: \"product_fields\", key: \"model\") {\n    ...Metafield\n    __typename\n  }\n  sellingPoints: metafield(\n    namespace: \"product_fields\"\n    key: \"product_selling_points\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  simpleDescription: metafield(namespace: \"product_fields\", key: \"description\") {\n    ...Metafield\n    __typename\n  }\n  whatIsInTheBox: metafield(\n    namespace: \"product_fields\"\n    key: \"what_is_in_the_box\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  specs: metafield(namespace: \"product_fields\", key: \"specs\") {\n    ...Metafield\n    __typename\n  }\n  faqs: metafield(namespace: \"product_fields\", key: \"faqs\") {\n    ...Metafield\n    __typename\n  }\n  manuals: metafield(namespace: \"product_fields\", key: \"manuals\") {\n    ...Metafield\n    __typename\n  }\n  amazonLink: metafield(namespace: \"product_fields\", key: \"amazon_link\") {\n    ...Metafield\n    __typename\n  }\n  description\n  descriptionHtml\n  handle\n  id\n  tags\n  productType\n  title\n  totalInventory\n  updatedAt\n  vendor\n  images(first: 100) {\n    edges {\n      node {\n        ...Image\n        transformedSrc(maxWidth: 400)\n        largeImageUrl: transformedSrc(maxWidth: 1440)\n        mediumImageUrl: transformedSrc(maxWidth: 992, crop: CENTER)\n        smallImageUrl: transformedSrc(maxWidth: 768)\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  variants(first: 100) {\n    ...ProductVariants\n    __typename\n  }\n  level_a_default_xl: metafield(\n    namespace: \"product_fields\"\n    key: \"level_a_default_xl\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_a_default_lg: metafield(\n    namespace: \"product_fields\"\n    key: \"level_a_default_lg\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_a_default_md: metafield(\n    namespace: \"product_fields\"\n    key: \"level_a_default_md\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_a_default_xs: metafield(\n    namespace: \"product_fields\"\n    key: \"level_a_default_xs\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_a_hover_xl: metafield(\n    namespace: \"product_fields\"\n    key: \"level_a_hover_xl\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_a_hover_lg: metafield(\n    namespace: \"product_fields\"\n    key: \"level_a_hover_lg\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_b_default_xl: metafield(\n    namespace: \"product_fields\"\n    key: \"level_b_default_xl\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_b_default_lg: metafield(\n    namespace: \"product_fields\"\n    key: \"level_b_default_lg\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_b_default_md: metafield(\n    namespace: \"product_fields\"\n    key: \"level_b_default_md\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_b_default_xs: metafield(\n    namespace: \"product_fields\"\n    key: \"level_b_default_xs\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_b_hover_xl: metafield(\n    namespace: \"product_fields\"\n    key: \"level_b_hover_xl\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_b_hover_lg: metafield(\n    namespace: \"product_fields\"\n    key: \"level_b_hover_lg\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  __typename\n}\n\nfragment Metafield on Metafield {\n  createdAt\n  description\n  id\n  key\n  namespace\n  type\n  updatedAt\n  value\n  __typename\n}\n\nfragment Image on Image {\n  altText\n  height\n  id\n  originalSrc\n  width\n  __typename\n}\n\nfragment ProductVariants on ProductVariantConnection {\n  edges {\n    node {\n      ...ProductVariant\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ProductVariant on ProductVariant {\n  availableForSale\n  compareAtPriceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  currentlyNotInStock\n  id\n  priceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  quantityAvailable\n  requiresShipping\n  selectedOptions {\n    name\n    value\n    __typename\n  }\n  sku\n  title\n  unitPrice {\n    amount\n    currencyCode\n    __typename\n  }\n  weight\n  weightUnit\n  image {\n    ...Image\n    __typename\n  }\n  __typename\n}\n"
        }

        self.request_method(headers=headers, url=url, data=data1)
        resp = self.request_method(headers=headers, url=url, data=data2)
        id = resp["data"]["checkoutCreate"]["checkout"]["id"]
        data3 = {
            "operationName": "CheckoutShippingLineUpdate",
            "variables": {
                "checkoutId": "{}".format(id),
                "shippingRateHandle": "Expedited"
            },
            "query": "mutation CheckoutShippingLineUpdate($checkoutId: ID!, $shippingRateHandle: String!) {\n  checkoutShippingLineUpdate(\n    checkoutId: $checkoutId\n    shippingRateHandle: $shippingRateHandle\n  ) {\n    checkout {\n      ...Checkout\n      __typename\n    }\n    checkoutUserErrors {\n      code\n      field\n      message\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment Checkout on Checkout {\n  completedAt\n  createdAt\n  currencyCode\n  email\n  id\n  webUrl\n  shippingDiscountAllocations {\n    allocatedAmount {\n      amount\n      currencyCode\n      __typename\n    }\n    __typename\n  }\n  shippingLine {\n    ...ShippingRate\n    __typename\n  }\n  taxesIncluded\n  taxExempt\n  lineItemsSubtotalPrice {\n    amount\n    currencyCode\n    __typename\n  }\n  subtotalPriceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  totalDuties {\n    amount\n    currencyCode\n    __typename\n  }\n  totalPriceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  totalTaxV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  lineItems(first: 100) {\n    ...CheckoutLineItems\n    __typename\n  }\n  __typename\n}\n\nfragment ShippingRate on ShippingRate {\n  handle\n  priceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  title\n  __typename\n}\n\nfragment CheckoutLineItems on CheckoutLineItemConnection {\n  edges {\n    node {\n      ...CheckoutLineItem\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment CheckoutLineItem on CheckoutLineItem {\n  id\n  quantity\n  title\n  discountAllocations {\n    allocatedAmount {\n      ...MoneyV2\n      __typename\n    }\n    __typename\n  }\n  variant {\n    ...CartLineProductVariant\n    __typename\n  }\n  customAttributes {\n    key\n    value\n    __typename\n  }\n  __typename\n}\n\nfragment MoneyV2 on MoneyV2 {\n  amount\n  currencyCode\n  __typename\n}\n\nfragment CartLineProductVariant on ProductVariant {\n  availableForSale\n  compareAtPriceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  currentlyNotInStock\n  id\n  priceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  quantityAvailable\n  requiresShipping\n  selectedOptions {\n    name\n    value\n    __typename\n  }\n  sku\n  title\n  unitPrice {\n    amount\n    currencyCode\n    __typename\n  }\n  product {\n    ...Product\n    __typename\n  }\n  weight\n  weightUnit\n  image {\n    ...Image\n    __typename\n  }\n  __typename\n}\n\nfragment Product on Product {\n  availableForSale\n  compareAtPriceRange {\n    ... on ProductPriceRange {\n      maxVariantPrice {\n        ... on MoneyV2 {\n          amount\n          currencyCode\n          __typename\n        }\n        __typename\n      }\n      minVariantPrice {\n        ... on MoneyV2 {\n          amount\n          currencyCode\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  landingPage: metafield(namespace: \"product_fields\", key: \"landing_page\") {\n    ...Metafield\n    __typename\n  }\n  model: metafield(namespace: \"product_fields\", key: \"model\") {\n    ...Metafield\n    __typename\n  }\n  sellingPoints: metafield(\n    namespace: \"product_fields\"\n    key: \"product_selling_points\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  simpleDescription: metafield(namespace: \"product_fields\", key: \"description\") {\n    ...Metafield\n    __typename\n  }\n  whatIsInTheBox: metafield(\n    namespace: \"product_fields\"\n    key: \"what_is_in_the_box\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  specs: metafield(namespace: \"product_fields\", key: \"specs\") {\n    ...Metafield\n    __typename\n  }\n  faqs: metafield(namespace: \"product_fields\", key: \"faqs\") {\n    ...Metafield\n    __typename\n  }\n  manuals: metafield(namespace: \"product_fields\", key: \"manuals\") {\n    ...Metafield\n    __typename\n  }\n  amazonLink: metafield(namespace: \"product_fields\", key: \"amazon_link\") {\n    ...Metafield\n    __typename\n  }\n  description\n  descriptionHtml\n  handle\n  id\n  tags\n  productType\n  title\n  totalInventory\n  updatedAt\n  vendor\n  images(first: 100) {\n    edges {\n      node {\n        ...Image\n        transformedSrc(maxWidth: 400)\n        largeImageUrl: transformedSrc(maxWidth: 1440)\n        mediumImageUrl: transformedSrc(maxWidth: 992, crop: CENTER)\n        smallImageUrl: transformedSrc(maxWidth: 768)\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  variants(first: 100) {\n    ...ProductVariants\n    __typename\n  }\n  level_a_default_xl: metafield(\n    namespace: \"product_fields\"\n    key: \"level_a_default_xl\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_a_default_lg: metafield(\n    namespace: \"product_fields\"\n    key: \"level_a_default_lg\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_a_default_md: metafield(\n    namespace: \"product_fields\"\n    key: \"level_a_default_md\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_a_default_xs: metafield(\n    namespace: \"product_fields\"\n    key: \"level_a_default_xs\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_a_hover_xl: metafield(\n    namespace: \"product_fields\"\n    key: \"level_a_hover_xl\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_a_hover_lg: metafield(\n    namespace: \"product_fields\"\n    key: \"level_a_hover_lg\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_b_default_xl: metafield(\n    namespace: \"product_fields\"\n    key: \"level_b_default_xl\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_b_default_lg: metafield(\n    namespace: \"product_fields\"\n    key: \"level_b_default_lg\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_b_default_md: metafield(\n    namespace: \"product_fields\"\n    key: \"level_b_default_md\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_b_default_xs: metafield(\n    namespace: \"product_fields\"\n    key: \"level_b_default_xs\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_b_hover_xl: metafield(\n    namespace: \"product_fields\"\n    key: \"level_b_hover_xl\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  level_b_hover_lg: metafield(\n    namespace: \"product_fields\"\n    key: \"level_b_hover_lg\"\n  ) {\n    ...Metafield\n    __typename\n  }\n  __typename\n}\n\nfragment Metafield on Metafield {\n  createdAt\n  description\n  id\n  key\n  namespace\n  type\n  updatedAt\n  value\n  __typename\n}\n\nfragment Image on Image {\n  altText\n  height\n  id\n  originalSrc\n  width\n  __typename\n}\n\nfragment ProductVariants on ProductVariantConnection {\n  edges {\n    node {\n      ...ProductVariant\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ProductVariant on ProductVariant {\n  availableForSale\n  compareAtPriceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  currentlyNotInStock\n  id\n  priceV2 {\n    amount\n    currencyCode\n    __typename\n  }\n  quantityAvailable\n  requiresShipping\n  selectedOptions {\n    name\n    value\n    __typename\n  }\n  sku\n  title\n  unitPrice {\n    amount\n    currencyCode\n    __typename\n  }\n  weight\n  weightUnit\n  image {\n    ...Image\n    __typename\n  }\n  __typename\n}\n"
        }
        resp = self.request_method(headers=headers, url=url, data=data3)
        web_url = resp["data"]["checkoutShippingLineUpdate"]["checkout"]["webUrl"]
        checkout_url = web_url.split("/")[-1]
        return checkout_url

    def checkout_order(self, headers, checkout_url):
        """
        检查更新订单order
        :return:
        """
        url = "https://dreo-test.myshopify.com/api/2022-01/graphql.json"
        headers["x-shopify-storefront-access-token"] = "c0775b59f20c51dae115e073bd8ed3fd"
        data = {"operationName": "Checkout", "variables": {
            "id": "gid://shopify/Checkout/{}".format(checkout_url)},
                "query": "query Checkout($id: ID!) {\n  node(id: $id) {\n    ... on Checkout {\n      ...SimpleCheckout\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment SimpleCheckout on Checkout {\n  id\n  ready\n  orderStatusUrl\n  webUrl\n  email\n  order {\n    name\n    orderNumber\n    statusUrl\n    id\n    lineItems(first: 20) {\n      edges {\n        cursor\n        node {\n          quantity\n          title\n          discountAllocations {\n            allocatedAmount {\n              ...MoneyV2\n              __typename\n            }\n            __typename\n          }\n          variant {\n            id\n            sku\n            priceV2 {\n              ...MoneyV2\n              __typename\n            }\n            product {\n              productType\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    totalPriceV2 {\n      ...MoneyV2\n      __typename\n    }\n    totalTaxV2 {\n      ...MoneyV2\n      __typename\n    }\n    totalShippingPriceV2 {\n      ...MoneyV2\n      __typename\n    }\n    totalRefundedV2 {\n      ...MoneyV2\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment MoneyV2 on MoneyV2 {\n  amount\n  currencyCode\n  __typename\n}\n"}
        resp = self.request_method(headers=headers, url=url, data=data)
        web_url = resp["data"]["node"]["webUrl"]
        return web_url

    def payment(self, headers):
        """
        付款(暂未实现)
        :return:
        """
        url = "https://deposit.us.shopifycs.com/sessions"
        data = {"credit_card": {"number": "1", "name": "lely", "month": 11, "year": 2022, "verification_value": "111"},
                "payment_session_scope": "dreo-test.myshopify.com"}
        self.request_method(headers=headers, url=url, data=data)

    def payment_order(self, url):
        """
        webdriver 付款
        :return:
        """
        from selenium import webdriver
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.implicitly_wait(15)
        driver.get(url)
        el = driver.find_element(By.XPATH,
                                 '//*[@class="card-fields-iframe" and @title="Field container for: Card number"]')
        driver.switch_to.frame(el)
        driver.find_element(By.XPATH, '//*[@id="number"]').send_keys(1)
        driver.switch_to.parent_frame()
        el2 = driver.find_element(By.XPATH,
                                  '//*[@class="card-fields-iframe" and @title="Field container for: Name on card"]')
        driver.switch_to.frame(el2)
        driver.find_element(By.XPATH, '//*[@id="name" and @data-current-field="name"]').send_keys("lyle")
        driver.switch_to.parent_frame()
        el3 = driver.find_element(By.XPATH,
                                  '//*[@class="card-fields-iframe" and @title="Field container for: Expiration date (MM / YY)"]')
        driver.switch_to.frame(el3)
        driver.find_element(By.XPATH, '//*[@id="expiry"]').send_keys("11/")
        driver.find_element(By.XPATH, '//*[@id="expiry"]').send_keys("22")
        driver.switch_to.parent_frame()
        el4 = driver.find_element(By.XPATH,
                                  '//*[@class="card-fields-iframe" and @title="Field container for: Security code"]')
        driver.switch_to.frame(el4)
        driver.find_element(By.XPATH,
                            '//*[@id="verification_value" and @data-current-field="verification_value"]').send_keys(
            "111")
        # 滚动条
        driver.switch_to.default_content()
        js = "window.scrollTo(0,10000)"
        driver.execute_script(js)
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="continue_button"]').click()
        time.sleep(10)

    def self_order(self, base_url, headers):
        """
        校验下单支付是否成功
        :return:
        """
        cur_url = "/api/transaction/order/page/self"
        url = base_url + cur_url
        return self.request_method(headers=headers, url=url, data=None, method="GET")

    @staticmethod
    def request_method(headers, url, data, method="POST"):
        """
        发送请求
        :return:
        """
        response = requests.request(method=method, url=url, headers=headers, json=data)
        resp = response.json()
        return resp
