import scrapy
import csv
from scrapy.utils.response import open_in_browser
import os


class BlogSpider(scrapy.Spider):
    name = 'myspider'

    def __init__(self, city='all', url='http://jefferson.sdgnys.com/search.aspx', sessionID='', *args, **kwargs):
        super(BlogSpider, self).__init__(*args, **kwargs)
        self.city = city
        self.url = url
        self.sessionID = sessionID

    def start_requests(self):
        return [scrapy.Request(
            url=self.url,
            # cookies={'ASP.NET_SessionId': self.sessionID,
            #          'TestCookie': 'test', 'LastSessID': self.sessionID,
            #          'HasAgreedToDisclaimer': 'True',
            #          'pubAccID': '20'
            #          },
            cookies={'ASP.NET_SessionId':'dd3t30553oko1mnlsyomky55',
                     'TestCookie': 'test', 'LastSessID': 'dd3t30553oko1mnlsyomky55',
                     'IMOSearchMode':'basic',
                     'HasAgreedToDisclaimer': 'True',
                     'pubAccID': '20'
                     },
            callback=self.parse
        )]

    def parse(self, response):
        # open_in_browser(response)
        return scrapy.FormRequest(self.url,
                                  formdata={'__EVENTTARGET': '',
                                            '__EVENTARGUMENT': '',
                                            '__VIEWSTATE': '/wEPDwUJNDU1Nzg0NzYzD2QWAgIDD2QWEgICDw8WAh4EVGV4dAUXSmVmZmVyc29uIENvdW50eSBTZWFyY2hkZAIEDxBkDxYXZgIBAgICAwIEAgUCBgIHAggCCQIKAgsCDAINAg4CDwIQAhECEgITAhQCFQIWFhcQBRJBbGwgTXVuaWNpcGFsaXRpZXMFA2FsbGcQBQVBZGFtcwUEMjIyMGcQBQpBbGV4YW5kcmlhBQQyMjIyZxAFB0FudHdlcnAFBDIyMjRnEAUKQnJvd252aWxsZQUEMjIyNmcQBQxDYXBlIFZpbmNlbnQFBDIyMjhnEAUIQ2hhbXBpb24FBDIyMzBnEAUHQ2xheXRvbgUEMjIzMmcQBQlFbGxpc2J1cmcFBDIyMzRnEAUJSGVuZGVyc29uBQQyMjM2ZxAFCkhvdW5zZmllbGQFBDIyMzhnEAUGTGUgUmF5BQQyMjQwZxAFCExvcnJhaW5lBQQyMjQyZxAFBEx5bWUFBDIyNDRnEAUHT3JsZWFucwUEMjI0NmcQBQdQYW1lbGlhBQQyMjQ4ZxAFDFBoaWxhZGVscGhpYQUEMjI1MGcQBQZSb2RtYW4FBDIyNTJnEAUHUnV0bGFuZAUEMjI1NGcQBQdUaGVyZXNhBQQyMjU2ZxAFCVdhdGVydG93bgUEMjI1OGcQBQVXaWxuYQUEMjI2MGcQBQVXb3J0aAUEMjI2MmdkZAIPDxBkDxYDZgIBAgIWAxAFDUFueSBTaXRlIFR5cGUFA2FueWcQBQtSZXNpZGVudGlhbAUDcmVzZxAFCkNvbW1lcmNpYWwFA2NvbWdkZAISDw8WAh8ABRlTd2l0Y2ggdG8gQWR2YW5jZWQgU2VhcmNoZGQCEw8WAh4HVmlzaWJsZWhkAhQPDxYCHwFoZGQCFg8PFgIfAAUFMTcuMDhkZAIXDw8WBB8ABQowNy8xMS8yMDE3HgdUb29sVGlwBRhWNEV4dHJhY3QgVmVyc2lvbjogMTYuMTJkZAIYD2QWAgIBDw8WAh8ABYcGPHA+V2VsY29tZSB0byBKZWZmZXJzb24gQ291bnR5IFJlYWwgUHJvcGVydHkgVGF4IFNlcnZpY2VzIGFzc2Vzc21lbnQgaW5mb3JtYXRpb24gcGFnZS4gICAgVGhpcyBzaXRlIHdpbGwgYWxsb3cgdXNlcnMgdG8gYWNjZXNzIHRoZSBpbmZvcm1hdGlvbiBjb21tb25seSByZXF1ZXN0ZWQgb24gcGFyY2VscyBpbiBKZWZmZXJzb24gQ291bnR5IG91dHNpZGUgdGhlIENpdHkgb2YgV2F0ZXJ0b3duLiAgIFRvIHZpZXcgcGFyY2VsIGluZm9ybWF0aW9uIGZvciB0aGUgQ2l0eSBvZiBXYXRlcnRvd24gcGxlYXNlIGdvIHRvIGh0dHA6Ly93d3cud2F0ZXJ0b3duLW55Lmdvdi9pbW8vLjwvcD4NCjxwPiZuYnNwOzwvcD4NCjxwPkN1cnJlbnQgdGF4IGluZm9ybWF0aW9uIGFuZCByYXRlcyBhcmUgYXZhaWxhYmxlIGJ5IGNsaWNraW5nIG9uIFRheCBJbmZvIHdoZW4gdmlld2luZyBhIHNwZWNpZmljIHBhcmNlbDwvcD4NCjxwPiZuYnNwOzwvcD4NCjxwPlRoZSB0YXggY2FsY3VsYXRvciB3aWxsIG5vdCB3b3JrIGZvciB0b3ducyBwZXJmb3JtaW5nIGEgcmV2YWx1YXRpb24uICZuYnNwO0ZvciAyMDE3IHRoZSBUb3ducyBwZXJmb3JtaW5nIGEgcmV2YWx1YXRpb24gYXJlIExvcnJhaW5lIGFuZCBSb2RtYW4uICZuYnNwOyBJZiB5b3UgaGF2ZSBzcGVjaWZpYyBxdWVzdGlvbnMgYWJvdXQgdGhlIHJldmFsdWF0aW9ucyBwbGVhc2UgY2FsbCB5b3VyIEFzc2Vzc29yLjwvcD4NCjxwPiZuYnNwOzwvcD4NCjxwPjIwMTcgRmluYWwgUm9sbCB2YWx1ZXMgYXJlIG5vdyBhdmFpbGFibGUuPC9wPmRkZBA8N1DPeA3rz2J6d7Zpu+3XFF6g',
                                            '__VIEWSTATEGENERATOR': 'BBBC20B8',
                                            '__EVENTVALIDATION': '/wEWHwLN5KG6BAKJlJfbBQKK29iCCwKK24DLDQKK2+j1DgKK29C/DwKK2/i7BQKtssf3AQKtsq+gAgKtspfqBAKtsv+UBQKtsueQCwLAiOXsBwLAiM2WCALAiLXfCgLAiJ2JCwLAiIWFAQL754PBDQL75+uLDgL759O1DwL757v+AQL756P6BwKe/qG2AgKe/ongBALpzrOKBQKHle2bDgKFn5PZAQKKh+66AwL9t8a4BgKln/PuCgK09sWVBYzdEKpwnd681u9PEWJLs1zXYUUN',
                                            'ddlMunic': self.city,
                                            'txtTaxMapNum': '',
                                            'txtLastOwner': '',
                                            'txtFirstOwner': '',
                                            'txtStreetNum': '',
                                            'txtStreetName': '',
                                            'btnSearch': 'Search',
                                            'hiddenInputToUpdateATBuffer_CommonToolkitScripts': '1'},
                                  callback=self.form_submit)

    def form_submit(self, response2):
        # open_in_browser(response2)
        for row in response2.css('.reportTable tr:not(.historic)'):
            counter = 0
            userData = {}
            for td in row.css('td'):
                counter += 1
                userData[counter] = td.css('::text').extract()
                #print("DATA   ", userData[counter])

                if counter == 2:
                    tax_link = td.css('a ::attr(href)').extract_first()


            if tax_link:
                #yield scrapy.Request(response2.urljoin(tax_link), meta=userData, callback=self.houseCost)
                #report_link = td.css('a ::attr(href)').extract_first()
                #return scrapy.Request(url=tax_link, callback=self.prop_detail)]
                yield scrapy.Request(url='http://jefferson.sdgnys.com/'+tax_link, callback=self.prop_detail)


        next_page = response2.css('#lnkNextPage ::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response2.urljoin(next_page), callback=self.form_submit)

    def houseCost(self, response):
        userData = response.meta
        # yield {
        #     'town': userData[1] if len(userData)>1 else '',
        #     'name': userData[3] if len(userData)>3 else '',
        #     'streetnum': userData[4] if len(userData)>4 else '',
        #     'streetname': userData[5] if len(userData)>5 else '',
        #     'fullMarketValue': response.css('#lblFullMarketValue ::text').extract_first(),
        #     'landAssessment': response.css('#lblLandAssess ::text').extract_first(),
        #     'totalAssessment': response.css('#lblTotalAssess ::text').extract_first(),
        #     'propertyClass': response.css('#lblSitePropClass ::text').extract_first(),
        #     'site': response.css('#lblSite ::text').extract_first(),
        #     'school': response.css('#lblSchoolDist ::text').extract_first(),
        #     'neighborhood': response.css('#lblNeighborhood ::text').extract_first()
        #}

    def prop_detail(self, response):
        #report_link = response.css('#btnReport').extract_first()
        response = str(response)
        if 'propdetail' in response:
            response = response.replace('<', '').replace('>', '').replace('200 ', '')
            response_param = response.split('?')[1]
            swis = response_param.split('&')[0].split('=')[1]
            print_key = response_param.split('&')[1].split('=')[1]
            report_url = 'http://jefferson.sdgnys.com/report.aspx?'
            report_url_new = report_url + 'file=&swiscode='+swis+'&printkey='+print_key+'&sitetype=res&siteNum=1'
            #print('report_url_new ', report_url_new)

            yield scrapy.Request(url=report_url_new, callback=self.report)

    def report(self, response):

        response = response.replace(body=response.body.replace(b'<br>', b' ,'))

        land_assessment = response.css('#lblLandAssessment ::text').extract_first()
        total_assessment = response.css('#lblTotalAssessment ::text').extract_first()
        full_market_value = response.css('#lblFullMarketValue ::text').extract_first()
        bathrooms = response.css('#lblBathrooms ::text').extract_first()
        bedrooms=response.css('#lblBedrooms ::text').extract_first()
        total_acreage=response.css('#lblTotalAcreage ::text').extract_first()
        owner_info=response.css('.owner_info ::text').extract_first()

        print("total_assessment ", total_assessment)
        print("land_assessment ", land_assessment)
        print("full_market_value ", full_market_value)
        print("bathrooms ", bathrooms)
        print("bedrooms ", bedrooms)
        print("total_acreage ", total_acreage)
        print("owner_info ", owner_info)

        #myfile = open("Informationen.csv", "a")
        #writer = csv.writer(myfile, delimiter=',')
        # #writer.writerows(zip(owner_info.encode(),land_assessment.encode(),total_assessment,full_market_value,bathrooms,bedrooms,total_acreage))
        # writer.writerows(zip(owner_info,land_assessment))

        file_exists = os.path.isfile('Informationen.csv')
        with open('Informationen.csv', 'a') as csvfile:
            headers = ['owner_info', 'land_assessment', 'total_assessment', 'owner_info', 'full_market_value', 'bathrooms', 'bedrooms']
            writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames=headers)

            if not file_exists:
                writer.writeheader()  # file doesn't exist yet, write a header

        with open('Informationen.csv', 'a') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',')
            filewriter.writerow([owner_info, land_assessment, total_assessment, total_acreage, full_market_value, bathrooms, bedrooms])




