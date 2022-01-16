import unittest
from decision import *

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

        self.assertEqual(result['when_leaving'], 23)

    def test_when_leaving_miliseconds(self):
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
            "endTime": "2022-01-14T19:30:00.1772144",
            "battery": 40
        }
        result = get_car_info(car_info)
        
        self.assertEqual(result['when_leaving'], 19)

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

        result_load1, result_unload, result_load2 = sale_potential(preds)
        
        self.assertCountEqual(result_load1, [(0, 70.0), (1, 150.0), (2, 150.0)]) 
        self.assertCountEqual(result_unload, [(3, 390.0), (4, 390.0), (5, 390.0), (6, 300.0)])
        self.assertCountEqual(result_load2, [(7, 150.0), (8, 169.73), (9, 190.2), (10, 200.0)])


if __name__ == '__main__':
    unittest.main()