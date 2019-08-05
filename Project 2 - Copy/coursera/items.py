# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

#get scrapy, not much to say about that...
import scrapy

# define a class that will link with the bottom of your spider's data collection function
class CourseraItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Course_Title=scrapy.Field()  #same for each field
    Partner=scrapy.Field()
    Rating=scrapy.Field()
    Num_of_Ratings=scrapy.Field()
    Num_of_Reviews=scrapy.Field()
    Difficulty_Level=scrapy.Field()
    Teacher=scrapy.Field()
    Language=scrapy.Field()
    Enrollment=scrapy.Field()
    Skills=scrapy.Field()
    Percent_Benefit=scrapy.Field()