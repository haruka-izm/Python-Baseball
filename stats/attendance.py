import pandas as pd
import matplotlib.pyplot as plt
from data import games

# select all rows: loc[], specify: games[]
attendance = games.loc[(games['type'] == 'info') & (games['multi2'] == 'attendance'), ['year', 'multi3']]

# change the column name
attendance.columns = ['year', 'attendance']

# select all rows in the attendance column
attendance.loc[:, 'attendance'] = pd.to_numeric(attendance.loc[:, 'attendance'])

attendance.plot(x='year', y='attendance', figsize=(15, 7), kind='bar')

plt.xlabel('Year')
plt.ylabel("Attendance")
plt.axhline(y=attendance['attendance'].mean(), label='Mean', linestyle='--', color='green')

# need to call plt.show()
plt.show()

