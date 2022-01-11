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
PRICE_CUT_OFF = 15 # how much money price should be above/below avg to be considered good for sale/buy 

city_grid_info = {
    'buy_price': 700, # zl for a Mwh
    'sell_price': 700 # zl for a Mwh
}

car_info = {
    'model': 'Tesla',
    'battery_capacity': 250, # KWh
    'when_leaving': 22, # how much time to leave
    'percent_charged' : 50
}

parking_info = {
    'battery_power': 50 # kW
}

cars = [car_info]

t = time.localtime()
current_time = time.strftime("%H:%M", t)
#print(f"current_time: {current_time}")

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

def compare_to_avg_preds(preds:list):
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

def find_best_charge_time(preds:list, car_info:dict, for_sale:bool = False):
    '''
    Finds best hours to charge car
    Args:
    preds - predictions of energy price 
    car_info - dictionary of car's info
    for_sale - if True will serach for the highest price instead of the lowest
    '''
    hours_needed = (car_info['battery_capacity']*car_info['percent_charged']/100)/parking_info['battery_power']
    print(f"how many hours needed to charge: {hours_needed}")
    hours_needed = math.ceil(hours_needed)
    idx = range(len(preds))
    zipped = list(zip(idx, preds))
    srt = sorted(zipped, key=lambda l:l[1])
    return srt[:hours_needed]

def find_best_sale_time(load1, unload, load2):
    '''
    Args:
    Lists returned by is_sale_potential
    load1 - 1st load time window
    unload - unload time window
    load2 - 2nd load time window
    Returns :
    Precise hours when to laod and unload in diffrent lists 
    '''
    load1 = sorted(key= lambda l:l[1])



def sale_potential(preds_to_avg:list, car_info:dict):
    '''
    Function tries to detect oportiunity to sale energy with profit.
    To do so we need cheap energy period followed by wxpensive energy period and again cheap.
    Args:
    preds_to_avg - predicitons compared to avg energy price (output of compare_to_avg_preds()) 
    car_info - dictionary of car's info
    Returns:
    False if sale is not possible
    or
    load1 - hours when to first load,
    unload - hours when to sell energy,
    load2 - hours when to second load 
    '''
    load1 = []
    load2 = []
    unload = []
    cheap = 0 # marker used to check if first cheap energy period was found
    expensive = 0 # marker used to check if expensive period was found 
    for nr, pred in enumerate(preds_to_avg):
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
        load1 = sorted(load1, key= lambda l:l[1])
        unload = sorted(unload,key= lambda l:l[1], reverse=True)
        load2 = sorted(load2, key= lambda l:l[1])
        possible_hours = min(len(load1), len(load2), len(unload))
        best_load1 = load1[:possible_hours]
        best_unload = unload[:possible_hours]
        best_load2 = load2[:possible_hours]

        return best_load1, best_unload, best_load2
    
        
            
# this func should be called for every car whenever a new predicions came up, schedule for 24h.
def schedule_charge(pcar_info:dict, preds:list, current_time = 0, time_interval = 0):
    '''
    Args:
    pcar_info - dict like car_info, about car on the parking
    preds - predictions of energy price
    '''
    period_preds = preds[:car_info['when_leaving']]
    compared_preds = compare_to_avg_preds(period_preds)
    if sale_potential(compared_preds, car_info):
        load1, unload, load2 = sale_potential(compared_preds, car_info)
        load1.extend(load2)
        best_unload_timing = unload
        best_load_timing = load1
    else:
        best_load_timing = find_best_charge_time(period_preds, car_info)
        best_unload_timing = []

    return best_load_timing, best_unload_timing   
    
def output_signal(best_load_timing:list, best_unload_timing:list) -> int:
    for i in best_load_timing:
        if i[0] == 1:
            return 1

    for i in best_unload_timing:
        if [0] == 1:
            return -1
        
    return 0




def main():
    
    preds = extract_prediction('parking-mock/PROG_RB_20211227_20211227202503.csv')
    best_load_timing, best_unload_timing = schedule_charge(car_info, preds)
    print(output_signal(best_load_timing, best_unload_timing))



if __name__ == '__main__':
    main()