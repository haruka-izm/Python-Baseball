import pandas as pd
import matplotlib.pyplot as plt
from data import games

# select all plays
plays = games[games['type'] == 'play']

# select all strike outs
strike_outs = plays[plays['event'].str.contains('K')]
strike_outs = strike_outs.groupby(['year', 'game_id']).size()

# to convert groupby obj to a DataFrame and
# to name the column that was created
strike_outs = strike_outs.reset_index(name='strike_outs')

# apply(): apply a function to multiple columns
strike_outs = strike_outs.loc[:, ['year', 'strike_outs']].apply(pd.to_numeric)
strike_outs.plot(x='year', y='strike_outs', kind='scatter').legend(['Strike Outs'])

plt.show()
