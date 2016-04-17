import curses
import curses_gui as cg
import curses_weather as cw
import locale
import subprocess
import api_access

API_KEY = 'c59469dd4ae25cd8f1fd8602fc296718'

if __name__ == '__main__':

    term_rows, term_cols = subprocess.check_output(['stty', 'size']).split()
    term_rows = int(term_rows)
    term_cols = int(term_cols)

    api = api_access.Access(API_KEY, 'metric')

    current_data, location = api.request_current_data('Prague')
    forecast_data = api.request_forecast_data('Prague')

    stdscr = cg.initCurses();

    loc_win = cw.Location_window()
    cur_win = cw.Current_weather_window(term_cols)
    forecast_win = cw.Forecast_window(term_rows, term_cols)
    info_window = cw.Info_window(term_rows, term_cols)
    stdscr.refresh()

    loc_win.draw_location(location)
    cur_win.draw_current_weather(current_data)
    forecast_win.draw_forecast(forecast_data, 0)
    info_window.refresh()
    while True:
        c = stdscr.getch()
        if c == ord('q'):
            break

    cg.endCurses(stdscr)
