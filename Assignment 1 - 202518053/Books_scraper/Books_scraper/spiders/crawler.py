import scrapy

from ..items import BooksScraperItem

class AssignmentSpider(scrapy.Spider):
    name = 'Books'
    
    start_urls = [
        'https://books.toscrape.com/'
    ]
    
    def parse(self,response):
        
        all_book_div = response.css('article.product_pod')
        
        items = BooksScraperItem()
        
        for book in all_book_div:
            book_title =  book.css('h3 a::attr(title)').get()
            book_rating = book.css('p.star-rating::attr(class)').re_first(r'star-rating (\w+)')
            book_price = book.css('p.price_color::text').get()
            book_instock = book.css('p.instock.availability::text').getall()

            items['book_title'] = book_title
            items['book_rating'] = book_rating
            items['book_price'] = book_price
            items['book_instock'] = book_instock
            
            yield items
            
        next_page = response.css('li.next a::attr(href)').get()
        
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)