from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
import requests
import cloudscraper
import asyncio



headers = {'User-agent':'Mozilla/5.0 (X11; Linux x86_64; Ubuntu 22.04) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
# headers = {'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

def yahooFinance(ticker):

    if ticker == "":
        return "No value"
    
    url = f'https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}'

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    price = soup.find('fin-streamer', {'data-field': 'regularMarketPrice', 'data-symbol': f'{ticker}'}).text
    EV1 = soup.find('tr', {'class' : 'Bxz(bb) H(36px) BdB Bdbc($seperatorColor) fi-row Bgc($hoverBgColor):h'})
    MC1 = soup.find('tr', {'class': 'Bxz(bb) H(36px) BdY Bdc($seperatorColor) fi-row Bgc($hoverBgColor):h'})
    RV1 = soup.find_all('tr', {'class': 'Bxz(bb) H(36px) BdY Bdc($seperatorColor)'})
    GP1 = soup.find_all('table', {'class': 'W(100%) Bdcl(c)'})

    IS = GP1[7].find_all('tr', {'class': 'Bxz(bb) H(36px) BdB Bdbc($seperatorColor)'})
    
    ev = EV1.find('td', {'class' : 'Fw(500) Ta(end) Pstart(10px) Miw(60px)'}).text
    mc = MC1.find('td', {'class' : 'Fw(500) Ta(end) Pstart(10px) Miw(60px)'}).text
    rv = RV1[6].find('td', {'class': 'Fw(500) Ta(end) Pstart(10px) Miw(60px)'}).text

    gp = IS[2].find('td', {'class': 'Fw(500) Ta(end) Pstart(10px) Miw(60px)'}).text

    ebitda = IS[3].find('td', {'class': 'Fw(500) Ta(end) Pstart(10px) Miw(60px)'}).text
    net = IS[4].find('td', {'class': 'Fw(500) Ta(end) Pstart(10px) Miw(60px)'}).text

    # print("*****************************")
    # print(f'Data for {ticker}')
    # print(f'Price: {price}')
    # print(f'EV: {ev}')
    # print(f'MC: {mc}')
    # print(f'Revenue: {rv}')
    # print(f'Gross Profit: {gp}')
    # print(f'EBITDA: {ebitda}')
    # print(f'Net Income: {net}')
    # print("*****************************")

    results = {
        "price": price,
        "gp": gp,
        "marketCap": mc,
        "enterpriseValue": ev,
        "revenue": rv,
        "ebitda": ebitda,
        "netIncome": net
    }
    return results

    # return gp
    # print(gp)


def investingData(url):
    scraper = cloudscraper.CloudScraper()
    response = scraper.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    current = soup.find_all('div', {'class': 'infoLine'})

    gp_margin = current[0].find('span', {'class', 'float_lang_base_2 text_align_lang_base_2 dirLtr bold'}).text
    np_margin = current[2].find('span', {'class', 'float_lang_base_2 text_align_lang_base_2 dirLtr bold'}).text

    print(f'Gross Profit Margin: {gp_margin}')
    print(f'Net Profit Margin: {np_margin}')


def pitchBook():
    # url = "https://finance.yahoo.com/quote/ABNB/key-statistics?p=ABNB"
    url = "https://pitchbook.com/profiles/company/51261-67#stock"
    headers = {
        "User-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3', 
        'Accept-Encoding': 'gzip, deflate, br', 
        'Accept-Language': 'en-US,en;q=0.9,en;q=0.8'
    }
    # headers={"User-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}
    
  
    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--start-maximized")
    # options.add_argument("--disable-extensions")
    # options.add_argument("--disable-infobars")
    # options.add_argument('--window-size=1920,1080')
    # options.add_argument('--no-sandbox')

    # driver = webdriver.Chrome(options=options)
    # driver.get(url)
    # soup = BeautifulSoup(driver.page_source, 'lxml')
    # print(soup)
    # driver.quit()

    req = requests.get(url, headers=headers)
    print(req)

    # stocks = soup.find("div", {'id': 'stock'})
    # financials = soup.find("div", {'id': 'financials'})
    # tbody = financials.find("tbody")
    # tr = tbody.find_all("tr")

    # price = soup.find("td", {'class': 'data-table__cell align-right offset-left-XL-5'}).text
    # mc = stocks.find_all("td", {'class': 'data-table__cell align-right pl-xl-10'})
    # ev = tr[0].find_all("td", {'class': 'data-table__cell align-right offset-right-XL-10'})
    # revenue = tr[1].find_all("td", {'class': 'data-table__cell align-right offset-right-XL-10'})
    # ebitda = tr[2].find_all("td", {'class': 'data-table__cell align-right offset-right-XL-10'})
    # netIncome = tr[3].find_all("td", {'class': 'data-table__cell align-right offset-right-XL-10'})

    # print(soup)
        
    # results = {
    #     "price": price,
    #     "marketCap": mc[2].text,
    #     "enterpriseValue": ev[0].text,
    #     "revenue": revenue[0].text,
    #     "ebitda": ebitda[0].text,
    #     "netIncome": netIncome[0].text
    # }

    # return results

pitchBook()