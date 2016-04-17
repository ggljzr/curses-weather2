import curses
import curses_gui as cg
import curses_weather as cw
import locale
import subprocess
import api_access
import pytoml as toml

loc_win = None
cur_win = None
fore_win = None
info_win = None

config = {}
daily = False

def refresh_weather(current_weather_data, forecast_weather_data, location):
    loc_win.draw_location(location)
    cur_win.draw_current_weather(current_weather_data)
    fore_win.draw_forecast(forecast_data, daily)

if __name__ == '__main__':

    term_rows, term_cols = subprocess.check_output(['stty', 'size']).split()
    term_rows = int(term_rows)
    term_cols = int(term_cols)

    if term_rows < cg.MIN_ROWS or term_cols < cg.MIN_COLS:
        print("requires minimal terminal size {}x{} (yours {}x{})".format(
            cg.MIN_COLS, cg.MIN_ROWS, term_col, term_rows))
        sys.exit()

    # reading config
    with open('config.toml') as config_file:
        config = toml.load(config_file)

    api = api_access.Access(config['api']['key'], config['weather']['units'])

    current_data, location = api.request_current_data(
        config['weather']['locations'][0])
    forecast_data = api.request_forecast_data(
        config['weather']['locations'][0])

    current_loc = 0
    loc_num = len(config['weather']['locations'])

    stdscr = cg.initCurses()
    daily = bool(config['weather']['daily'])

    loc_win = cw.Location_window()
    cur_win = cw.Current_weather_window(term_cols)
    fore_win = cw.Forecast_window(term_rows, term_cols)
    info_win = cw.Info_window(term_rows, term_cols)
    stdscr.refresh()

    refresh_weather(current_data, forecast_data, location)
    info_win.update(current_loc + 1, loc_num)

    while True:
        c = stdscr.getch()
        if c == ord('q'):
            break
        if c == curses.KEY_F5:
            current_data, location = api.request_current_data(
                config['weather']['locations'][current_loc])
            forecast_data = api.request_forecast_data(
                config['weather']['locations'][current_loc])
            refresh_weather(current_data, forecast_data, location)
        if c == curses.KEY_RIGHT:
            current_loc = (current_loc + 1) % loc_num
            current_data, location = api.request_current_data(
                config['weather']['locations'][current_loc])
            forecast_data = api.request_forecast_data(
                config['weather']['locations'][current_loc])
            refresh_weather(current_data, forecast_data, location)
            info_win.update(current_loc + 1, loc_num)
        if c == curses.KEY_LEFT:
            current_loc = (current_loc - 1) % loc_num
            current_data, location = api.request_current_data(
                config['weather']['locations'][current_loc])
            forecast_data = api.request_forecast_data(
                config['weather']['locations'][current_loc])
            refresh_weather(current_data, forecast_data, location)
            info_win.update(current_loc + 1, loc_num)

    cg.endCurses(stdscr)
