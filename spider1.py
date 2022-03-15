import scrapy


class PrimersSpider(scrapy.Spider):
    name = "Primers"
    start_urls = ["https://www.midsouthshooterssupply.com/dept/reloading/primers"]
    custom_settings = {"FEEDS": {"primers.json": {"format": "json"}}}

    def parse(self, response):
        print("Parse called : URL : ", response.url)
        products = response.css("div#Div1.product")
        for product in products:
            yield {
                'Price': product.css("span.price span::text").get(),
                'Description': product.css("div.product-description a::text").get(),
                'Stock Status': 'No' if product.css("span.status span::text").get() == 'Out of Stock' else 'Yes',
                'Title': product.css("div.product-description a::text").get(),
                'Manufacturer': product.css("a.catalog-item-brand::text").get()
            }

        next_page = response.xpath("//*[contains(text(), 'Next')]/@href").get()
        if next_page:
            next_page_url = response.url + '?' + next_page.split('?')[1]
            print("Url found : ", next_page_url)
            yield response.follow(next_page_url, callback=self.parse)
