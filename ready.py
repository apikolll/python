import gspread
from oauth2client.service_account import ServiceAccountCredentials
from data import *
import time
import schedule
import datetime

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    'https://www.googleapis.com/auth/drive'
]

credentials = {
  "type": "service_account",
  "project_id": "web-scraping-396009",
  "private_key_id": "508f121b119d0e1d9b75ed25136282141ec09abf",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC2C13s6dsPzC8k\nXA4HY/CPwPBicgAThC5o3M+yoVaINWILYY8X0T4foDIA5An2h/ASvMvHu6Ed3ZyY\n5vts1NmQGVudyT9vJS+U7M7QcK/1t/vMV4MQDCeo3naEZTrht2pu8tmP+EB8bcsL\nsHQPotVDjSUeMMT5O+1p2FtCKdD1yN4tVJInW3oD91BIUnZ9kQHPcPG0iyX4T09u\n6l7b+vJ/4CvQDtH2w3Ik1BgYQfVDV9lFt0BY9hsDeYkRBq4Oh9j5CvQhIjRCws/1\nbSD/ssCbDJcl4QJPu5j9Ycr4/EweTTRJfyQ83+xIRTLBoV84Gokh6ZoqBcyTQEdW\ndvysLvgtAgMBAAECggEAC3qAq/fm6dfBv99/ZvSPQ5Eygb1Bx06WBTipw/qrqR+s\nlJ53K6pJlNbrWuZba8xl1S31r3IOQQLV5UeTN5PdkATOo7lVIvNLom6ixRPbPyQg\nYAxt5YIkB2As8EDYdfO0ZgCGuq7i6grw5Zt1Bf4KHR32PDFuX29pkztNgx4oizF0\nTJ8dZaLxJ5DuzvlF5h69oYOnj7eXrytfccY5QV66o+n2kcnXXDv73gZ37A6RZEnr\nTMIs6y5L9QFO0wRenddySNAj/aFevXHp/O+K7HHuU6Zey32rEK4tBLo+4qdiJC90\nC0QrpS6Z8VBXg2FyZqYgur7YvOI0wfVryenLVqv5hQKBgQDeNbGJd4soQNANo3DH\nEKF6kNcUW3BZOfQK/eQNqvZcQhlMd9tQuu+Xmic4em8uRHpUK1PmgfuC/1YMkuwm\nGodPubTUaprhAQF7nbqCeVXxumsp30g7flaDilA7+lEgvynZ/qXe6lqORS7Ewq0q\nv2DKNQDscwtzQ1RPBMFyzJZWuwKBgQDRuhgpFOVarB9+SZpTggqy3M4K+4d/fEXA\nzuu9EooMV03qSKrfyT05opaIhdwFfegObQq4RYF+JLqSy5d3cMl+4rb8OsVAtC2y\nABZo1dAM1U/5ybzmjmlV8ido5sfIVux93ovGtw0iYTGDQxoXRC3xAokEi3NsHUF/\neXH57wCiNwKBgQDNmkLWHh1NNoMLS4ILPrEa9i9774tJk9zh2r+LgfeHr8U2wuPT\nk9QiowjNMkPzPHsvrBNqgjSUpesZoUwNiZhPxVWzAZyiukqD9ZJgLSK/kqybRrTQ\nD3q/JVhN1rQAJ8DyqrMRSihV4V9/wV124zMMhfR/04bxtIeqwYy4yuIEBwKBgQCH\naQn0bGNxWbSzyz3zMQFLXrlB6gkgTNKUnIUkfHXZZf0OiYCaIMqBDfL3jsXyXcqY\nldrYAziKg5ha80yGd7IBVMwkqqV1E2B1jwzo/zPnNUr/0js++TAVp9W+K1NOjKEA\n29GPqdy3F93qDEcqQoEPHT3uS0NoyLLjZTwrzR6xnQKBgCFaWOV8pEMvk1pSjaNG\nMwju2fXV2vNNYK3qZVkYoNW6DPB01f+1smOZwrHmGdMAHtM2ygI8hThCEMXD8QGZ\nc3emCEBeSGEBB82wCBc8bSaULiwmnsiu46gBGt6dsQusv90SQBcu+0t3XgLbRzJI\nj6tU5BYv9ylL2IDkePNBSqmy\n-----END PRIVATE KEY-----\n",
  "client_email": "web-scraping-python@web-scraping-396009.iam.gserviceaccount.com",
  "client_id": "108912995456780197091",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/web-scraping-python%40web-scraping-396009.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

creds = ServiceAccountCredentials.from_json_keyfile_name(credentials, scopes=scopes)

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

def timeStamp():
    time_stamp = datetime.datetime.now()
    # ts = f'{time_stamp.strftime("%A")}, {(time_stamp.strftime("%b"))} {(time_stamp.strftime("%b"))}, {(time_stamp.strftime("%H"))}:{(time_stamp.strftime("%M"))}'
    return f'{time_stamp.strftime("%c")}'

def main():

    pitchbook = sheet.range("B3:B90")
    yahoo = sheet.range("E3:E90")
    # time_stamp = sheet.acell("B91")
    time_stamp = timeStamp()

    sheet.update_acell("B94", time_stamp)
    sheet.update_acell("E94", "Pass")

    for i in range(len(pitchbook)):
        print(f"Fetching data for {yahoo[i].value}...")

        result_pitchbook = pitchBook(pitchbook[i].value)
        result_yahoo = yahooFinance(yahoo[i].value)

        mc = changeFormatPitchbook(result_pitchbook)
        gp = changeFormatYahoo(result_yahoo)
        
        sheet.update_acell(f"I{i + 3}", f"{result_pitchbook['price']}")
        sheet.update_acell(f"J{i + 3}", f"{mc}")
        sheet.update_acell(f"L{i + 3}", f"{result_pitchbook['enterpriseValue']}")
        sheet.update_acell(f"M{i + 3}", f"{result_pitchbook['revenue']}")
        sheet.update_acell(f"O{i + 3}", f"{result_pitchbook['ebitda']}")
        sheet.update_acell(f"P{i + 3}", f"{result_pitchbook['netIncome']}")
        sheet.update_acell(f"N{i + 3}", f"{gp}")
    

# schedule.every().day.at("18:50").do(main)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

if __name__ == "__main__":
    main()
