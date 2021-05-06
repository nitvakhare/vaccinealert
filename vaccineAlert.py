#!/usr/local/bin/python
from time import sleep
import requests
from twilio.rest import Client
import datetime
import logging


def getslots(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    final_result = []
    negative = []
    logging.info(response.status_code)
    print(response.status_code)
    if response.status_code == 200:
        data = eval(response.text)
        for entry in data['centers']:
            for cap in entry['sessions']:
                if cap['available_capacity'] > 0:
                    result = {'Center': entry['name'], 'Address': entry['address'],
                              'available_capacity': cap['available_capacity'], 'date': cap['date']}
                    final_result.append(result)
                else:
                    no_slot = {'Center': entry['name'], 'Address': entry['address'],
                               'available_capacity': cap['available_capacity'], 'date': cap['date']}
                    negative.append(no_slot)
        return [final_result, negative]
    else:
        return None


def sendsmsalert(result, mobile):
    account_sid = '<REPLACE_YOUR_TWILIO_SID_HERE>'
    auth_token = '<REPLACE_YOUR_TWILIO_AUTH_TOKEN_HERE>>'

    client = Client(account_sid, auth_token)

    client.api.account.messages.create(
        to=mobile,
        from_="<REPLACE_YOUR_TWILIO_PHONE_NUMBER_HERE>",
        body=str("VaccineAlert:") + str(result))


def main():
    logging.info("Initiating run...")
    tomorrow = datetime.datetime.today() + datetime.timedelta(1)
    tomorrow = tomorrow.strftime('%d-%m-%Y')
    pin_mobile = {'424206': '+91999999999',  # Pin Phone 1
                  '422001': '+91999999999',  # Pin Phone 1
                  '422008': '+91999999999',  # Pin Phone 1
                  '422001': '+91999999999',  # Pin Phone 1
                  '422008': '+91999999999',  # Pin Phone 1
                  }
    for k, v in pin_mobile.items():
        pin = k
        mobile = v
        url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pin}&date={tomorrow}"
        final_result = getslots(url)
        if final_result and len(final_result[0]) > 0:
            try:
                sendsmsalert(str(final_result[0]), mobile)
                logging.info(f"Sent SMS to {mobile}")
            except:
                pass
        sleep(30)


if __name__ == '__main__':
    main()
