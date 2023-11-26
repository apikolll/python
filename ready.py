import requests
import gspread
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials
import time

# Headers to allow browser detect as a human not Bot.
headers = {'User-agent':'Mozilla/5.0 (X11; Linux x86_64; Ubuntu 22.04) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

# Scope is use to connect to google shhet
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name("./data/creds.json", scopes=scopes)

file = gspread.authorize(creds)
workbook = file.open("Valuation Database (updated)")
sheet = workbook.worksheet("Data")

yahooTicker = sheet.get("D3:D")


# Function to change format from received data
def changeFormatYahoo(result):
    million = "M"
    billion = "B"
    trillion = "T"

    if billion in result:
        mc = result.split("B")
        return '{:,.0f}'.format(float(mc[0]) * 1000000)
    elif trillion in  result:
        mc = result.split("T")
        return '{:,.0f}'.format(float(mc[0]) * 1000000000)
    elif million in  result:
        mc = result.split("M")
        return '{:,.0f}'.format(float(mc[0]) * 1000)
    else:
        return result


# The main function
def main(): 
    print("Running...")
    for i in range(len(yahooTicker)):
        url = f"https://finance.yahoo.com/quote/{yahooTicker[i][0]}/key-statistics?p={yahooTicker[i][0]}"
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, "lxml")

        price = soup.find('fin-streamer', {'data-field': 'regularMarketPrice', 'data-symbol': f'{yahooTicker[i][0]}'}).text
        EV1 = soup.find('tr', {'class' : 'Bxz(bb) H(36px) BdB Bdbc($seperatorColor) fi-row Bgc($hoverBgColor):h'})
        MC1 = soup.find('tr', {'class': 'Bxz(bb) H(36px) BdY Bdc($seperatorColor) fi-row Bgc($hoverBgColor):h'})
        RV1 = soup.find_all('tr', {'class': 'Bxz(bb) H(36px) BdY Bdc($seperatorColor)'})
        GP1 = soup.find_all('table', {'class': 'W(100%) Bdcl(c)'})
        all = soup.find_all("table", {"class": "W(100%) Bdcl(c)"})
        IS1 = all[7].find("tbody")
        quaterlyRevenueGrowth = IS1.find_all("td", {"class" : "Fw(500) Ta(end) Pstart(10px) Miw(60px)"})[2].text
        leveredFreeCashFlow = all[9].find_all("td", {"class" : "Fw(500) Ta(end) Pstart(10px) Miw(60px)"})[1].text

        IS = GP1[7].find_all('tr', {'class': 'Bxz(bb) H(36px) BdB Bdbc($seperatorColor)'})

        ev = EV1.find('td', {'class' : 'Fw(500) Ta(end) Pstart(10px) Miw(60px)'}).text
        mc = MC1.find('td', {'class' : 'Fw(500) Ta(end) Pstart(10px) Miw(60px)'}).text
        rv = RV1[6].find('td', {'class': 'Fw(500) Ta(end) Pstart(10px) Miw(60px)'}).text
        gp = IS[2].find('td', {'class': 'Fw(500) Ta(end) Pstart(10px) Miw(60px)'}).text
        ebitda = IS[3].find('td', {'class': 'Fw(500) Ta(end) Pstart(10px) Miw(60px)'}).text
        net = IS[4].find('td', {'class': 'Fw(500) Ta(end) Pstart(10px) Miw(60px)'}).text

        data = {
            "price": price,
            "EV": ev,
            "MC" : mc,
            "RV": rv,
            "GP": gp,
            "EBITDA": ebitda,
            "NET" : net,
            "QRG": quaterlyRevenueGrowth,
            "LFCF": leveredFreeCashFlow
        }

        sheet.batch_update([
                {
                    'range': f"H{i + 3}:P{i + 3}",
                    'values': [[f"${price}", changeFormatYahoo(mc), changeFormatYahoo(ev), changeFormatYahoo(rv), changeFormatYahoo(gp), changeFormatYahoo(ebitda), changeFormatYahoo(net), quaterlyRevenueGrowth, changeFormatYahoo(leveredFreeCashFlow)]]
                }
            ])

        print(f"{yahooTicker[i][0]} completed")
        time.sleep(2)

    print("Completed")


if __name__ == "__main__":
    main()