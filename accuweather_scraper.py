from bs4 import BeautifulSoup
import requests
import pandas as pd

district_list=[]
country_list=[]
morning=[]
afternoon=[]
evening=[]
night=[]
feels_list=[]

high_low_list=[]
wind_speed_list=[]
humidity_list=[]
dewPoint_list=[]
pressure_list=[]
uv_index_list=[]
visibility_list=[]
moonPhase_list=[]


hyperlink_list = ['https://weather.com/weather/today/l/bd3ce777ddce75bafeceeeb193d0c00b1b5a1a663d5899b674dc4d8aa8b4692d',
                  'https://weather.com/weather/today/l/2e8d8d50ee900ae59e114469fe74f03f8bdb14454f1ceeff504d87a98b84b9b7',
                  'https://weather.com/weather/today/l/a4bf563aa6c1d3b3daffff43f51e3d7f765f43968cddc0475b9f340601b8cc26',
                  'https://weather.com/weather/today/l/a28b7610302e8eb27bef2d081530cbbe826326e94fa0216223d07246138cc364',
                  'https://weather.com/weather/today/l/3e301eacc5e5837f2015b55650fc7d39ff9b778be1c4e5c7bd013c45532a2896']
for link in hyperlink_list:
    html_file = requests.get(link).text
    soup = BeautifulSoup(html_file, 'lxml')
    destination=soup.find('h1',class_="CurrentConditions--location--kyTeL").text.replace(' ','').strip().split(",")
    district_name=destination[0]
    country_name=destination[-1]
    district_list.append(district_name)
    country_list.append(country_name)

    avg_weatherBox=soup.find('ul',class_="WeatherTable--columns--OWgEl WeatherTable--wide--3dFXu")
    weather_list=avg_weatherBox.find_all('li')
    for index,weather in enumerate(weather_list):
        spans=weather.find_all('span')
        if index==0:
            morning.append(spans[1].text)
        elif index==1:
            afternoon.append(spans[1].text)
        elif index==2:
            evening.append(spans[1].text)
        elif index==3:
            night.append(spans[1].text)

    feelsLike=soup.find('span',class_='CurrentConditions--tempValue--3a50n').text.replace(' ','').strip()
    feels_list.append(feelsLike)

    infoBox=soup.find_all('div',class_='WeatherDetailsListItem--wxData--2s6HT')
    high_low=infoBox[0].text.strip()
    wind_direction=infoBox[1].title.text
    wind_speed=infoBox[1].text.replace(wind_direction,'').strip()
    humidity=infoBox[2].text.strip()
    dewPoint=infoBox[3].text.strip()
    pressure_direction=infoBox[4].title.text
    pressure=infoBox[4].text.replace(pressure_direction,'').strip()
    uv_index=infoBox[5].text.strip()
    visibility=infoBox[6].text.strip()
    moonPhase=infoBox[7].text.strip()

    high_low_list.append(high_low)
    wind_speed_list.append(wind_speed)
    humidity_list.append(humidity)
    dewPoint_list.append(dewPoint)
    pressure_list.append(pressure)
    uv_index_list.append(uv_index)
    visibility_list.append(visibility)
    moonPhase_list.append(moonPhase)

weather_dataframe=pd.DataFrame(
    {
        "District Name":district_list,
        "Country Name":country_list,
        "Morning":morning,
        "Afternoon":afternoon,
        "Evening":evening,
        "Night":night,
        "Feelings Like":feels_list,
        "High/Low":high_low_list,
        "Wind":wind_speed_list,
        "Humidity":humidity_list,
        "Dewpoint":dewPoint_list,
        "Pressure":pressure_list,
        "UV Index":uv_index_list,
        "Visibility":visibility_list,
        "Moon Phase":moonPhase_list
    }
)
weather_dataframe.to_excel('weather_scrapes/weather_excel2.xlsx')
print('weather scraped')