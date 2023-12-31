import unittest
from decision import *
import datetime
class GetCarInfoTest(unittest.TestCase):

    def test_battery_capacity_get_car_info(self):
        car_info = {
            "id": "ac1f2001-7e59-1f19-817e-597fd23e0000",
            "parkingSpotId": "c0a83201-8cxc-1hnn-237c-dfjr4rcc05047",
            "carDTO": {
                "id": "c0a83801-7d96-17c0-817d-96e85f600003",
                "licensePlate": "WZ1463Y",
                "ownerId": "c0a83801-7cdc-1fd9-817c-dc301d4f0001",
                "carModel": {
                    "id": "c0a83801-7cdc-1fd9-817g-fc381e4f0003",
                    "manufacturer": "MINI",
                    "name": "Electric",
                    "batteryCapacity": 40
                }
            },
            "userPreferences": [],
            "startTime": "2022-01-14T17:50:56.1772139",
            "endTime": "2022-01-14T23:30:00",
            "battery": 40
        }
        
        result = get_car_info(car_info)

        self.assertEqual(result['battery_capacity'], 40)


    def test_percent_charged(self):
        car_info = {
            "id": "ac1f2001-7e59-1f19-817e-597fd23e0000",
            "parkingSpotId": "c0a83201-8cxc-1hnn-237c-dfjr4rcc05047",
            "carDTO": {
                "id": "c0a83801-7d96-17c0-817d-96e85f600003",
                "licensePlate": "WZ1463Y",
                "ownerId": "c0a83801-7cdc-1fd9-817c-dc301d4f0001",
                "carModel": {
                    "id": "c0a83801-7cdc-1fd9-817g-fc381e4f0003",
                    "manufacturer": "MINI",
                    "name": "Electric",
                    "batteryCapacity": 40
                }
            },
            "userPreferences": [],
            "startTime": "2022-01-14T17:50:56.1772139",
            "endTime": "2022-01-14T23:30:00",
            "battery": 40
        }
    
        result = get_car_info(car_info)

        self.assertEqual(result['percent_charged'], 40)


    def test_when_leaving(self):
        start = datetime.datetime.today()
        start = datetime.datetime.strptime(str(start).split('.')[0], '%Y-%m-%d %H:%M:%S')
        start = start.isoformat()
        end = datetime.datetime.today() + datetime.timedelta(hours=8)
        end = datetime.datetime.strptime(str(end).split('.')[0], '%Y-%m-%d %H:%M:%S')
        end = end.isoformat()
        car_info = {
            "id": "ac1f2001-7e59-1f19-817e-597fd23e0000",
            "parkingSpotId": "c0a83201-8cxc-1hnn-237c-dfjr4rcc05047",
            "carDTO": {
                "id": "c0a83801-7d96-17c0-817d-96e85f600003",
                "licensePlate": "WZ1463Y",
                "ownerId": "c0a83801-7cdc-1fd9-817c-dc301d4f0001",
                "carModel": {
                    "id": "c0a83801-7cdc-1fd9-817g-fc381e4f0003",
                    "manufacturer": "MINI",
                    "name": "Electric",
                    "batteryCapacity": 40
                }
            },
            "userPreferences": [],
            "startTime": str(start),
            "endTime": str(end),
            "battery": 40
        }
        
        result = get_car_info(car_info)
        start = datetime.datetime.now().hour
        endTime = car_info['endTime'].split('.')[0]
        endTime = datetime.datetime.strptime(endTime, '%Y-%m-%dT%H:%M:%S').hour
        self.assertEqual(result['when_leaving'], endTime-start-1)

    def test_when_leaving_miliseconds(self):
        start = datetime.datetime.today()
        start = datetime.datetime.strptime(str(start).split('.')[0], '%Y-%m-%d %H:%M:%S')
        start = start.isoformat()
        end = datetime.datetime.today() + datetime.timedelta(hours=8)
        end = datetime.datetime.strptime(str(end).split('.')[0], '%Y-%m-%d %H:%M:%S')
        end = end.isoformat()
        car_info = {
            "id": "ac1f2001-7e59-1f19-817e-597fd23e0000",
            "parkingSpotId": "c0a83201-8cxc-1hnn-237c-dfjr4rcc05047",
            "carDTO": {
                "id": "c0a83801-7d96-17c0-817d-96e85f600003",
                "licensePlate": "WZ1463Y",
                "ownerId": "c0a83801-7cdc-1fd9-817c-dc301d4f0001",
                "carModel": {
                    "id": "c0a83801-7cdc-1fd9-817g-fc381e4f0003",
                    "manufacturer": "MINI",
                    "name": "Electric",
                    "batteryCapacity": 40
                }
            },
            "userPreferences": [],
            "startTime": str(start),
            "endTime": str(end),
            "battery": 40
        }
        result = get_car_info(car_info)
        start = datetime.datetime.now().hour
        endTime = car_info['endTime'].split('.')[0]
        endTime = datetime.datetime.strptime(endTime, '%Y-%m-%dT%H:%M:%S').hour
        
        self.assertEqual(result['when_leaving'], endTime-start-1)

class TestFindBestChargeTime(unittest.TestCase):


    def test_low_high_prices(self):
        car_info = {
            'battery_capacity': 100,
            'when_leaving' : 8,
            'percent_charged' : 10
        }
        preds = [70.0, 150.0, 150.0, 190.0, 190.0, 390.0, 490.0, 350.0, 450.0]

        result = find_best_charge_time(preds, car_info)
        self.assertCountEqual(result, [(0, 70.0), (1, 150.0)])


class SalePotentialTest(unittest.TestCase):

    
    def test_low_high_low_prices(self):
        preds = [70.0, 150.0, 150.0, 390.0, 390.0, 390.0, 300.0, 150.0, 169.73, 190.2, 200.0]
        car_info = {
            'battery_capacity': 100,
            'when_leaving' : 11,
            'percent_charged' : 10
        }
        result_load1, result_unload, result_load2 = sale_potential(preds, car_info)
        
        self.assertCountEqual(result_load1, [(0, 70.0), (1, 150.0), (2, 150.0)]) 
        self.assertCountEqual(result_unload, [(3, 390.0), (4, 390.0), (5, 390.0), (6, 300.0)])
        self.assertCountEqual(result_load2, [(7, 150.0), (8, 169.73), (9, 190.2), (10, 200.0)])

    
    def test_high_low_prices(self):
        preds = [400.0, 450.0, 450.0, 390.0, 270.0, 270.0, 200.0, 200.0]
        car_info = {
            'battery_capacity': 100,
            'when_leaving' : 8,
            'percent_charged' : 10
        }
        result_load1, result_unload, result_load2 = sale_potential(preds, car_info)
        
        self.assertCountEqual(result_load1, []) 
        self.assertCountEqual(result_unload, [(0, 400.0), (1, 450.0), (2, 450.0), (3, 390.0)])
        self.assertCountEqual(result_load2, [(4, 270.0), (5, 270.0), (6, 200.0), (7, 200.0)])

    
    def test_low_high_prices(self):
        preds = [200.0, 250.0, 250.0, 290.0, 370.0, 370.0, 400.0, 400.0]
        car_info = {
            'battery_capacity': 100,
            'when_leaving' : 8,
            'percent_charged' : 10
        }
        result = sale_potential(preds, car_info)
        
        self.assertFalse(result)


class ScheduleChargeTest(unittest.TestCase):
    
    def test_low_high_low_8h_stay(self):

        preds = [100.0, 150.0, 200.0, 350.0, 450.0, 400.0, 200.0, 200.0, 350.0, 450.0, 450.0, 450.0, 500.0, 450.0, 350.0, 390.0, 300.0, 250.0, 200.0, 150.0, 150.0, 150.0, 100.0, 100.0]
        
        start = datetime.datetime.today()
        start = datetime.datetime.strptime(str(start).split('.')[0], '%Y-%m-%d %H:%M:%S')
        start = start.isoformat()
        end = datetime.datetime.today() + datetime.timedelta(hours=8)
        end = datetime.datetime.strptime(str(end).split('.')[0], '%Y-%m-%d %H:%M:%S')
        end = end.isoformat()
        print(start, end)
        car_info = {
            "id": "ac1f2001-7e59-1f19-817e-597fd23e0000",
            "parkingSpotId": "c0a83201-8cxc-1hnn-237c-dfjr4rcc05047",
            "carDTO": {
                "id": "c0a83801-7d96-17c0-817d-96e85f600003",
                "licensePlate": "WZ1463Y",
                "ownerId": "c0a83801-7cdc-1fd9-817c-dc301d4f0001",
                "carModel": {
                    "id": "c0a83801-7cdc-1fd9-817g-fc381e4f0003",
                    "manufacturer": "MINI",
                    "name": "Electric",
                    "batteryCapacity": 100
                }
            },
            "userPreferences": [],
            "startTime": str(start),
            "endTime": str(end),
            "battery": 40
        } 
        
        result = schedule_charge(car_info, preds)   
        self.assertEqual(result, 1)        

    def test_high_low_8h_stay_low_battery(self):

        preds = [400.0, 450.0, 400.0, 350.0, 450.0, 200.0, 400.0, 150.0, 350.0, 450.0, 450.0, 450.0, 500.0, 450.0, 350.0, 390.0, 300.0, 250.0, 200.0, 150.0, 150.0, 150.0, 100.0, 100.0]
        
        start = datetime.datetime.today()
        start = datetime.datetime.strptime(str(start).split('.')[0], '%Y-%m-%d %H:%M:%S')
        start = start.isoformat()
        end = datetime.datetime.today() + datetime.timedelta(hours=8)
        end = datetime.datetime.strptime(str(end).split('.')[0], '%Y-%m-%d %H:%M:%S')
        end = end.isoformat()
        print(start, end)
        car_info = {
            "id": "ac1f2001-7e59-1f19-817e-597fd23e0000",
            "parkingSpotId": "c0a83201-8cxc-1hnn-237c-dfjr4rcc05047",
            "carDTO": {
                "id": "c0a83801-7d96-17c0-817d-96e85f600003",
                "licensePlate": "WZ1463Y",
                "ownerId": "c0a83801-7cdc-1fd9-817c-dc301d4f0001",
                "carModel": {
                    "id": "c0a83801-7cdc-1fd9-817g-fc381e4f0003",
                    "manufacturer": "MINI",
                    "name": "Electric",
                    "batteryCapacity": 100
                }
            },
            "userPreferences": [],
            "startTime": str(start),
            "endTime": str(end),
            "battery": 5
        } 
        
        result = schedule_charge(car_info, preds)   
        self.assertEqual(result, 0)  


    def test_high_low_8h_stay_high_battery(self):

        preds = [500.0, 400.0, 400.0, 350.0, 450.0, 200.0, 400.0, 150.0, 350.0, 450.0, 450.0, 450.0, 500.0, 450.0, 350.0, 390.0, 300.0, 250.0, 200.0, 150.0, 150.0, 150.0, 100.0, 100.0]
        
        start = datetime.datetime.today()
        start = datetime.datetime.strptime(str(start).split('.')[0], '%Y-%m-%d %H:%M:%S')
        start = start.isoformat()
        end = datetime.datetime.today() + datetime.timedelta(hours=8)
        end = datetime.datetime.strptime(str(end).split('.')[0], '%Y-%m-%d %H:%M:%S')
        end = end.isoformat()
        print(start, end)
        car_info = {
            "id": "ac1f2001-7e59-1f19-817e-597fd23e0000",
            "parkingSpotId": "c0a83201-8cxc-1hnn-237c-dfjr4rcc05047",
            "carDTO": {
                "id": "c0a83801-7d96-17c0-817d-96e85f600003",
                "licensePlate": "WZ1463Y",
                "ownerId": "c0a83801-7cdc-1fd9-817c-dc301d4f0001",
                "carModel": {
                    "id": "c0a83801-7cdc-1fd9-817g-fc381e4f0003",
                    "manufacturer": "MINI",
                    "name": "Electric",
                    "batteryCapacity": 100
                }
            },
            "userPreferences": [],
            "startTime": str(start),
            "endTime": str(end),
            "battery": 90
        } 
        
        result = schedule_charge(car_info, preds)   
        self.assertEqual(result, -1)

    def test_high_low_2h_stay_low_battery(self):

        preds = [500.0, 450.0, 200.0, 150.0, 150.0, 400.0, 200.0, 200.0, 350.0, 450.0, 450.0, 450.0, 500.0, 450.0, 350.0, 390.0, 300.0, 250.0, 200.0, 150.0, 150.0, 150.0, 100.0, 100.0]
        
        start = datetime.datetime.today()
        start = datetime.datetime.strptime(str(start).split('.')[0], '%Y-%m-%d %H:%M:%S')
        start = start.isoformat()
        end = datetime.datetime.today() + datetime.timedelta(hours=2)
        end = datetime.datetime.strptime(str(end).split('.')[0], '%Y-%m-%d %H:%M:%S')
        end = end.isoformat()
        print(start, end)
        car_info = {
            "id": "ac1f2001-7e59-1f19-817e-597fd23e0000",
            "parkingSpotId": "c0a83201-8cxc-1hnn-237c-dfjr4rcc05047",
            "carDTO": {
                "id": "c0a83801-7d96-17c0-817d-96e85f600003",
                "licensePlate": "WZ1463Y",
                "ownerId": "c0a83801-7cdc-1fd9-817c-dc301d4f0001",
                "carModel": {
                    "id": "c0a83801-7cdc-1fd9-817g-fc381e4f0003",
                    "manufacturer": "MINI",
                    "name": "Electric",
                    "batteryCapacity": 100
                }
            },
            "userPreferences": [],
            "startTime": str(start),
            "endTime": str(end),
            "battery": 15
        } 
        
        result = schedule_charge(car_info, preds)   
        self.assertEqual(result, 1)


    def test_high_low_2h_stay_high_battery(self):

        preds = [500.0, 450.0, 200.0, 150.0, 150.0, 400.0, 200.0, 200.0, 350.0, 450.0, 450.0, 450.0, 500.0, 450.0, 350.0, 390.0, 300.0, 250.0, 200.0, 150.0, 150.0, 150.0, 100.0, 100.0]
        
        start = datetime.datetime.today()
        start = datetime.datetime.strptime(str(start).split('.')[0], '%Y-%m-%d %H:%M:%S')
        start = start.isoformat()
        end = datetime.datetime.today() + datetime.timedelta(hours=2)
        end = datetime.datetime.strptime(str(end).split('.')[0], '%Y-%m-%d %H:%M:%S')
        end = end.isoformat()
        print(start, end)
        car_info = {
            "id": "ac1f2001-7e59-1f19-817e-597fd23e0000",
            "parkingSpotId": "c0a83201-8cxc-1hnn-237c-dfjr4rcc05047",
            "carDTO": {
                "id": "c0a83801-7d96-17c0-817d-96e85f600003",
                "licensePlate": "WZ1463Y",
                "ownerId": "c0a83801-7cdc-1fd9-817c-dc301d4f0001",
                "carModel": {
                    "id": "c0a83801-7cdc-1fd9-817g-fc381e4f0003",
                    "manufacturer": "MINI",
                    "name": "Electric",
                    "batteryCapacity": 100
                }
            },
            "userPreferences": [],
            "startTime": str(start),
            "endTime": str(end),
            "battery": 85
        } 
        
        result = schedule_charge(car_info, preds)   
        self.assertEqual(result, 1)


if __name__ == '__main__':
    unittest.main()