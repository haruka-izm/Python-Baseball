import pandas as pd
import matplotlib.pyplot as plt

from frames import games, info, events

# to select all rows of the game DF that have a type of play,
# but not NP as an event
plays = games.query("type == 'play' & event != 'NP'")

plays.columns = ['type', 'inning', 'team', 'player', 'count', 'pitches',
                 'event', 'game_id', 'year']

# there are some spots in the event data where there are consecutive rows that represent the same at bat
# to calculate DER (plate appearances), these need to be removed
# shift(): removes the index a specified amount up or down
pa = plays.loc[plays['player'].shift() != plays['player'], ['year', 'game_id', 'inning', 'team', 'player']]

# to calc the plate appearances for each team for each game
pa = pa.groupby(['year', 'game_id', 'team']).size().reset_index(name='PA')

# set index
# in order to calc the DER of a team,
# need to reshape the data by the type of event that happened at each plate appearance
events = events.set_index(['year', 'game_id', 'team', 'event_type'])
events = events.unstack().fillna(0).reset_index()

events.columns = events.columns.droplevel()
events.columns = ['year', 'game_id', 'team', 'BB', 'E', 'H', 'HBP', 'HR', 'ROE', 'SO']

# remove the label of the index
events = events.rename_axis(None, axis='columns')

events_plus_pa = pd.merge(events, pa, how='outer', left_on=['year', 'game_id', 'team'], right_on=['year', 'game_id', 'team'])

# events_plus_pa: contains almost all of the info to calc the DER of each All-star team
defense = pd.merge(events_plus_pa, info)

# add a new column to the defense DF
defense.loc[:, 'DER'] = 1 - ((defense['H'] + defense['ROE']) /
                             (defense["PA"] - defense['BB'] - defense['SO'] - defense['HBP'] - defense['HR']))

# convert the year column of the defense DF to numeric values
defense.loc[:, 'year'] = pd.to_numeric(defense['year'])

der = defense.loc[defense['year'] >= 1978, ['year', 'defense', 'DER']]

der =  der.pivot(index='year', columns='defense', values='DER')

der.plot(x_compat=True, xtics=range(1978, 2018, 4), rot=45)
plt.show()















