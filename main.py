import csv
import time
from statistics import mean
import math

'''
Decision algorytm assumes that we get info about energy price and the prices for the next 24 hours.
This info comes every period of time.
As we don't have real parking and real info from city grid we have to symulate it.
The predictions will be average prices from last days.
'''

TIME_INTERVAL = 30 # time between info from city grid about prices in minutes
PRICE_CUT_OFF = 10 # how much money price should be above/below avg to be considered good for sale/buy 

city_grid_info = {
    'buy_price': 700, # zl for a Mwh
    'sell_price': 700 # zl for a Mwh
}

car_info = {
    'model': 'Tesla',
    'battery_capacity': 250, # KWh
    'when_leaving': 24, # how much time to leave
    'percent_charged' : 50
}

parking_info = {
    'battery_power': 50 # kW
}

cars = [car_info]

t = time.localtime()
current_time = time.strftime("%H:%M", t)
print(current_time)

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

def comapre_to_avg_preds(preds:list):
    '''
    Function subtracts from all preds the avg value
    Args: 
    preds - predictions of energy price
    Rerturns: 
    predictions compared to avg, for example -17 means price is 17zl lower than avg.
    '''
    avg = mean(preds)
    preds = [i - avg for i in preds]
    return preds

def find_best_charge_time(preds:list, car_info:dict):
    '''
    Finds best hours to charge car(no sale possibility accounted)
    Args:
    preds - predictions of energy price 
    car_info - dictionary of car's info
    '''
    hours_needed = (car_info['battery_capacity']*car_info['percent_charged']/100)/parking_info['battery_power']
    print(hours_needed)
    hours_needed = math.ceil(hours_needed)
    idx = range(len(preds))
    zipped = list(zip(idx, preds))
    srt = sorted(zipped, key=lambda l:l[1])
    return srt[:hours_needed]

def is_sale_potential(preds_to_avg:list, car_info:dict):
    '''
    Function tries to detect oportiunity to sale energy with profit.
    To do so we need cheap energy period followed by wxpensive energy period and again cheap.
    Args:
    preds_to_avg - predicitons compared to avg energy price (output of compare_to_avg_preds()) 
    car_info - dictionary of car's info
    Returns:
    False if sale is not possible
    or
    load1 - hours when first load is possible,
    unload - hours when selling energy possible,
    load2 - hours when second load possible
    '''
    load1 = []
    load2 = []
    unload = []
    cheap = 0 # marker used to check if first cheap energy period was found
    expensive = 0 # marker used to check if wxpensive period was found 
    for nr, pred in enumerate(preds):
        # PRICE_CUT_OFF is a const defining how much should actual price differ from avg price to be considered.
        if pred < -PRICE_CUT_OFF:
            if expensive == 0:
                load1.append((nr, pred))
                cheap = 1
            if expensive == 1:
                load2.append((nr, pred))
        if pred > PRICE_CUT_OFF and cheap == 1:
            expensive = 1
            unload.append((nr, pred))
    
    if len(load1)==0 or len(load2)==0 or len(unload)==0:
        return False
    else:
        return load1, unload, load2
    
        
            
# this func should be called for every car whenever a new predicions came up, schedule for 24h.
def schedule_charge(parked_cars:list, preds:list, current_time = 0, time_interval = 0):
    '''
    Args:
    parked_cars - list of dicts like car_info, about every car on the parking
    preds - predictions of energy price

    '''
    for car_info in parked_cars:
        period_preds = preds[:car_info['when_leaving']]
        compared_preds = comapre_to_avg_preds(period_preds)
        if is_sale_potential(compared_preds, car_info):
            pass
        else:
            best = find_best_charge_time(period_preds, car_info)

    return best    
    
def schedule_parking():
    pass

preds = extract_prediction('PROG_RB_20211227_20211227202503.csv')

print(find_best_charge_time(preds, car_info))
comapre_to_avg_predsds = comapre_to_avg_preds(preds[:car_info['when_leaving']])
print(is_sale_potential(comapre_to_avg_predsds, car_info))