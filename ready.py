import gspread
from oauth2client.service_account import ServiceAccountCredentials
from data import *
import time
import schedule

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    'https://www.googleapis.com/auth/drive'
]

creds = ServiceAccountCredentials.from_json_keyfile_name("./data/creds.json", scopes=scopes)

file = gspread.authorize(creds)
workbook = file.open("python test")
sheet = workbook.sheet1

def changeFormatPitchbook(result):
    million = "M"
    billion = "B"
    trillion = "T"

    if billion in result["marketCap"]:
        mc = result["marketCap"].split("B")
        newMC = mc[0].split("$")
        return float(newMC[1]) * 1000000000
    elif trillion in  result["marketCap"]:
        mc = result["marketCap"].split("T")
        newMC = mc[0].split("$")
        return float(newMC[1]) * 1000000000000
    elif million in  result["marketCap"]:
        mc = result["marketCap"].split("M")
        newMC = mc[0].split("$")
        return float(newMC[1]) * 1000000
    else:
        return result["marketCap"]
    

def changeFormatYahoo(result):
    million = "M"
    billion = "B"
    trillion = "T"

    if billion in result:
        mc = result.split("B")
        return float(mc[0]) * 1000000000
    elif trillion in  result:
        mc = result.split("T")
        return float(mc[0]) * 1000000000000
    elif million in  result:
        mc = result.split("M")
        return float(mc[0]) * 1000000
    else:
        return result


def main():

    pitchbook = sheet.range("B2:B89")
    yahoo = sheet.range("A2:A89")

    for i in range(len(pitchbook)):
        print(f"Fetching data for {yahoo[i].value}...")

        result_pitchbook = pitchBook(pitchbook[i].value)
        result_yahoo = yahooFinance(yahoo[i].value)

        mc = changeFormatPitchbook(result_pitchbook)
        gp = changeFormatYahoo(result_yahoo)

        sheet.update_acell(f"D{i + 2}", f"{result_pitchbook['price']}")
        sheet.update_acell(f"E{i + 2}", f"{mc}")
        sheet.update_acell(f"F{i + 2}", f"{result_pitchbook['enterpriseValue']}")
        sheet.update_acell(f"G{i + 2}", f"{result_pitchbook['revenue']}")
        sheet.update_acell(f"H{i + 2}", f"{result_pitchbook['ebitda']}")
        sheet.update_acell(f"I{i + 2}", f"{result_pitchbook['netIncome']}")
        sheet.update_acell(f"J{i + 2}", f"{gp}")


# schedule.every(10).minutes.do(main)

schedule.every().day.at("00:00").do(main)

while True:
    schedule.run_pending()
    time.sleep(1)

# if __name__ == "__main__":
#     main()
