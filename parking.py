from request import WebClient
import decision
import json
from apscheduler.schedulers.blocking import BlockingScheduler


def read_current_res_ids(filename:str) -> set:
    '''

    '''
    with open(filename) as f:
        res_list = json.load(f)
    ids = set([res['id'] for res in res_list])

    return ids

def get_new_cars(new_res_list:list, ids:set) -> list:
    '''

    '''
    new_cars = []
    for new_res in new_res_list:
        if new_res['id'] not in ids:
            new_cars.append(new_res)
    
    return new_cars


def get_car_info(reservation_dict:dict) -> dict:
    car_info = {}
    car_info['battery_capacity'] = reservation_dict['carDTO']['carModel']['batteryCapacity']
    car_info['when_leaving'] = reservation_dict['endTime'].time()
    car_info['battery_capacity'] = reservation_dict['carDTO']['carModel']['batteryCapacity']
    car_info['percent_charged'] = reservation_dict['battery']
    return car_info


def make_decision_for_cars(res_list:list, preds_src:str) -> int:
    signals = []
    preds = decision.extract_prediction(preds_src)
    for res_dict in res_list:
        car_info = get_car_info(res_dict)
        best_load_timing, best_unload_timing = decision.schedule_charge(car_info, preds)
        signals.append(decision.output_signal(best_load_timing, best_unload_timing))
    
    return signals


def check_for_new_cars(webClient) -> None:
    token = WebClient.get_login_token('email=john.doe%40mail.com&password=1234')
    new_res_list = WebClient.get_reserations_list(token)

    current_ids = read_current_res_ids('data/reservation_list.json')   
    new_cars = get_new_cars(new_res_list, current_ids)

    with open('data/reservation_list.json', 'w') as f:
        json.dump(new_res_list, f)

    if new_cars:
        signals = make_decision_for_cars(new_cars, 'data/PROG_RB_20211227_20211227202503.csv')
        print(signals)


def update_database():
    pass


def schedule_charge_for_all_cars():
    with open('data/reservation_list.json', 'r') as f:
        res_list = json.load(f)
    signals = make_decision_for_cars(res_list, 'data/PROG_RB_20211227_20211227202503.csv')
    print(signals)


if __name__ == '__main__':
    WebClient = WebClient('http://localhost:8080')

    scheduler = BlockingScheduler(timezone="Europe/Warsaw")
    scheduler.add_job(lambda: check_for_new_cars(WebClient), 'interval', seconds=20)
    scheduler.add_job(schedule_charge_for_all_cars, 'interval', minutes=60)
    scheduler.add_job(lambda: update_database(WebClient), 'interval', minutes=10)
    
    scheduler.start()