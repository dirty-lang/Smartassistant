import wikipediaapi
import requests
from gtts import gTTS
import os

# Weather Function
def get_weather(city):
    api_key = "87480a5ba12cf8befe50b089f19a6737"  # OpenWeatherMap API Key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        try:
            weather = data['weather'][0]['description']
            temperature = data['main']['temp']
            return f"The weather in {city} is {weather} with a temperature of {temperature}°C."
        except KeyError:
            return "Sorry, I couldn't fetch the weather details for this city. Please try again."
    else:
        return f"Error: {response.status_code}. Unable to fetch weather data. Check the city name or try later."

# News Function
def get_news():
    news_api_key = "pub_63562af1b1654006a09ca31870395cbe5a08c"  # NewsData API Key
    url = f"https://newsdata.io/api/1/news?apikey={news_api_key}&q=news&country=in"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get('results', [])
        if articles:
            news = "\n".join([article['title'] for article in articles[:5]])
            return news
        else:
            return "No news found."
    else:
        return "Sorry, I couldn't fetch the news."

# Wikipedia Function
def get_wikipedia_summary(query):
    user_agent = "MyWikipediaBot/1.0 (myemail@example.com)"
    wiki = wikipediaapi.Wikipedia(
        language='en',
        user_agent=user_agent
    )
    page = wiki.page(query)
    if page.exists():
        return page.summary[:500] + "..."
    else:
        return "Sorry, I couldn't find any information on that topic."

# Text-to-Speech Function using gTTS
def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    os.system("mpg321 output.mp3")  # Linux command to play audio
    # For Windows or macOS, you can use 'playsound' instead of mpg321:
    # from playsound import playsound
    # playsound('output.mp3')

# Main Function
def main():
    print("Hi, I am your Intelligent Assistant! How can I help you?")
    while True:
        print("\nCommands: 'weather', 'news', 'wiki', 'exit'")
        command = input("Enter your command: ").lower()

        if "weather" in command:
            city = input("Which city's weather do you want to know? ")
            weather_info = get_weather(city)
            print(weather_info)
            speak(weather_info)  # Speak the weather info
        elif "news" in command:
            print("Here are the top news headlines:")
            news_info = get_news()
            print(news_info)
            speak(news_info)  # Speak the news headlines
        elif "wiki" in command:
            query = input("What topic should I search on Wikipedia? ")
            wiki_info = get_wikipedia_summary(query)
            print(wiki_info)
            speak(wiki_info)  # Speak the Wikipedia summary
        elif "exit" in command:
            print("Goodbye!")
            speak("Goodbye!")  # Speak the exit message
            break
        else:
            print("Sorry, I didn't understand that command.")
            speak("Sorry, I didn't understand that command.")  # Speak if command is not recognized

# Run the assistant
main()
