# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.response import Response


class ShopSpider(scrapy.Spider):
    name = 'shop'
    start_urls = ['https://mebli-lviv.com.ua/ua/index.php?route=product/search&category_id=77&search=&sub_category=true&description=true']

    def parse(self, response: Response):
        furnitures = response.xpath("//div[contains(@class, 'product-block')]")[:20]
        for furniture in furnitures:
            yield {
                'price': furniture.xpath("./div[@class='product-meta']//span[@class='special-price']/text()").get(),
                'description': furniture.xpath(".//a[@class='img']/@title").get(),
                'image': furniture.xpath(".//img/@src").get()
            }
