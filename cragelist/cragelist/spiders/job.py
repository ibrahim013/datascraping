# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class JobSpider(scrapy.Spider):
    name = 'jumia'
    allowed_domains = ['jumia.com.ng']
    start_urls = ['https://www.jumia.com.ng/phones-tablets/']

    def parse(self, response):
        jobs = response.xpath('//div[@class="sku -gallery"]')
        for job in jobs:
            title = job.xpath('a[@class="link"]/h2[@class="title"]/span[@class="name"]/text()').extract_first()
            brand = job.xpath('a[@class="link"]/h2[@class="title"]/span[@class="brand "]/text()').extract_first()
            price = job.xpath('a[@class="link"]/div[@class="price-container clearfix"]/span[@class="price-box ri"]/span[@class="price "]/span[2]/text()').extract_first()
            absolute_url = job.xpath('a/@href').extract_first()
            yield Request(absolute_url, callback =self.parse_page, meta={'URL': absolute_url, 'Title': title, 'Brand': brand, 'Price':price})
        
        absolute_next_url = response.xpath('//section[@class="pagination"]/ul[@class="osh-pagination -horizontal"]/li[@class="item"]/a[@title="Next"]/@href').extract_first()
        
        yield Request(absolute_next_url, callback = self.parse)
    
    def parse_page(self, response):
        url = response.meta.get('URL')
        title = response.meta.get('Title')
        brand = response.meta.get('Brand')
        price = response.meta.get('Price')

        reviews = response.xpath('//div[@class="reviews"]')

        for review in reviews:
            allreview = review.xpath('article[@class="card-desktop -ratingReview"]/div[@class="by"]/address[@class="author word-wrap"]/text()').extract_first()
            
        yield{'URL': url, 'Title': title, 'Brand': brand, 'Price': price, 'Reviews':allreview}
