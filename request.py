from email import header
from urllib import response
import  requests
import json



class WebClient():

    def __init__(self, url) -> None: 
        self.url = url


    def get_login_token(self, payload):
        url = self.url + '/login'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()['access_token']

    def get_reserations_list(self, access_token):
        url = self.url + '/parking/c0a83201-7cxc-1hh9-357c-dc3u1r4y00045/reservations'
        headers = {
        'Authorization': f'Bearer {access_token}'
        }

        response = requests.request("GET", url, headers=headers)
        return response.json()

    def put_battery(self, access_token, res_id, battery):
        url = self.url + '/parking/reservation/update'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        payload = json.dumps({
            "reservationId": f"{res_id}",
            "battery": battery
        })
        response = requests.request("PUT", url, headers=headers, data=payload)
        return response.json()    



    