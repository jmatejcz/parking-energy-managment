import logging
from turtle import update
from request import WebClient
import decision
import json
import utils
from apscheduler.schedulers.blocking import BlockingScheduler
import csv
import datetime

DATABASE_INTERVAL = 10 #minutes

class Parking():

    def __init__(self) -> None:
        self.state = []
        self.price_preds = []
        self.working_time = 0
        self.charger_power = 50

    def update_price_preds(self, filename):
        with open(filename) as f:
            pred_reader = csv.reader(f, delimiter=';')
            next(pred_reader)
            rows = list(pred_reader)
            new_preds = []
            for row in rows[self.working_time+1: self.working_time+25]:
                try:
                    new_preds.append(float(row[2].replace(',', '.')))
                except ValueError:
                    pass
                
            self.price_preds = new_preds
        self.working_time += 1
        utils.log_price_preds_updated(self.price_preds)
        
    def add_new_car(self, car_info:dict) -> None:
        self.state.append(car_info)

    def update_state(self, state:list) -> None:
        self.state = state

    def get_new_cars(self, new_res_list) -> None:
        ids = set([car['id'] for car in self.state])
        new_cars = []
        for new_car in new_res_list:
            if new_car['id'] not in ids:
                new_cars.append(new_car)
        
        for car_info in new_cars:
            car_info = self.make_decision_for_car(car_info)
            self.add_new_car(car_info)
            utils.log_new_car(car_info)

    def make_decision_for_car(self, car_info:dict) -> dict:
        if car_info['endTime'] is None:
            mode = 1
        else:
            mode = decision.schedule_charge(car_info, self.price_preds)

        car_info['charge_mode'] = mode
        utils.log_charge_mode(car_info)
        return car_info


def check_for_new_cars(WebClient, Parking) -> None:
    token = WebClient.get_login_token('email=john.doe%40mail.com&password=1234')
    new_res_list = WebClient.get_reserations_list(token)

    Parking.get_new_cars(new_res_list)


def update_database(WebClient, Parking):
    token = WebClient.get_login_token('email=john.doe%40mail.com&password=1234')
    for res in Parking.state:
        
        res['battery'] += res['charge_mode']*Parking.charger_power/res['carDTO']['carModel']['batteryCapacity']*100*DATABASE_INTERVAL/60
        if res['battery'] > 100:
            res['battery'] = 100
        elif res['battery'] < 0:
            res['battery'] = 0
        WebClient.put_battery(token, res['id'], res['battery'])
        utils.log_database_update(res)


def schedule_charge_for_all_cars(Parking):
    for car_info in Parking.state:
        Parking.make_decision_for_car(car_info)


def update_price_preds(Parking, filename):
    Parking.update_price_preds(filename)
    schedule_charge_for_all_cars(Parking)


if __name__ == '__main__':
    WebClient = WebClient('http://localhost:8080')
    Parking = Parking()
    Parking.update_price_preds('data/PL_CENY_NIEZB_20220101_20220115.csv')
    scheduler = BlockingScheduler(timezone="Europe/Warsaw")

    scheduler.add_job(lambda: check_for_new_cars(WebClient, Parking), 'interval', minutes=1, id='check_for_new_cars')
    #scheduler.add_job(lambda: schedule_charge_for_all_cars(Parking), 'interval', hours=1, id='schedule_charge')
    scheduler.add_job(lambda: update_database(WebClient, Parking), 'interval', minutes=DATABASE_INTERVAL, id='update_database')
    scheduler.add_job(lambda: update_price_preds(Parking, 'data/PL_CENY_NIEZB_20220101_20220115.csv'), 'interval', hours=1, id='update_price_preds')
    
    scheduler.start()
