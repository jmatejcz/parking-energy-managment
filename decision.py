import csv
import time
from statistics import mean
import math
from datetime import datetime


'''
Decision algorytm assumes that we get info about energy price and the prices for the next 24 hours.
This info comes every period of time.
As we don't have real parking and real info from city grid we have to symulate it.
The predictions will be average prices from last days.
'''

PRICE_CUT_OFF = 20

parking_info = {
    'battery_power': 50 # kW
}

def extract_prediction(file_name):
    preds = []
    with open(file_name) as f:
        pred_reader = csv.reader(f, delimiter=';')
        next(pred_reader)
        for row in pred_reader:
            try:
                preds.append(float(row[2].replace(',', '.')))
            except:
                pass

    return preds


def find_best_charge_time(period_preds:list, car_info:dict):
    '''
    Finds best hours to charge car
    Args:
    preds - predictions of energy price 
    car_info - dictionary of car's info
    '''
    hours_needed = (car_info['battery_capacity']*(100-car_info['percent_charged'])/100)/parking_info['battery_power']
    hours_needed = math.ceil(hours_needed)
    idx = range(len(period_preds))
    zipped = list(zip(idx, period_preds))
    srt = sorted(zipped, key=lambda l:l[1])
    return srt[:hours_needed]


def sale_potential(period_preds:list, car_info:dict):
    '''
    Function tries to detect oportiunity to sale energy with profit.
    To do so we need cheap energy period followed by wxpensive energy period and again cheap.
    Args:
    period_preds - predicitons of energy price
    Returns:
    False if sale is not possible
    or
    '''
    hours_needed = (car_info['battery_capacity']*(100-car_info['percent_charged'])/100)/parking_info['battery_power']
    hours_needed = math.ceil(hours_needed)
    load1 = []
    load2 = []
    unload = []
    expensive = 0 # marker used to check if expensive period was found 
    avg = mean(period_preds)
    preds_to_avg = [i - avg for i in period_preds]
    
    for nr, pred in enumerate(preds_to_avg):
        # PRICE_CUT_OFF is a const defining how much should actual price differ from avg price to be considered.
        if pred < -PRICE_CUT_OFF:
            if expensive == 0:
                load1.append((nr, period_preds[nr]))
            if expensive == 1:
                load2.append((nr, period_preds[nr]))
        if pred > PRICE_CUT_OFF:
            expensive = 1
            unload.append((nr, period_preds[nr]))
    

    if len(load2)==0 or len(unload)==0:
        return False
    elif hours_needed >= len(load1)+len(load2):
        return False
    else:
        load1 = sorted(load1, key= lambda l:l[1])
        unload = sorted(unload,key= lambda l:l[1], reverse=True)
        load2 = sorted(load2, key= lambda l:l[1])

        return load1, unload, load2
    
        
def get_car_info(car_info:dict):
    new_car_info = {}
    new_car_info['battery_capacity'] = car_info['carDTO']['carModel']['batteryCapacity']
    if car_info['endTime']:
        endTime = car_info['endTime'].split('.')[0]
        endTime = datetime.strptime(endTime, '%Y-%m-%dT%H:%M:%S')
        start = datetime.now()
        diff = (endTime - start).total_seconds()//3600.0
        new_car_info['when_leaving'] = int(diff)
    else:
        new_car_info['when_leaving'] = car_info['carDTO']['carModel']['batteryCapacity']/parking_info['battery_power']
    new_car_info['percent_charged'] = car_info['battery']
    return new_car_info


def schedule_charge(car_info:dict, preds:list):
    '''
    this func should be called for every car whenever a new predicions came up, schedule for 24h.
    Args:
    car_info - dict like car_info, about car on the parking
    preds - predictions of energy price
    '''
    
    if not preds:
        return 0
    car_info = get_car_info(car_info)
    if car_info['when_leaving']<0:
        return 0
    if car_info['when_leaving'] == 0:
        return 1
    period_preds = preds[:car_info['when_leaving']]
    if sale_potential(period_preds, car_info):
        load1, unload, load2 = sale_potential(period_preds, car_info)
        load1.extend(load2)
        best_unload_timing = unload
        best_load_timing = load1
    else:
        best_load_timing = find_best_charge_time(period_preds, car_info)
        best_unload_timing = []
    
    return output_signal(best_load_timing, best_unload_timing, car_info)
  
    

def output_signal(best_load_timing:list, best_unload_timing:list, car_info) -> int:

    hours_needed = (car_info['battery_capacity']*(100-car_info['percent_charged'])/100)/parking_info['battery_power']
    hours_needed = math.ceil(hours_needed)
    hours_for_now = (car_info['battery_capacity']*car_info['percent_charged']/100)/parking_info['battery_power']

    if best_load_timing and best_load_timing[0][0] == 0 and hours_needed > 0:
        return 1

      
    elif best_unload_timing and best_unload_timing[0][0] == 0 and hours_for_now > 0:
        return -1

    else:    
        return 0
