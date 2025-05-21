import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('C:/Users/Lenovo/Downloads/Tennis data - Sheet1 (1).csv')

# Data cleanup
print("DATA CLEANUP AND CHECK")
print(df.head())
print(df.columns)  # Verify column names

df = df.dropna(how='all')

df['YEAR'] = pd.to_numeric(df['YEAR'], errors='coerce')


print("ANALYSIS")
# Count the number of wins for each champion
champion_counts = df['CHAMPION'].value_counts()

# Display the top champions
print("Most Successful Players:")
print(champion_counts.head())

# Count the number of wins for each champion
champion_counts = df['CHAMPION'].value_counts()


# Filter rows where Novak Djokovic appeared in either CHAMPION or RUNNER-UP
djokovic_matches = df[(df['CHAMPION'] == 'Novak Djokovic (Serbia)') | (df['RUNNER-UP'] == 'Novak Djokovic (Serbia)')]

print("Novak Djokovic's Finals Appearances:")
print(djokovic_matches)


#most successful players per tournamet
print(df[df['TOURNAMENT'] == 'French Open']['CHAMPION'].value_counts())

#what player is better on what surface
print(df.groupby('SURFACE')['CHAMPION'].value_counts())

#country dominance
df['CHAMPION_COUNTRY'] = df['CHAMPION'].str.extract(r'\((.*?)\)')
print(df['CHAMPION_COUNTRY'].value_counts())
