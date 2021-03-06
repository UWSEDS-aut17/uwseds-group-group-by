import argparse
import arrow
import ics
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt


def _group(s, groups):
    """Group a string using regex groups.

    Parameters:
    -----------
    s: the string to group
    groups: a list of tuples of (regex pattern, replacement string)

    Returns:
    --------
    s: the group for the string
    """
    for pattern, replacement in groups:
        if pattern.match(s):
            return replacement
    return s


def _total_hours(seconds):
    """Converts seconds to hours.

    Parameters:
    -----------
    seconds: the total seconds

    Returns:
    --------
    the total hours as a float
    """
    return seconds / 3600.0


def _process_calendar(calendar_file):
    """Processes a calendar, grouping events by name.

    Parameters:
    -----------
    calendar_file: the ics calendar file
    start_date: the starting date, or None
    end_date: the end date, or None
    allday: if true, includes all day events in processing
    grouping_regex_strs: regular expressions for grouping patterns

    Returns:
    --------
    DataFrame
    cal_df : Calender DataFrame grouped by event
    """

    calendar = ics.Calendar(open(calendar_file).read())
    cal_df = pd.DataFrame(
        columns=['day', 'month', 'year', 'hour', 'event_name', 'duration'])
    groups = defaultdict(lambda: 0)
    total_seconds = 0
    i = 0
    for event in calendar.events:
        start_date = arrow.get(event.begin)
        end_date = arrow.get(event.end)
        cal_df.loc[i] = [start_date.datetime.day, start_date.datetime.month,
                         start_date.datetime.year,
                         start_date.datetime.hour,
                         event.name, event.duration.total_seconds()]
        i += 1

    return cal_df


def _valid_date(s):
    """Validates and converts a date as arrow-compatible.

    Parameters:
    -----------
    s: the string argument

    Returns:
    --------
        an arrow date

    Raises:
    -------
        ArgumentTypeError: if the date is invalid
    """
    try:
        return arrow.get(s)
    except TypeError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def plot(x, y, z, xlabel, ylabel, title, fig_size, fig_color, flag):
    """Plots gcal data
    Parameters
    ----------
    x : Gcal DataFrame
    x  : Data to plot on x-axis
    y  : Data to plot on y-axis
    xlabel : Label for x-axis
    ylabel : Label for y-axix
    fig_size : Size of output figure
    fig_color : Color for the bar chart
    flag: Gcal flag

    Returns
    -------
    Figure object of bar plots
    """
    try:
        fig, ax = plt.subplots(nrows=1)
        ax.bar(z[0:5], y[0:5], color=fig_color)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        if flag == '-T' or flag == '-L':
            plt.xticks(z[0:5], x[0:5])

        fig.set_size_inches(fig_size)
        return fig
    except:
        return "Can't generate plot"


def plot_data(x, y, x_column, y_column, xlabel, ylabel, title, fig_size,
              fig_color):
    """Plots gcal data
    Parameters
    ----------
    x : Gcal DataFrame
    x  : Data to plot on x-axis
    y  : Data to plot on y-axis
    xlabel : Label for x-axis
    ylabel : Label for y-axix
    title: Figure title
    fig_size : Size of output figure
    fig_color : Color for the bar chart

    Returns
    -------
    Figure object of bar plots
    """

    fig, ax = plt.subplots(nrows=1)
    ax.bar(x[x_column], x[y_column], color=fig_color)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(x[x_column], y)
    fig.set_size_inches(fig_size)
    return fig


def get_plots(cal_df):
    """ Calls plotter function and returns plot objects

    Parameters:
    -----------
    cal_df: Calender DataFrame

    Returns:
    Figure objects
    """

    # calendar_file = 'data/shsher@uw.edu.ics'

    cal_df['minutes'] = cal_df['duration'] / 60
    cal_df['hours'] = cal_df['duration'] / 3600

    # remove birthdays and events longer than 1 day
    cal_df = cal_df[~cal_df['event_name'].str.contains('birthday')]
    cal_df = cal_df[(cal_df['hours'] < 24) & (cal_df['hours'] > 0)]

    cal_df['count'] = 1
    cal_min = cal_df.groupby(['event_name'], as_index=False)[
        'event_name', 'count', 'minutes'].sum()
    cal_min.sort_values('minutes', ascending=False)
    cal_month = cal_df.groupby('month', as_index=False)['count'].sum()
    cal_month_time = cal_df.groupby('month', as_index=False)['hours'].sum()
    cal_year_time = cal_df.groupby('year', as_index=False)['count'].sum()

    months = ["January",
              "Febuary",
              "March",
              "April",
              "May",
              "June",
              "July",
              "August",
              "September",
              "October",
              "November",
              "December"]

    fig1 = plot_data(cal_month_time, months, 'month', 'hours', 'Month',
                     'Hours Spent ',
                     'Total Time Spent Per Month', (15, 5), '#db3236')

    fig2 = plot_data(cal_month, months, 'month', 'count', 'Month',
                     'Number of Events ',
                     'Total Events Per Month', (15, 5), '#db3236')

    fig3 = plot_data(cal_year_time, [2016, 2017, 2018], 'year', 'count',
                     'Year',
                     'Number of Events', 'Number of Events', (10, 5),
                     '#db3236')

    return [fig1, fig2, fig3]


def get_cal_dates(cal_df):
    """ Function to return calender dates dataframe to be used for overall plot

    Parameters:
    -----------
    cal_df : Calender dataframe

    Returns:
    --------
    DataFrame
    Datas when user had a calender event
    """

    cal_dates = pd.DataFrame(columns=['Date', 'count'])
    cal_dates['Date'] = pd.to_datetime(cal_df[['day', 'month', 'year']])
    cal_dates['count'] = 1
    return cal_dates
