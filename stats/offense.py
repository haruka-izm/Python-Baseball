import pandas as pd
import matplotlib.pyplot as plt

from data import games

# select all rows that have a type of play
plays = games[games['type'] == 'play']

# to easily access to certain columns, label them
plays.columns = ['type', 'inning', 'team', 'player', 'count', 'pitches', 'event', 'game_id', 'year']

# Q: what is the distribution of hits across innings?
# just need hits, singles, doubles, triples, and home runs
# select the rows where the event column's value starts with S, D, T, HR
# only return the inning and event columns
hits = plays.loc[plays['event'].str.contains('^(?:S(?!B)|D|T|HR)'), ['inning', 'event']]

# convert column type: str to numeric
hits.loc[:, 'inning'] = pd.to_numeric(hits.loc[:, 'inning'])

# replace dict
# the event column of the hits DF now contains event info of various confs for later use
replacements = {r'^S(.*)': "single", r'^D(.*)': 'double', r'^T(.*)': 'triple', r'^HR(.*)': 'hr'}

# call the replace func on the hits['event']
hit_type = hits['event'].replace(replacements, regex=True)

# to add a new column
hits = hits.assign(hit_type=hit_type)

# group the hits DF by inning and hit_type
# size(): count the num of hits per inning
# then reset the index of the resulting DF, arg: creating a new column named 'count'
hits = hits.groupby(['inning', 'hit_type']).size().reset_index(name='count')

# to convert hit type to categorical
# to specify the order
hits['hit_type'] = pd.Categorical(hits['hit_type'], ['single', 'double', 'triple', 'hr'])

hits = hits.sort_values(['inning', 'hit_type'])

# to reshape for plotting
hits = hits.pivot(index='inning', columns='hit_type', values='count')

hits.plot.bar(stacked=True)
plt.show()
