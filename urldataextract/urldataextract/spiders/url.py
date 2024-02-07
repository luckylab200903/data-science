from pathlib import Path

import scrapy

import openpyxl

file_path = r"C:\Users\KESHAV KUMAR SINGH\Desktop\internshala\internshala\urldataextract\urldataextract\spiders\Input.xlsx"

workbook = openpyxl.load_workbook(file_path)
sheet = workbook.worksheets[0]

websites_list = []
for row in sheet.iter_rows(min_row=2, values_only=True): 
    website = row[1]  
    websites_list.append(website)

print(len(websites_list))

workbook.close()


























from pathlib import Path
import scrapy
from scrapy.crawler import CrawlerProcess

# Initialize counter for filename
file_counter = 0

class QuotesSpider(scrapy.Spider):
    name = "websites"

    def start_requests(self):
        urls =websites_list
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        global file_counter 
        file_counter += 1  
        filename = f"blackassign{file_counter:04d}.txt"  
        with open(filename, 'w', encoding='utf-8') as f:
        
            title_content = response.css(".entry-title::text").get()
            if title_content:
                f.write(title_content.strip() + "\n\n")
        
        
            post_content = response.css(".td-post-content.tagdiv-type ::text").getall()
            if post_content:
                cleaned_content = "\n".join(line.strip() for line in post_content if line.strip())
                f.write(cleaned_content.strip())
        
        self.log(f"Saved file {filename}")

