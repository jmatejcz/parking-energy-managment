from request import WebClient
import decision
import json

parked_cars = []

def read_current_res_ids(filename) -> set:
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
    car_info['battery_capacity'] = reservation_dict['carDTO']['carModel']['batteyCapacity']
    when_leaving = reservation_dict['endTime'].time()
    car_info['when_leaving'] = reservation_dict['carDTO']['carModel']['batteyCapacity']


if __name__ == '__main__':
    WebClient = WebClient('http://localhost:8080')
    token = WebClient.get_login_token('email=john.doe%40mail.com&password=1234')
    new_res_list = WebClient.get_reserations_list(token)


    current_ids = read_current_res_ids('data/reservation_list.json', )   

    new_cars = get_new_cars(new_res_list, current_ids)

    with open('data/reservation_list.json', 'w') as f:
        json.dump(new_res_list, f)