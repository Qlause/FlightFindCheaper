import datetime as dt
from flighdata import FlighData
from spreadsheet import Sheet
from decouple import config
import smtplib

KEY_T = config("KEY_T")
URL_T = config("URL_T")
AUTHKEY_T = config("AUTHKEY_T")
AUTHURL_T = config("AUTHURL_T")
SHEET_KEY = config("SH_KEY")
SHEET_URL = config("SH_URL")
FROM = config("FROM")
TIME = dt.datetime.now().strftime(f"%d/%m/%Y")
NEXT_6_MONTH = dt.datetime.now() + dt.timedelta(days=30 * 6)
NEXT_6_MONTH = NEXT_6_MONTH.strftime(f"%d/%m/%Y")
EMAIL = config("EMAIL")
EMAIL_PW = config("EMAIL_PW")

f_data = FlighData(KEY_T, FROM)
sheet = Sheet(SHEET_KEY, SHEET_URL)

def send_email(to_city, airport, price, airlines, date_depart, date_arrive):
    conn = smtplib.SMTP("smtp.gmail.com")
    conn.starttls()
    conn.login(user=EMAIL,
               password=EMAIL_PW)
    
    airline = ""
    for i, v in enumerate(airlines):
        airline += v
        if i != len(airlines) - 1 :
            airline += ", "
    
    conn.sendmail(from_addr=EMAIL,
                  to_addrs="ardialbrian@gmail.com",
                  msg=f"Subject: Allert flight Discount\n\nFlight to {to_city} / {airport }, \nOnly Rp.{price} ({airline}). \nDeparture {date_depart} ~ {date_arrive}")


user_inp = sheet.retrieve().json()['checkUserInput']
for data in user_inp:
    oneway = f_data.get_data(fly_to=data["iataCode"],
                    date_from=TIME,
                    date_to=NEXT_6_MONTH,
                    price_max=data['price'])
    
    if len(oneway) > 0:
        date = oneway[0]["dates_in_utc"].split(" ~ ")
        date_d = date[0].split("T")[0]
        date_a = date[1].split("T")[0]
        send_email(oneway[0]["city_to"],
                   oneway[0]["country_to"],
                   str('{:20,.2f}'.format(float(oneway[0]["price"]))).strip(), 
                   oneway[0]["airlines"],
                   date_d,
                   date_a)
    else:
        print("No Data Found")

 