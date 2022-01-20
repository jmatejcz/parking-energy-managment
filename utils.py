import logging

LOG_PATH = 'logs/logs.log'
logging.basicConfig(filename=LOG_PATH, filemode='a', level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger('apscheduler').propagate = False

def log_new_car(car_info:dict):
    logging.info(f"new car (id: {car_info['id']}, licesnse plate: {car_info['carDTO']['licensePlate']}) plugged.")

def log_database_update(car_info):
    logging.info(f"car (id:{car_info['id']}, licesnse plate: {car_info['carDTO']['licensePlate']}, leaving at:{car_info['endTime']}) battery updated to {car_info['battery']}.")

def log_charge_mode(car_info:dict):
    logging.info(f"car (id:{car_info['id']}, licesnse plate: {car_info['carDTO']['licensePlate']}, leaving at:{car_info['endTime']}) charge mode changed to {car_info['charge_mode']}.")

def log_price_preds_updated(preds):
    logging.info(f"Energy price predicitons for next 24 hours updated.")
    logging.info(f"Current predicions:{preds}")
