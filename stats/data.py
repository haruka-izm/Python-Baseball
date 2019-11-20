import os, glob
import pandas as pd

game_files = glob.glob(os.path.join(os.getcwd(), 'games', '*.EVE'))
game_files.sort()

game_frames = []
for game_file in game_files:
    # names: column names
    game_frame = pd.read_csv(game_file, names=['type', 'multi2',
    'multi3', 'multi4', 'multi5', 'multi6', 'event'])
    game_frames.append(game_frame)

games = pd.concat(game_frames)

# clean values
# dataframe.loc[row condition, [columns]] == new value
games.loc[games['multi5'] == '??', 'multi5'] = ''

# values to be filled in for all rows on the indentifiers DataFrame
identifiers = games['multi2'].str.extract(r'(.LS(\d{4})\d{5})')
identifiers = identifiers.fillna(method='ffill')

# change the column's names
identifiers.columns = ['game_id', 'year']

# append the columns of the identifiers DataFrame to the game DataFrame
games = pd.concat([games, identifiers], axis=1, sort=False)

# fill in all Nan values in the gara with ' '
games = games.fillna(' ')

# to slightly reduce the memory use
games.loc[:, 'type'] = pd.Categorical(games.loc[:, 'type'])

print(games.head(5))
