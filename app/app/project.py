from flask import Flask, render_template, request, send_from_directory
import requests
import os
import datetime
import json

API_KEY = os.environ.get("API_KEY")

bg_color = os.environ.get("BG_COLOR")
if not bg_color: bg_color = "white"

app = Flask(__name__)

def name_to_cord(user_input, cca2):
    '''
    This function receives the user input (location and country code) from the form page,
    and sends the received location information to the cord_to_weather function to get the weather data.
    Finally, it returns the weather data.
    '''
    # print(user_input, flush=True)
    response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={user_input},{cca2}&limit=1&appid={API_KEY}")
    location_data = response.json()
    # print(location_data, flush=True)
    if location_data and type(location_data) != dict:            # Check if the location data is valid returns an error massage if false
        lat_cord = location_data[0]['lat']
        lon_cord = location_data[0]['lon']                       # Get the latitude and longitude coordinates of the location
        city = location_data[0]['name']
        country = location_data[0]['country']
        final_result = cord_to_weather(lat_cord, lon_cord, city, country) # Call the cord_to_weather function to get the weather data
        return final_result                                      # Return the weather data    
    else: 
        return 'invalid location'

def cord_to_weather(lat_cord, lon_cord, city, country):
    '''
    This function receives the latitude and longitude coordinates from the name_to_cord function
    and returns the actual weather data for the specified location.
    '''
    # print('here22', flush=True)
    # print(lat_cord,lon_cord, flush=True)
    response = requests.get(f"https://api.openweathermap.org/data/3.0/onecall?lat={lat_cord}&lon={lon_cord}&units=metric&appid={API_KEY}")
    weather_data = response.json()
    # print(weather_data, flush=True)
    # print(weather_data, flush=True)
    # Get the daily weather data
    days = weather_data["daily"]
    result_dict = {}
    day_count = 0
    for day in days:
        temps = day["temp"]
        day_temp = temps["day"]
        night_temp = temps["night"]
        hum = day["humidity"]
        time = day["dt"]
        weather_icon = day["weather"][0]["icon"]
        weather_status = day["weather"][0]["main"]
        date = datetime.datetime.fromtimestamp(time).date()
        day_result = {str(day_count): {'city': city, 'country':country, 'date': str(date), 'day': day_temp,
            'night': night_temp, 'humidity': hum, 'weather_icon': weather_icon, 'weather_status': weather_status}} #Store the weather data for each day in a dictionary
        result_dict.update(day_result)
        todays_poam = ''
        # if day_count == 0:
        #      todays_poam = poam(city, temps, weather_status)
        day_count += 1
    poam_dict = {'todays_poam': todays_poam}
    result_dict.update(poam_dict)
    # print(result_dict, flush=True)
    extract_and_save_data(result_dict)
    return result_dict


@app.route("/", methods =["GET", "POST"])
def form_page():
    if request.method == "POST":
        city = request.form.get("location")
        country = request.form.get("country")
        switch = 0
        if city == '':
            if country == '':
                return render_template("form.html",error = 'please enter some input' ) #returns an error massage if both city and country are empty
            else:
                c_city = requests.get(f"https://restcountries.com/v3.1/name/{country}").json()
                switch = 1
        else:
            c_city = ''
        #c_city = ''
        if type(c_city) != list:
            cca2 = '' # if we dont get a country name sets the cca2 to nothing
        else:
            cca2 = c_city[0]["cca2"] # if we do extracts the cca2
            if switch == 1:          # and if we haven't recived a city extracts the capital city
                city = c_city[0]["capital"][0]
        # print('here', flush=True)
        response = name_to_cord(city, cca2) 
        if type(response) == dict:          #checks that we got a valid responce otherwise returns the error msg
            # print(response,city, flush=True)
            return render_template("weather.html", location = city, response = response)
        else: return render_template("form.html", error = response)
    return render_template("form.html" )

#response = {'0': {'city': 'london', 'date': '2023-02-07', 'day': 11.35, 'night': 11.07, 'humidity': 52, 'weather_icon': '10d'}, '1': {'city': 'london', 'date': '2023-02-08', 'day': 8.97, 'night': 9.86, 'humidity': 65, 'weather_icon': '10d'}, '2': {'city': 'london', 'date': '2023-02-09', 'day': 10.68, 'night': 11.91, 'humidity': 56, 'weather_icon': '10d'}, '3': {'city': 'london', 'date': '2023-02-10', 'day': 11.8, 'night': 12.43, 'humidity': 52, 'weather_icon': '10d'}, '4': {'city': 'london', 'date': '2023-02-11', 'day': 11.39, 'night': 12.94, 'humidity': 53, 'weather_icon': '01d'}, '5': {'city': 'london', 'date': '2023-02-12', 'day': 11.87, 'night': 12.3, 'humidity': 51, 'weather_icon': '10d'}, '6': {'city': 'london', 'date': '2023-02-13', 'day': 12.76, 'night': 13.42, 'humidity': 40, 'weather_icon': '01d'}, '7': {'city': 'london', 'date': '2023-02-14', 'day': 12.53, 'night': 12.3, 'humidity': 44, 'weather_icon': '01d'}}


def extract_and_save_data(data):
    extracted_data = {}

    for key, value in data.items():
        if key.isdigit():
            date = value['date']
            city = value['city']
            
            if date not in extracted_data:
                extracted_data[date] = []
            
            extracted_data[date].append(city)
    
    # Save the extracted data as a JSON file
    os.makedirs('data', exist_ok=True)

    filename = 'extracted_data.json'
    filepath = os.path.join('./data/', filename)  # Assuming a 'data' directory to store the JSON file
    
    if not os.path.exists(filepath):
        # Create a new JSON file with initial structure
        with open(filepath, 'w') as file:
            file.write('[\n]')
    
    # Append data to the existing JSON file
    with open(filepath, 'r+') as file:
        file.seek(0, os.SEEK_END)
        file.seek(file.tell() - 2, os.SEEK_SET)
        file.truncate()
        
        if file.tell() > 1:
            file.write(',\n')
        
        json.dump(extracted_data, file)
        file.write('\n]')

@app.route("/history")
def download_history():
    # Assuming the JSON files are stored in the 'data' directory
    filename = "extracted_data.json"  # Replace with the desired filename
    directory = "./data"
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r') as file:
        extracted_data = json.load(file)

    return render_template('history.html', extracted_data=extracted_data,bg_color=bg_color)

if __name__ == "__main__":
    app.run()
    
    
    
    
    
    
    
    
