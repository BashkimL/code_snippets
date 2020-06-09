# -*- coding: utf-8 -*-
import scrapy
import re
import csv

click_url= []

class TrainSpider(scrapy.Spider):
	name = 'Train'
	allowed_domains = ['www.personaltrainers.nl']
	start_urls = [
		'https://www.personaltrainers.nl/zoek-een-personal-trainer']
	baseurl = 'https://www.personaltrainers.nl/zoek-een-personal-trainer/Belgie/'
	basse_url2 = 'https://www.personaltrainers.nl'
	def parse(self, response):
		path = response.xpath("//body")

		for city in path:
			ct_name = city.xpath(".//select[@name='area'][2]/option/text()").extract()[1:]


			for item in ct_name:
				Ct_url = self.baseurl + item +'/'
				# print(Ct_url)

				# yield {"Ct_url": Ct_url}
				yield scrapy.Request(Ct_url, callback=self.parse_info)

	def parse_info(self, response):
		trainers = response.xpath("//body")

		for traineri in trainers:
			njeriu = traineri.xpath(".//div[@class='trainer']/div[@class='trainer_result_more']/a/@href").extract()			
			print(njeriu)
			for njerz in njeriu:


				url_njeriu = self.basse_url2 + njerz
				print(url_njeriu)
				# yield {"NJ" : url_njeriu}
				yield scrapy.Request(url_njeriu, callback=self.parse_tdhanat)

	def parse_tdhanat(self, response):
		bigpath = response.xpath("//div[@id='contenttop']")
		
		for X in bigpath:
			pathname = X.xpath(".//div[@class='padme']/h1/text()").extract_first()
			print(pathname)	
			pathNR =  X.xpath(".//div[@id='trainer_contact']/div/text()").extract_first().replace('u2009',' ')
			line =response.xpath("//body").extract_first()
			lst = str(line).replace("+","").replace('"',"").replace(" ","")
			Email = re.findall(r'[\w\.-]+@[\w\.-]+', lst)[0]
			
			# print(Email[1])
			yield{"TrainMan":pathname,
				"TrainNR" : pathNR,
				"Email" : Email
					}			
