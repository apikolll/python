import gspread
from oauth2client.service_account import ServiceAccountCredentials


scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    'https://www.googleapis.com/auth/drive'
]

creds = ServiceAccountCredentials.from_json_keyfile_name("./data/creds.json", scopes=scopes)


file = gspread.authorize(creds)
workbook = file.open("python test")
sheet = workbook.sheet1

cells = sheet.range("A2:A89")

# for cell in cells:
#     print(cell.value)