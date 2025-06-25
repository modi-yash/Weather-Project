import sys
import os
# Weather.py
class City:
    def __init__(self, name, country, lat, lon, temp, weather):
        self.name = name
        self.country = country
        self.lat = lat
        self.lon = lon
        self.temp = temp
        self.weather = weather
def clear_terminal():
    # Clears the terminal screen.
    _ = os.system('cls') if os.name == 'nt' else os.system('clear')
    #os.system('cls') if os.name == 'nt' else os.system('clear')

try:
    clear_terminal()
except Exception as e:
    print("An error occurred while trying to clear the terminal:", e)

# Weather App
is_fahrenheit = False # Default to Celsius if not determined
app_id_open_weather = ("apid", ) # OpenWeatherMap API key
try:
    import requests # type: ignore
    # Checking if should be Fahrenheit or Celsius
    try:
        
        responseCF = requests.get(f"http://ip-api.com/json/")
        dataCF = responseCF.json()
        
        if responseCF.status_code == 200:
            dataCF = responseCF.json()
            if dataCF["countryCode"] == "US" or dataCF["countryCode"] == "LR" or dataCF["countryCode"] == "FM" or dataCF["countryCode"] == "VI" or dataCF["countryCode"] == "KY" or dataCF["countryCode"] == "MH":
                is_fahrenheit = True
        else:
            print("Could not retrieve your location. Status code:", responseCF.status_code)
        
        # End of Fahrenheit or Celsius check

        print("Welcome to the Weather App!", "Type \'quit\' to quit at any time.\n")
        while(True):
            
            city = input("Enter the name of the location: ").strip().lower()
            print()

            if(city == "exit" or city == "quit" or city == "leave" or city == "stop" or city == "end"):
                # Exit the program gracefully
                print("Exiting the Weather App. Goodbye!")
                sys.exit(0)
                
            try:
                response_weather = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={app_id_open_weather[0]}&units={'imperial' if is_fahrenheit else 'metric'}")
            
            # Handle potential errors in the request
            except requests.exceptions.ConnectionError:
                print("Failed to connect to the weather service. Please check your internet connection.")
            except requests.exceptions.Timeout:
                print("The request timed out. Please try again later.")
            except Exception as e:
                print("An unknown error occurred:", e)
            else:
                # If the request was successful, process the response
                # Check if the response is valid
                if(response_weather.status_code == 200):
                    data_weather = response_weather.json()
                    # name, country, lat, lon, temp, weather
                    city = City(data_weather["name"], data_weather["sys"]["country"], data_weather["coord"]["lat"], data_weather["coord"]["lon"], data_weather["main"]["temp"], data_weather["weather"][0]["description"])
                    print(f"Weather in {city.name}, {city.country} is {city.temp}°{'F' if is_fahrenheit else 'C'} with {city.weather}.\n","\n")
                elif(response_weather.status_code == 404):
                    print(f"City '{city}' not found. Please check the city name and try again.\n")
                else:
                    print(f"An error occurred: {response_weather.status_code} - {response_weather.reason}")
    
    #These only appear if there is an error 
    except requests.exceptions.ConnectionError:
        print("Failed to connect to the location service. Please check your internet connection.")
    except requests.exceptions.Timeout:
        print("The request timed out. Please try again later.")
    except Exception as e:
        print("An unknown error occurred:", e)
except ImportError:
    print("The 'requests' module is not installed. Please install it before running this script. You may install it by typing 'pip install requests' in your terminal.")
except Exception as e:
    print("An unexpected error occurred:", e)


# End of try block for requests import
