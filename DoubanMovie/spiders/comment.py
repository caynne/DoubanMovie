# -*- coding:utf-8 -*-

import scrapy
from scrapy import Selector
from DoubanMovie.items import DoubanmovieItem
from scrapy import Request
from collections import defaultdict

class CrawlComment(scrapy.Spider):
    name = "comment"
    start_urls= ["https://movie.douban.com/subject/25921812/comments"]

    form_data = {
        'source':'None',
        'redir':'https://www.douban.com',
        'form_email':'455049421@qq.com',
        'form_password':'lmm123456',
        'login':'登录'
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Host': 'accounts.douban.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
    }

    def start_requests(self):
        return [Request(url ="http://www.douban.com/login",
                        meta={'cookiejar':1},
                        callback=self.parse_login
                             )]

    def parse_login(self,response):
        sel = Selector(response)
        #验证码
        if 'captcha_image' in response.body:
            captcha_id = sel.xpath('//input[@name="captcha-id"]/@value').extract()
            #验证码图片url
            captcha_url =  sel.xpath('//img[@id="captcha_image"]/@src').extract()
            print '需求输入难码,请打开链接查看验证码后输入:'
            print captcha_url
            captcha_solution = raw_input()
            self.form_data['captcha-solution'] = captcha_solution;
            self.form_data['captcha-id'] = captcha_id

        return scrapy.FormRequest.from_response(response,
                                                formdata=self.form_data,
                                                meta={'cookiejar':response.meta['cookiejar']},
                                                callback = self.after_login
                                                )
    def after_login(self,response):
        print response.status
        return Request(url='https://movie.douban.com/subject/25921812/comments',
                       meta={'cookiejar':response.meta['cookiejar']},
                       callback= self.parse
                       )


    def parse(self, response):
        sel = Selector(response)
        item = DoubanmovieItem()
        #xpath获取用户名
        commentItem = sel.xpath('//div[@class="comment-item"]')
        print commentItem[8].extract()
        for ci in commentItem:
            #userName = ci.xpath('//span[@class = "comment-info"]/a/text()').extract()
            #xpath获取每一条评论的文本内容
            #comment = ci.xpath('//div[@class="comment"]/p[@class=""]/text()[1]').extract()
            #xpath获取这条评论的打分
            #grade = ci.xpath('//span[@class="comment-info"]/span[contains(@class,"allstar")]/@title'.format()).extract()
            # for i in range(19):
            #     item['userName'] = userName[i].replace('\n','').strip()
            #     item['comment'] = comment[i].replace('\n','').strip()
            #     item['grade'] = grade[i].replace('\n','').strip()
            #     yield item

            #这里使用xpth要在前面加"."使用相对路径来取元素,不然还是绝对路径取全局的.
            try :
                item['userName'] = ci.xpath('.//span[@class = "comment-info"]/a/text()').extract()[0].replace('\n','').strip()
                item['comment'] = ci.xpath('.//div[@class="comment"]/p[@class=""]/text()[1]').extract()[0].replace('\n','').replace('\"','').replace('\'','').strip()
                item['grade'] = ci.xpath('.//span[@class="comment-info"]/span[contains(@class,"allstar")]/@title'.format()).extract()[0].replace('\n','').strip()
            except:
                pass
            yield item



        #获取下一页的url
        nextPageUrl = sel.xpath('//a[@class = "next"]/@href').extract()[0]
        if nextPageUrl:

             nextPageUrl = "https://movie.douban.com/subject/25921812/comments" + nextPageUrl
             request = Request(nextPageUrl,
                               callback=self.parse,
                               meta={'cookiejar':response.meta['cookiejar']}
                               )
             yield request
