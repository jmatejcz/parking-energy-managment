import logging

LOG_PATH = 'logs/logs.log'
logging.basicConfig(filename=LOG_PATH, filemode='w', level=logging.INFO, format='%(asctime)s - %(message)s')
#logging.getLogger('apscheduler').propagate = False

def log_new_car(new_car_info:dict):
    logging.info(f"new car (id: {new_car_info['id']}) plugged.")

def log_database_update(car_info):
    logging.info(f"car (id:{car_info['id']}) battery updated to {car_info['battery']}.")

def log_charge_mode(new_car_info:dict):
    logging.info(f"car (id:{new_car_info['id']}) charge mode changed to {new_car_info['charge_mode']}.")

def log_price_preds_updated():
    logging.info(f"Energy price predicitons for next 24 hours updated.")
