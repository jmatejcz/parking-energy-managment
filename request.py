import  requests



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
            



    