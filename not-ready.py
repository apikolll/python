import gspread
from oauth2client.service_account import ServiceAccountCredentials
from data import *
import time
import schedule
import datetime
from test import *

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    'https://www.googleapis.com/auth/drive'
]

creds = ServiceAccountCredentials.from_json_keyfile_name("./data/creds.json", scopes=scopes)

file = gspread.authorize(creds)
workbook = file.open("Valuation Database (updated)")
sheet = workbook.worksheet("Data")

def changeFormatPitchbook(result):
    million = "M"
    billion = "B"
    trillion = "T"

    if billion in result["marketCap"]:
        mc = result["marketCap"].split("B")
        newMC = mc[0].split("$")
        return float(newMC[1]) * 1000000
    elif trillion in  result["marketCap"]:
        mc = result["marketCap"].split("T")
        newMC = mc[0].split("$")
        return float(newMC[1]) * 1000000000
    elif million in  result["marketCap"]:
        mc = result["marketCap"].split("M")
        newMC = mc[0].split("$")
        return float(newMC[1]) * 1000
    else:
        return result["marketCap"]
    

def changeFormatYahoo(result):
    million = "M"
    billion = "B"
    trillion = "T"

    if billion in result:
        mc = result.split("B")
        return float(mc[0]) * 1000000
    elif trillion in  result:
        mc = result.split("T")
        return float(mc[0]) * 1000000000
    elif million in  result:
        mc = result.split("M")
        return float(mc[0]) * 1000
    else:
        return result

def timeStamp():
    time_stamp = datetime.datetime.now()
    # ts = f'{time_stamp.strftime("%A")}, {(time_stamp.strftime("%b"))} {(time_stamp.strftime("%b"))}, {(time_stamp.strftime("%H"))}:{(time_stamp.strftime("%M"))}'
    return f'{time_stamp.strftime("%c")}'


# def checkValue():

# def scrapeYahoo():
#     yahoo = sheet.range("D3:D98")

#     print("Scraping from yahoo finance started...")

#     for i in range(len(yahoo)):
#         result_yahoo = yahooFinance(yahoo[i].value)

#         gp = changeFormatYahoo(result_yahoo["gp"])
#         mc = changeFormatYahoo(result_yahoo["marketCap"])
#         ev = changeFormatYahoo(result_yahoo["enterpriseValue"])
#         rv = changeFormatYahoo(result_yahoo["revenue"])
#         ebit = changeFormatYahoo(result_yahoo["ebitda"])
#         ni  = changeFormatYahoo(result_yahoo["netIncome"])
        
#         sheet.update_acell(f"H{i + 3}", f"{result_yahoo['price']}")
#         sheet.update_acell(f"I{i + 3}", f"{mc}")
#         sheet.update_acell(f"J{i + 3}", f"{ev}")
#         sheet.update_acell(f"K{i + 3}", f"{rv}")
#         sheet.update_acell(f"L{i + 3}", f"{gp}")
#         sheet.update_acell(f"M{i + 3}", f"{ebit}")
#         sheet.update_acell(f"N{i + 3}", f"{ni}")
    
#     print("Scraping from yahoo finance completed...")


# def scrapePitchBook():
#     pitchbook = sheet.range("B3:B92")

#     print("Scraping from pitchbook started...")
#     for i in range(len(pitchbook)):
        
#         result_pitchbook = pitchBook(pitchbook[i].value)

#         mc = changeFormatPitchbook(result_pitchbook)
        
#         sheet.update_acell(f"H{i + 3}", f"{result_pitchbook['price']}")
#         sheet.update_acell(f"I{i + 3}", f"{mc}")
#         sheet.update_acell(f"J{i + 3}", f"{result_pitchbook['enterpriseValue']}")
#         sheet.update_acell(f"K{i + 3}", f"{result_pitchbook['revenue']}")
#         sheet.update_acell(f"M{i + 3}", f"{result_pitchbook['ebitda']}")
#         sheet.update_acell(f"N{i + 3}", f"{result_pitchbook['netIncome']}")
    
#     print("Scraping from pitchbook completed...")


# def checkRange():
#     for i in range(3, 98):
#         checkRange = sheet.range(f"H{i}:N{i}")
#         for j in range(len(checkRange)):
#             print(checkRange[j].value == "" or checkRange[j].value == "N/A")


# def main():
#     # pitchbook = sheet.range("B3:B92")
#     # yahoo = sheet.range("D3:D98")
#     time_stamp = timeStamp()

#     # scrapePitchBook()
#     yahoo = sheet.range("D3:D98")

#     print("Scraping from yahoo finance started...")

#     for i in range(len(yahoo)):
#         result_yahoo = yahooFinance(yahoo[i].value)

#         gp = changeFormatYahoo(result_yahoo["gp"])
#         mc = changeFormatYahoo(result_yahoo["marketCap"])
#         ev = changeFormatYahoo(result_yahoo["enterpriseValue"])
#         rv = changeFormatYahoo(result_yahoo["revenue"])
#         ebit = changeFormatYahoo(result_yahoo["ebitda"])
#         ni  = changeFormatYahoo(result_yahoo["netIncome"])
        
#         sheet.update_acell(f"H{i + 3}", f"{result_yahoo['price']}")
#         sheet.update_acell(f"I{i + 3}", f"{mc}")
#         sheet.update_acell(f"J{i + 3}", f"{ev}")
#         sheet.update_acell(f"K{i + 3}", f"{rv}")
#         sheet.update_acell(f"L{i + 3}", f"{gp}")
#         sheet.update_acell(f"M{i + 3}", f"{ebit}")
#         sheet.update_acell(f"N{i + 3}", f"{ni}")
    
#     print("Scraping from yahoo finance completed...")
    
#     sheet.update_acell("B100", time_stamp)
#     sheet.update_acell("D100", "")

#     # sheet.update_acell("D109", "Pass")
    

# if __name__ == "__main__":
#     main()


def main():
    pitchbook = sheet.range("B3:B92")
    time_stamp = timeStamp()

    sheet.update_acell("B100", time_stamp)
    sheet.update_acell("D100", "")

    print("Scraping from pitchbook started...")
    for i in range(len(pitchbook)):
        
        result_pitchbook = scrapePitchbook(pitchbook[i].value)

        # print(result_pitchbook)

    #     # mc = changeFormatPitchbook(result_pitchbook)

        sheet.batch_update([
            {
                'range': f"H{i + 3}:I{i + 3}",
                'values': [[f"{result_pitchbook['price']}", f"{result_pitchbook['marketCap']}"]]
            }
        ])
        
    #     sheet.update_acell(f"H{i + 3}", f"{result_pitchbook['price']}")
    #     sheet.update_acell(f"I{i + 3}", f"{result_pitchbook['marketCap']}")
    #     sheet.update_acell(f"J{i + 3}", f"{result_pitchbook['enterpriseValue']}")
    #     sheet.update_acell(f"K{i + 3}", f"{result_pitchbook['revenue']}")
    #     sheet.update_acell(f"M{i + 3}", f"{result_pitchbook['ebitda']}")
    #     sheet.update_acell(f"N{i + 3}", f"{result_pitchbook['netIncome']}")
    
    print("Scraping from pitchbook completed...")

    sheet.update_acell("D100", "Pass")
    

if __name__ == "__main__":
    main()
