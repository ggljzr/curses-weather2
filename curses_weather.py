import curses
import curses_gui as cg
import icons
import time
import utils


LOC_WIN_SIZE_ROWS = 7
LOC_WIN_SIZE_COLS = 14

DAY_WIDTH = 12

class Location_window(cg.Window):

    def __init__(self):
        cg.Window.__init__(self, LOC_WIN_SIZE_ROWS,
                           LOC_WIN_SIZE_COLS, 0, 0, 'Location')

    def draw_location(self, location):

        str_country = "Country: {}".format(location.country)
        str_lon = "Lon: {}".format(location.lon)
        str_lat = "Lat: {}".format(location.lat)

        try:
            self.window.addstr(2, 1, location.city, curses.A_BOLD)
            self.window.addstr(3, 1, str_lon, curses.color_pair(cg.PAIR_CYAN))
            self.window.addstr(4, 1, str_lat, curses.color_pair(cg.PAIR_CYAN))
            self.window.addstr(5, 1, str_country, curses.color_pair(cg.PAIR_GREEN))
        except curses.error:
            pass

        self.refresh()


class Current_weather_window(cg.Window):

    def __init__(self, term_cols):
        cg.Window.__init__(self, LOC_WIN_SIZE_ROWS, term_cols -
                           LOC_WIN_SIZE_COLS - 1, LOC_WIN_SIZE_COLS + 1, 0, 'Current weather')

    def draw_current_weather(self, current_weather_data):

        temperature = 'Temperature: {} C '.format(
            current_weather_data['main']['temp'])
        pressure = 'Pressure: {} hPa '.format(
            current_weather_data['main']['pressure'])
        humidity = 'Humidity: {} % '.format(
            current_weather_data['main']['humidity'])
        wind = 'Wind: {} ms '.format(current_weather_data['wind']['speed'])

        sunriseUnix = current_weather_data['sys']['sunrise']
        sunsetUnix = current_weather_data['sys']['sunset']

        sunrise = 'Sunrise: ' + utils.getTimeFormat(sunriseUnix)
        sunset = 'Sunset:  ' + utils.getTimeFormat(sunsetUnix)
        date = utils.getDateFormat(sunsetUnix)
        curWeather = current_weather_data['weather'][0]['description']

        icon = utils.getIcon(current_weather_data['weather'][0]['icon'])

        maxLen = max([len(temperature), len(
            pressure), len(humidity), len(wind)])

        temperature = utils.padEntry(temperature, maxLen, ':', ' ')
        pressure = utils.padEntry(pressure, maxLen, ':', ' ')
        humidity = utils.padEntry(humidity, maxLen, ':', ' ')
        wind = utils.padEntry(wind, maxLen, ':', ' ')

        rightOffset = self.columns - maxLen - 1
        leftOffset = 1

        self.window.clear()
        self.drawWindowBorder()

        try:
            self.window.addstr(2, rightOffset, temperature,
                               curses.color_pair(cg.PAIR_YELLOW))
            self.window.addstr(3, rightOffset, pressure,
                               curses.color_pair(cg.PAIR_YELLOW))
            self.window.addstr(4, rightOffset, humidity,
                               curses.color_pair(cg.PAIR_YELLOW))
            self.window.addstr(5, rightOffset, wind,
                               curses.color_pair(cg.PAIR_YELLOW))

        except curses.error:
            pass

        try:
            self.window.addstr(2, leftOffset + icons.iconWidth +
                               1, date, curses.color_pair(cg.PAIR_CYAN))
            self.window.addstr(3, leftOffset + icons.iconWidth + 1,
                               curWeather, curses.color_pair(cg.PAIR_CYAN))
            self.window.addstr(4, leftOffset + icons.iconWidth + 1,
                               sunrise, curses.color_pair(cg.PAIR_CYAN))
            self.window.addstr(5, leftOffset + icons.iconWidth + 1,
                               sunset, curses.color_pair(cg.PAIR_CYAN))

        except curses.error:
            pass

        try:
            icons.drawIcon(leftOffset, 1, icon, self.window)
        except curses.error:
            pass

        self.refresh()


class Forecast_window(cg.Window):

    def __init__(self, term_rows, term_cols):
        cg.Window.__init__(self, term_rows - LOC_WIN_SIZE_ROWS - 1,
                           term_cols, 0, LOC_WIN_SIZE_ROWS, 'Forecast')
    
    def drawDay(self, yPos, xPos, dayData):

        date = utils.getDateFormat(dayData['dt'])
        weekday = utils.getWeekDay(dayData['dt']) 
        time = ' ' + utils.getTimeFormat(dayData['dt'])
        icon = utils.getIcon(dayData['weather'][0]['icon'])

        temp = '{} °C'.format(dayData['main']['temp'])
        humidity = 'Hum: {} %'.format(dayData['main']['humidity'])
        pressure = '{} hPa'.format(dayData['main']['pressure'])


        #refactor: cenetring weekday
        try:
            self.window.addstr(
                yPos, xPos, date, curses.A_BOLD | curses.color_pair(cg.PAIR_GREEN))
            self.window.addstr(yPos + 1, xPos + 4, weekday, curses.A_BOLD | curses.color_pair(cg.PAIR_CYAN))
            self.window.addstr(yPos + 2, xPos, time,
                                  curses.A_BOLD | curses.color_pair(cg.PAIR_YELLOW))
            icons.drawIcon(xPos, yPos + 3, icon, self.window)
            self.window.addstr(yPos + icons.iconHeight + 4, xPos, temp,
                                  curses.color_pair(cg.PAIR_GREEN))
            self.window.addstr(yPos + icons.iconHeight + 5, xPos, humidity,
                                  curses.color_pair(cg.PAIR_GREEN))
            self.window.addstr(yPos + icons.iconHeight + 6, xPos, pressure,
                                  curses.color_pair(cg.PAIR_GREEN))
        except curses.error:
            pass

    def draw_forecast(self, forecast_data, daily):

        days = forecast_data['list']
       
        if daily == True:
            days = days[0::8]
        else:
            days = days[0::2]

        dayWidth = DAY_WIDTH
        daysNum = self.columns // dayWidth

        days = days[:daysNum]
        dayX = (self.columns - daysNum * dayWidth) // 2
        dayY = 3

        self.window.clear()
        self.drawWindowBorder()

        for day in days:
            self.drawDay(dayY, dayX, day)
            dayX = dayX + dayWidth

        self.refresh()


    
class Info_window(object):

    def __init__(self, term_rows, term_cols):
        self.rows = term_rows
        self.cols = term_cols
        self.window = curses.newwin(1, term_cols, term_rows - 1, 0)

    def update(self, cur_loc, loc_num):
        navInf = '<F5 refresh><Prev {}/{} Next> '.format(cur_loc, loc_num)
        try:
            self.window.addstr(0, 1, 'Weather from www.openweathermap.org',
                              curses.A_BOLD | curses.color_pair(cg.PAIR_CYAN))
            self.window.addstr(0, self.cols - len(navInf), navInf,
                              curses.A_BOLD | curses.color_pair(cg.PAIR_RED))
        except:
            pass
        self.window.refresh()


