import unittest
import parking



class TestParkingMethods(unittest.TestCase):

    def test_read_current_res_ids(self):
        pass

    def test_get_new_cars(self):
        ids = set()
        res_list = [{'id': 'c0a83801-7e1c-1d36-817e-1c700ff20000',
         'parkingSpotId': 'c0a83201-8cxc-1hnn-237c-dfjr4rcc05046',
          'carDTO': {'id': 'c0a83801-7d96-17c0-817d-96e85f600000', 'licensePlate': 'WA6724Y', 'ownerId': 'c0a83801-7cdc-1fd9-817c-dc301d4f0000',
           'carModel': {'id': 'c0a83801-7cdc-1fd9-817g-fc381e4f0000', 'manufacturer': 'Tesla', 'name': 'Model Y', 'batteryCapacity': 50}},
            'userPreferences': [], 'startTime': '2022-01-02T21:16:53.228302', 'endTime': None, 'battery': 10}]
        assert parking.get_new_cars(res_list, ids) == {'id': 'c0a83801-7e1c-1d36-817e-1c700ff20000',
         'parkingSpotId': 'c0a83201-8cxc-1hnn-237c-dfjr4rcc05046',
          'carDTO': {'id': 'c0a83801-7d96-17c0-817d-96e85f600000', 'licensePlate': 'WA6724Y', 'ownerId': 'c0a83801-7cdc-1fd9-817c-dc301d4f0000',
           'carModel': {'id': 'c0a83801-7cdc-1fd9-817g-fc381e4f0000', 'manufacturer': 'Tesla', 'name': 'Model Y', 'batteryCapacity': 50}},
            'userPreferences': [], 'startTime': '2022-01-02T21:16:53.228302', 'endTime': None, 'battery': 10}
        
        