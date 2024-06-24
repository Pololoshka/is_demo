from integration_utils.bitrix_robots.models import BaseRobot
import requests
from datetime import datetime

from robot_currency.weather_const import WEATHER_CODES


class CurrencyRobot(BaseRobot):
    APP_DOMAIN = "touched-enhanced-monkey.ngrok-free.app"
    CODE = "currency_robot"
    NAME = "Показать прогноз погоды"
    USE_SUBSCRIPTION = True

    PROPERTIES = {
        "user": {
            "Name": {"ru": "Получатель"},
            "Value": {"ru": "Ответственный"},
            "Type": "user",
            "Required": "Y",
        },
        "city": {
            "Name": {"ru": "Город"},
            "Type": "string",
            "Required": "Y",
        },
    }

    RETURN_PROPERTIES = {
        "current_weather": {
            "Name": {"ru": "Погода"},
            "Type": "string",
            "Required": "Y",
        },
        "ok": {
            "Name": {"ru": "ok"},
            "Type": "bool",
            "Required": "Y",
        },
        "error": {
            "Name": {"ru": "error"},
            "Type": "string",
            "Required": "N",
        },
    }

    def process(self) -> dict:
        try:
            response_geolocation = requests.get(
                url="https://geocoding-api.open-meteo.com/v1/search",
                params={
                    "name": self.props["city"],
                    "count": "1",
                    "format": "json",
                    "language": "ru",
                },
            )

            geo_data = response_geolocation.json()["results"][0]

            response_weather = requests.get(
                url="https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": geo_data["latitude"],
                    "longitude": geo_data["longitude"],
                    "current_weather": "true",
                    "timezone": geo_data["timezone"],
                },
            )
            weather_data = response_weather.json()["current_weather"]
            result = (f"Сейчас {datetime.now().strftime('%H:%M %d.%m.%Y')} "
                      f"в городе {geo_data["name"]} {weather_data["temperature"]}°. "
                      f"{WEATHER_CODES[int(weather_data["weathercode"])]}.")
            self.dynamic_token.call_api_method(
                "bizproc.event.send",
                {
                    "event_token": self.event_token,
                    "return_values": {
                        "current_weather": result
                        ,
                    },
                },
            )

        except KeyError:
            self.dynamic_token.call_api_method(
                "bizproc.event.send",
                {
                    "event_token": self.event_token,
                    "return_values": {
                        "current_weather": None,
                    },
                },
            )

        except Exception as exc:
            return dict(ok=False, error=str(exc))
        print(dict(ok=True))
        return dict(ok=True)
