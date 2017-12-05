import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime

def open_linkedin(fname):
    
    
def clean_df(df, date_column):
    df[date_column] = pd.to_datetime(df[date_column]).dt.date
    df[date_column] = df[date_column] - pd.to_timedelta(7, unit='d')
    df_by_week = df.groupby([date_column]).count().reset_index()
    return df_by_week


def get_sent_receive_invites(df, direction_column):
    invites_sent = df[df[direction_column] == 'OUTGOING']
    invites_received = df[df[direction_column] == 'INCOMING']
    return invites_sent, invites_received


def plot(df, x,y, xlabel, ylabel, title, fig_size, fig_color):
    fig,ax= plt.subplots(nrows=1)
    ax.bar(df[x],df[y], color = fig_color)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.set_size_inches(fig_size)
    return


def import_recruiters_contacts(path):
    contacts_df = read_safely('./connections.csv')
    words = ['Recruiter', 'Talent', 'Sourcer', 'Recruiting']
    contacts_df['Position'] = contacts_df['Position'].dropna().apply(lambda x: 'Recruiter' if 
                                                   (any(word in x for word in words)) else x,1)
    recruiters_df = contacts_df[contacts_df['Position'] == 'Recruiter']
    return recruiters_df
