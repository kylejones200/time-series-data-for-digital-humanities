# Description: Short example for Time Series Data for Digital Humanities.




from google_pygram import GooglePyGram as gpg
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

word_list = ["democracy", "liberty", "freedom", "equality", "capitalism"]
start_year = 1800
end_year = 2019
pygram = gpg(
    corpus="English",
    corpus_year=2019,
    start_year=start_year,
    end_year=end_year,
    smoothing=3,
    case_sensitive=False,
    phrases=word_list
)

# Convert results to a DataFrame
df = pygram.to_df()

# Ensure years are integers
df["year"] = df["year"].astype(int)
df.to_csv("ngram.csv")
# Get full data range for plotting
full_y_min = df[word_list].min().min()
full_y_max = df[word_list].max().max()

# Define cleaned label range for the left spine and y-ticks
label_y_min = 0.00002
label_y_max = 0.00012

# Plot trends
plt.figure(figsize=(10, 5))
ax = plt.gca()  # Get the current axis

for word in word_list:
    line, = plt.plot(df["year"], df[word], label=word)  # Save the line object
    plt.text(df["year"].iloc[-1] + 2, df[word].iloc[-1], word, 
             fontsize=10, verticalalignment='bottom', color=line.get_color())


ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylim(full_y_min, full_y_max)
ax.spines['left'].set_bounds(label_y_min, label_y_max)
ax.spines['bottom'].set_bounds(df["year"].min(), df["year"].max())
min_year = df["year"].min()
max_year = df["year"].max()
x_ticks = list(range(min_year, max_year, 50)) + [max_year]
ax.set_xticks(sorted(set(x_ticks)))
ax.set_yticks([label_y_min, (label_y_min + label_y_max) / 2, label_y_max])
plt.xlabel("Year")
plt.ylabel("Relative Frequency")
plt.title(f"Google Books Ngram Trends from {start_year} to {end_year}")
plt.savefig("ngram_trends.png")
plt.show()
