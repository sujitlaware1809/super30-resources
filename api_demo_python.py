import requests

def get_weather(city, api_key):
    """Get current weather for a city using OpenWeatherMap API"""
    
    # Construct the API URL
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # For Celsius (use "imperial" for Fahrenheit)
    }
    
    # Make the API request
    response = requests.get(base_url, params=params)
    
    # Check if request was successful
    if response.status_code == 200:
        weather_data = response.json()
        return format_weather_data(weather_data)
    else:
        return f"Error: {response.status_code}, {response.text}"

def format_weather_data(data):
    """Format the API response into readable weather information"""
    
    main = data['main']
    weather = data['weather'][0]
    wind = data['wind']
    
    formatted_data = {
        "city": data['name'],
        "country": data['sys']['country'],
        "description": weather['description'],
        "temperature": main['temp'],
        "feels_like": main['feels_like'],
        "humidity": main['humidity'],
        "wind_speed": wind['speed'],
    }
    
    return formatted_data

def print_weather(weather_data):
    """Print weather data in a nice format"""
    
    print(f"Weather in {weather_data['city']}, {weather_data['country']}:")
    print(f"  Condition: {weather_data['description']}")
    print(f"  Temperature: {weather_data['temperature']}°C")
    print(f"  Feels like: {weather_data['feels_like']}°C")
    print(f"  Humidity: {weather_data['humidity']}%")
    print(f"  Wind speed: {weather_data['wind_speed']} m/s")

# Main program
if __name__ == "__main__":
    API_KEY = "3317bc82b3a9c7ef6bd96bf8f1834a58"  # Replace with your actual API key
    
    while True:
        city = input("Enter a city name (or 'quit' to exit): ")
        if city.lower() == 'quit':
            break
            
        weather = get_weather(city, API_KEY)
        if isinstance(weather, dict):
            print_weather(weather)
        else:
            print(weather)  # Print error message
        print()