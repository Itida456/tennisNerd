import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Example tennis data
data = {
    'Player': ['Novak Djokovic', 'Rafael Nadal', 'Roger Federer', 'Andy Murray', 'Daniil Medvedev'],
    'Grand Slam Wins': [24, 22, 20, 3, 2],
    'Win Percentage': [85.5, 83.2, 81.5, 76.3, 74.2],
}

# Create a DataFrame
df = pd.DataFrame(data)

# Bar plot for Grand Slam wins
plt.figure(figsize=(10, 6))
sns.barplot(x='Grand Slam Wins', y='Player', data=df, palette='viridis')
plt.title('Grand Slam Wins by Players', fontsize=16)
plt.xlabel('Number of Grand Slam Wins')
plt.ylabel('Players')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()

# Line plot for win percentages
plt.figure(figsize=(10, 6))
sns.lineplot(x='Player', y='Win Percentage', data=df, marker='o', color='blue')
plt.title('Win Percentage by Player', fontsize=16)
plt.xlabel('Players')
plt.ylabel('Win Percentage')
plt.xticks(rotation=45)
plt.grid(linestyle='--', alpha=0.7)
plt.show()

# Pie chart for Grand Slam wins distribution
plt.figure(figsize=(8, 8))
plt.pie(df['Grand Slam Wins'], labels=df['Player'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
plt.title('Grand Slam Wins Distribution', fontsize=16)
plt.show()

# Heatmap of data correlation
plt.figure(figsize=(8, 5))
sns.heatmap(df[['Grand Slam Wins', 'Win Percentage']].corr(), annot=True, cmap='coolwarm', cbar=True)
plt.title('Correlation Heatmap', fontsize=16)
plt.show()
