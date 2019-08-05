from scrapy import Spider, Request # Request allows you to pass the URL's from 1 function to another as the argument
from coursera.items import CourseraItem #connects to Item folder
import re #regular expressions; don't need if you're not using this

class CourseraSiteSpider(Spider): #initiate the class that's a spider
    name = 'coursera_site_spider' #name that you call the spider with in your command line / anaconda prompt (make sure you're cd into your directory when you run)
    allowed_urls = ["https://www.coursera.org/"] #all the websites your spider is allowed to go to; if it finds a link outside this main website, it will ignore
    start_urls = ["https://www.coursera.org/sitemap~www~courses.xml"] #first page your spider starts on

    def parse(self, response): #first function, doesn't matter what you call it, just want these arguments
        num_pages = 406 # I manually calculated # of pages it has to go through.
        #result_urls is my url that has a {} substitution to put in new integers (1,2,3...) to go to each page. Copied example from bestbuy lab.
        result_urls = ["https://www.coursera.org/courses?query=&indices%5Bprod_all_products%5D%5Bpage%5D={}&indices%5Bprod_all_products%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Bprod_all_products%5D%5Bconfigure%5D%5BhitsPerPage%5D=10&configure%5BclickAnalytics%5D=true".format(x) for x in range(1, num_pages + 1)]

        for y in result_urls:  # 1st for loop! Go to each page of individual products (example) and do something...
            print('=' * 50)  # test by showing lines in your command line output to know it's working
            print(y) # another test to display exactly which url you're looping through (good for error checking)
            yield Request(url=y, callback=self.parse_into_course) #send each of those url's one at a time through to next function
            # url = like R, where this is just describing an argument
            # callback = sending the result of 1 index of the for loop to which function next? Sends 1 url at a time

        def parse_into_course(self, response): #next level function, this is your page with 10 products (let's say)
            course_list = response.xpath('//a[@data-click-key="search.search.click.search_card"]/@href').extract()
            # find the xpath that can be generalized to get all the urls on a given page.
            # here @href leads to a link that reads like /next_product, so you have to append it to the original website link
            # ex. main_page.com/next_product . Can concatenate like a string if you have this situation
            # Concatenation main_page + x (where x is the index of course list)

            for x in course_list: #2nd for loop! This one goes through all the products in a given page.
                print('-' * 50) # more testing to see if this loop is going
                print(x) # same as above
                yield Request(url="https://www.coursera.org" + x, callback=self.parse_course)
                # takes each product's individual url from the list (url) of all 10 products in the list on that page
                # and callback sends it to the next function (in this case, "parse_course")
                # basically, get into each course by its URL

        def parse_course(self, response): #finally getting data! Last function to actually grab stuff

        #if you have a repetitive structure (like reviews) may want to use best buy example for this part.

            try: # basic error control; attempt to collect result from each xpath. If it doesn't work, go to except
                #assigns variable "Course Title" to the text / number value you get from this XPath.
                Course_Title = response.xpath('//h1[@class="H2_1pmnvep-o_O-weightNormal_s9jwp5-o_O-fontHeadline_1uu0gyz max-text-width-xl m-b-1s"]//text()').extract()[0]
                # This line contains the xpath that you get from "inspect" on a part of your website. can make customizable with:
                # '//__ <first part of website you're checking into, can be anything since // means whatever before, start when you find this ___ thing
                # [@___ = "_____" ] first part after @ can match the xpath to a specific part, don't know what it's called...
                # //text()' grabs text (even though it's part of a string) to add to item.
                # extract gets the value from it
                # can index if you go into a list from this operation
            except:
                Course_Title = ""
                # what to do if you can't get a value from that xpath. Sometimes good to use empty strings instead of "None" since "None" will
                # become "NaN" which is registered as a float in Python.
            try:
                Partner = response.xpath('//div[@class="m-b-1s m-r-1"]//@alt').extract()[0]
            except:
                Partner = ""
            try:
                Rating = float(response.xpath(
                    '//span[@class="H4_1k76nzj-o_O-weightBold_uvlhiv-o_O-bold_1byw3y2 m-l-1s m-r-1 m-b-0"]//text()').extract()[
                                   0])
            except:
                Rating = None
            try:
                Num_of_Ratings = response.xpath(
                    '//div[@class="P_gjs17i-o_O-weightNormal_s9jwp5-o_O-fontBody_56f0wi m-r-1s color-white"]//text()').extract()
            except:
                Num_of_Ratings = ""
            try:
                Num_of_Reviews = response.xpath('//div[@class="reviewsCount"]//text()').extract()
            except:
                Num_of_Reviews = ""
            try:
                Difficulty_Level = response.xpath(
                    '//h4[@class="H4_1k76nzj-o_O-weightBold_uvlhiv-o_O-bold_1byw3y2 m-b-0 m-t-1s"]//text()').extract()
            except:
                Difficulty_Level = ""
            try:
                Language = response.xpath(
                    '//h4[@class="H4_1k76nzj-o_O-weightBold_uvlhiv-o_O-bold_1byw3y2 m-b-0"]//text()').extract()
            except:
                Language = ""
            try:
                Enrollment = response.xpath('//div[@class="enrolledLargeFont_16g5ucx"]//text()').extract()[0]
            except:
                Enrollment = ""
            try:
                Skills = response.xpath(
                    '//div[@class="Box_120drhm-o_O-displayflex_poyjc-o_O-wrap_rmgg7w"]//text()').extract()
            except:
                Skills = ""
            try:
                Percent_Benefit = response.xpath(
                    '//div[@class="Box_120drhm-o_O-centerAlign_19zvu2s-o_O-displayflex_poyjc m-b-1"]//text()').extract()
            except:
                Percent_Benefit = ""
            try:
                Teacher = response.xpath('//a[@class="link-no-style"]/text()').extract()
            except:
                Teacher = ""
            # Financial_Aid= response.xpath('')

            item = CourseraItem()
            item['Course_Title'] = Course_Title
            item['Partner'] = Partner
            item['Rating'] = Rating
            item['Num_of_Ratings'] = Num_of_Ratings
            item['Num_of_Reviews'] = Num_of_Reviews
            item['Difficulty_Level'] = Difficulty_Level
            item['Teacher'] = Teacher
            item['Language'] = Language
            item['Enrollment'] = Enrollment
            item['Skills'] = Skills
            item['Percent_Benefit'] = Percent_Benefit

            yield item
