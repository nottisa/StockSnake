code = input("code >> ")
import aiohttp, asyncio
from html.parser import HTMLParser
async def scrape(code):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f'https://finance.yahoo.com/quote/{code}') as r:
                       
            class MyHTMLParser(HTMLParser):
                def __init__(self):
                    HTMLParser.__init__(self)
                    self.recording = 0
                    self.data = {}

                def handle_starttag(self, tag, attributes):
                    if tag == 'fin-streamer':
                        if  attributes[1][0] == "data-symbol" and attributes[1][1] == str.upper(code) and attributes[3][1] == "regularMarketPrice" :
                            self.recording = 1
                        elif attributes[1][0] == "data-symbol" and attributes[1][1] == str.upper(code) and attributes[3][1] == "regularMarketChange" :
                            self.recording = 2
                        elif attributes[1][0] == "data-symbol" and attributes[1][1] == str.upper(code) and attributes[2][1] == "regularMarketChangePercent" :
                            self.recording = 3
                        else:
                            return
                    elif tag == 'td':
                        if  attributes[0][0] == "class" and attributes[0][1] == "Ta(end) Fw(600) Lh(14px)" and attributes[1][1] == "PREV_CLOSE-value" :
                            self.recording = 4
                        elif attributes[0][0] == "class" and attributes[0][1] == "Ta(end) Fw(600) Lh(14px)" and attributes[1][1] == "OPEN-value" :
                            self.recording = 5
                        elif attributes[0][0] == "class" and attributes[0][1] == "Ta(end) Fw(600) Lh(14px)" and attributes[1][1] == "BID-value" :
                            self.recording = 6
                        elif attributes[0][0] == "class" and attributes[0][1] == "Ta(end) Fw(600) Lh(14px)" and attributes[1][1] == "ASK-value" :
                            self.recording = 7
                        elif attributes[0][0] == "class" and attributes[0][1] == "Ta(end) Fw(600) Lh(14px)" and attributes[1][1] == "DAYS_RANGE-value" :
                            self.recording = 8
                        elif attributes[0][0] == "class" and attributes[0][1] == "Ta(end) Fw(600) Lh(14px)" and attributes[1][1] == "FIFTY_TWO_WK_RANGE-value" :
                            self.recording = 9
                        elif attributes[0][0] == "class" and attributes[0][1] == "Ta(end) Fw(600) Lh(14px)" and attributes[1][1] == "TD_VOLUME-value" :
                            self.recording = 10
                        elif attributes[0][0] == "class" and attributes[0][1] == "Ta(end) Fw(600) Lh(14px)" and attributes[1][1] == "AVERAGE_VOLUME_3MONTH-value" :
                            self.recording = 11
                        elif attributes[0][0] == "class" and attributes[0][1] == "Ta(end) Fw(600) Lh(14px)" and attributes[1][1] == "MARKET_CAP-value" :
                            self.recording = 12
                        elif attributes[0][0] == "class" and attributes[0][1] == "Ta(end) Fw(600) Lh(14px)" and attributes[1][1] == "BETA_5Y-value" :
                            self.recording = 13
                        elif attributes[0][0] == "class" and attributes[0][1] == "Ta(end) Fw(600) Lh(14px)" and attributes[1][1] == "PE_RATIO-value" :
                            self.recording = 14
                        elif attributes[0][0] == "class" and attributes[0][1] == "Ta(end) Fw(600) Lh(14px)" and attributes[1][1] == "EPS_RATIO-value" :
                            self.recording = 15
                        elif attributes[0][0] == "class" and attributes[0][1] == "Ta(end) Fw(600) Lh(14px)" and attributes[1][1] == "EARNINGS_DATE-value" :
                            self.recording = 16
                        elif attributes[0][0] == "class" and attributes[0][1] == "Ta(end) Fw(600) Lh(14px)" and attributes[1][1] == "DIVIDEND_AND_YIELD-value" :
                            self.recording = 17
                        elif attributes[0][0] == "class" and attributes[0][1] == "Ta(end) Fw(600) Lh(14px)" and attributes[1][1] == "EX_DIVIDEND_DATE-value" :
                            self.recording = 18
                        elif attributes[0][0] == "class" and attributes[0][1] == "Ta(end) Fw(600) Lh(14px)" and attributes[1][1] == "ONE_YEAR_TARGET_PRICE-value" :
                            self.recording = 19
                        else:
                            return
                    else:
                        return
                        
                def handle_endtag(self, tag):
                    if tag == 'fin-streamer' and self.recording:
                        self.recording = 0

                def handle_data(self, data):
                    if self.recording == 1:
                        self.data["regularMarketPrice"] = data
                    elif self.recording == 2:
                        self.data["regularMarketChange"] = data
                    elif self.recording == 3:
                        self.data["regularMarketChangePercent"] = data[1:-2]
                    elif self.recording == 4:
                        self.data["PREV_CLOSE-value"] = data
                    elif self.recording == 5:
                        self.data["OPEN-value"] = data
                    elif self.recording == 6:
                        self.data["BID-value"] = data
                    elif self.recording == 7:
                        self.data["ASK-value"] = data
                    elif self.recording == 8:
                        self.data["DAYS_RANGE-value"] = data
                    elif self.recording == 9:
                        self.data["FIFTY_TWO_WK_RANGE-value"] = data
                    elif self.recording == 10:
                        self.data["TD_VOLUME-value"] = data
                    elif self.recording == 11:
                        self.data["AVERAGE_VOLUME_3MONTH-value"] = data
                    elif self.recording == 12:
                        self.data["MARKET_CAP-value"] = data
                    elif self.recording == 13:
                        self.data["BETA_5Y-value"] = data
                    elif self.recording == 14:
                        self.data["PE_RATIO-value"] = data
                    elif self.recording == 15:
                        self.data["EPS_RATIO-value"] = data
                    elif self.recording == 16:
                        self.data["EARNINGS_DATE-value"] = data
                    elif self.recording == 17:
                        self.data["DIVIDEND_AND_YIELD-value"] = data
                    elif self.recording == 18:
                        self.data["EX_DIVIDEND_DATE-value"] = data
                    elif self.recording == 19:
                        self.data["ONE_YEAR_TARGET_PRICE-value"] = data
                    self.recording = 0
            parser = MyHTMLParser()
            parser.feed(await r.text())
            return parser.data
            r.close()
        await cs.close()
print(asyncio.run(scrape(code)))