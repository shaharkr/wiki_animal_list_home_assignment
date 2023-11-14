import requests
from configurator import Configurator


class WebExtractor:
    def send_get_request(url: str, headers: dict = {}, attribute_needed: str = None) -> requests.Response:
        try:
            response = requests.get(url=url, headers=headers)
            # check if status code is valid
            if response.status_code not in range(200, 300):
                raise Exception(f"Status code:{response.status_code}. Text:{response.text}")
            
            
            if attribute_needed is not None:
                # spesific attribute of the response
                return getattr(response, attribute_needed)
            else:
                return response
        
        except Exception as e:
            raise Exception(f"Failure sending GET request- ERROR:{str(e)}")