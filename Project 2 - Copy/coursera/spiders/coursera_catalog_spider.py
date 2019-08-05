
from scrapy import Spider, Request # Request allows for the passing of URL's from 1 function to another, as the argument
from coursera.items import CourseraItem # connects to Item folder
import re # regular expressions

class CourseraSiteSpider(Spider): #initiate the class that's a spider
    name = 'coursera_site_spider' #name to call the spider within the command line / anaconda prompt (make sure to cd in the right directory to run)
    allowed_urls = ["https://www.coursera.org/"] #all the websites the spider is allowed to go to; if it finds a link outside this main website, it will ignore
    start_urls = ["https://www.coursera.org/sitemap~www~courses.xml"] #first page your spider starts on

    def parse(self, response): #first function, creates a list of all the pages and iterates through them
        num_pages = 100 # I manually calculated # of pages it has to go through. Will change to be dynamic or continue until it gets an error in a future edit.
        #result_urls is my url that has a {} substitution to put in new integers (1,2,3...) to go to each page. Copied example from bestbuy lab.
        result_urls = ["https://www.coursera.org/courses?query=&indices%5Bprod_all_products%5D%5Bpage%5D={}&indices%5Bprod_all_products%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Bprod_all_products%5D%5Bconfigure%5D%5BhitsPerPage%5D=10&configure%5BclickAnalytics%5D=true".format(x) for x in range(1, num_pages + 1)]

        for y in result_urls:  # 1st for loop! Go to each page of individual products (example) and do something...
            print('=' * 50)  # test by showing lines in command line output to know it's working
            print(y) # another test to display exactly which url you're looping through (good for error checking)
            yield Request(url=y, callback=self.parse_into_course) #send each of those url's one at a time through to next function
            # url = this is just describing an argument
            # callback = sending the result of 1 index of the for loop to which function next? Sends 1 url at a time

        def parse_into_course(self, response): #next function, this is the page with 10 products
            course_list = response.xpath('//a[@data-click-key="search.search.click.search_card"]/@href').extract()
            # find the xpath that can be generalized to get all the urls on a given page. Put into a list
            # here @href leads to a link that reads like /next_product, so have to append it to the original website link
            # ex. main_page.com/next_product . Can concatenate like a string in this situation
            # Concatenation main_page + x (where x is the index of course list)

            for x in course_list: #2nd for loop! This one goes through all the products in a given page.
                print('-' * 50) # more testing to see if this loop is functioning as expected
                print(x) # same as above
                yield Request(url="https://www.coursera.org" + x, callback=self.parse_course)
                # takes each product's individual url from the list (url) of all 10 products in the list on that page
                # and callback sends it to the next function (in this case, "parse_course")
                # basically, get into each course by its URL

        def parse_course(self, response): #finally getting data! Last function to actually grab stuff

            try: # basic error control; attempt to collect result from each xpath. If it doesn't work, go to except
                #assigns variable "Course Title" to the text / number value you get from this XPath.
                Course_Title = response.xpath('//h1[@class="H2_1pmnvep-o_O-weightNormal_s9jwp5-o_O-fontHeadline_1uu0gyz max-text-width-xl m-b-1s"]//text()').extract()[0]
                # This line contains the xpath from using "inspect" on a part of the website.
                # '//__ anything before, start when you find this ___ thing
                # [@___ = "_____" ] first part after @ can match the xpath to a specific element
                # //text()' grabs text to add to item.
                # extract() gets the value from your xpath
                # can index if you go into a list from this operation
            except:
                Course_Title = ""
                # what to do if you can't get a value from that xpath. Sometimes good to use empty strings instead of "None" since "None" will
                # become "NaN" which is registered as a float in Python. Can complicate data cleaning slightly
            try:
                Partner = response.xpath('//div[@class="m-b-1s m-r-1"]//@alt').extract()[0]
            except:
                Partner = ""

            item = CourseraItem() # connects to item page in your project folder
            item['Course_Title'] = Course_Title # assigns the item "Course_Title" with the variable assigned in the above collecting function
            item['Partner'] = Partner # same as above. Gets value into function

            yield item #yields the result to the items page to be put in the final data set.

