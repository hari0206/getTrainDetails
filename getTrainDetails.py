from datetime import datetime, timedelta
import pandas as pd
import json
import requests

URL = "https://www.irctc.co.in/eticketing/protected/mapps1/altAvlEnq/TC"


def get_departure_arrival_date_time(duration, departure_time):
    """functionality to foramt time according to requirements

    Args:
        duration (str): journey duration
        departure_time (str): departure time of train

    Returns:
        object: datetime object
    """
    current_date = datetime.now().strftime("%Y%m%d")
    departure_dt = f"{current_date};{departure_time}"
    departure_date_time = datetime.strptime(departure_dt, '%Y%m%d;%H:%M')
    duration_obj = datetime.strptime(duration, '%H:%M')
    arrival_date_time = departure_date_time + \
        timedelta(hours=duration_obj.hour, minutes=duration_obj.minute)

    return departure_date_time, arrival_date_time


def write_to_excel(data):
    """functionality to write data to excel sheet

    Args:
        data (list(dict)): all trains details
    """
    df = pd.DataFrame.from_dict(data)
    df.to_excel('get_list_of_train.xlsx', index=False,
                sheet_name="Train Details")


def get_train_details():
    """functionality to extract train details from irctc website 
    """
    try:
        current_date = datetime.now().strftime("%Y%m%d")
        payload = {
            "concessionBooking": False,
            "srcStn": "MAS",
            "destStn": "SBC",
            "jrnyClass": "",
            "jrnyDate": current_date,
            "quotaCode": "GN",
            "currentBooking": "false",
            "flexiFlag": False,
            "handicapFlag": False,
            "ticketType": "E",
            "loyaltyRedemptionBooking": False,
            "ftBooking": False
        }
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'greq': '1646911169787',
        }
        response = requests.post(URL, headers=headers, data=json.dumps(payload))
        data = response.json()

        train_details = [{
            "TrainName": ele.get("trainName"),
            "TrainNumber": ele.get("trainNumber"),
            "DepartureDateTime": get_departure_arrival_date_time(ele.get("duration"), ele.get("departureTime"))[0],
            "ArrivalDateTime": get_departure_arrival_date_time(ele.get("duration"), ele.get("departureTime"))[1],
            "TravelDuration": ele.get("duration")
        } for ele in data["trainBtwnStnsList"]]
        
        write_to_excel(train_details)

        return {
            "status":True,
            "description":"data fetched successfully"
        }
    except Exception as e:
        return {
            "status":False,
            "description":str(e)
        }

if __name__=="__main__":
    result=get_train_details()
    print(result)