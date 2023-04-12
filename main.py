code = input("code >> ")
import aiohttp, asyncio
from html.parser import HTMLParser
async def scrape(code):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f'https://finance.yahoo.com/quote/{code}') as r:
            try:               
                class MyHTMLParser(HTMLParser):
                    def __init__(self):
                        HTMLParser.__init__(self)
                        self.recording = 0
                        self.data = []
                        self.dta = []

                    def handle_starttag(self, tag, attributes):
                        if tag != 'fin-streamer':
                            return
                        if self.recording:
                            self.recording += 1
                            return
                        if  attributes[1][0] == "data-symbol" and attributes[1][1] == str.upper(code) and attributes[3][1] == "regularMarketPrice" :
                            self.recording = 1
                        else:
                            return
                        
                    def handle_endtag(self, tag):
                        if tag == 'fin-streamer' and self.recording:
                            self.recording -= 1

                    def handle_data(self, data):
                        if self.recording == 1:
                            self.dta.append(data)
                parser = MyHTMLParser()
                parser.feed(await r.text())
                dta = parser.dta
                print(dta)
            except:
                pass
            r.close()
        await cs.close()
    
asyncio.run(scrape(code))