import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('../rated/2024-10-15.csv')
df['result']
# Extract the score from the result column
def extract_score(x):
    x = x.split('\n')[0].replace('*', '').split(' ')[-1]
    try:
        return int(x)
    except:
        return 0
df['score'] = df['result'].apply(extract_score)
# df['score'].unique()
def plot_hist_side_by_side_fixed_x(df, source):
    # Filter data for the given source and both models
    tmp_gpt = df.loc[(df['source'] == source) & (df['model'] == 'gpt'), :]
    tmp_claude = df.loc[(df['source'] == source) & (df['model'] == 'claude'), :]

    # Group by score and count titles
    # tmp_gpt = tmp_gpt.groupby('score')['title'].count().reset_index()
    # tmp_claude = tmp_claude.groupby('score')['title'].count().reset_index()

    # Define bins and width
    width = 0.35  # Width of the bars

    # Create subplots
    # fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    bins = [-2, -1, 0, 1, 2]
    # Plot histograms side by side
    plt.hist(tmp_gpt['score'], bins = bins, alpha=0.6, color='red', label='gpt', align='mid', width=width)
    plt.hist(tmp_claude['score'], bins = bins, alpha=0.6, color='tan', label='claude', align='mid', width=width)

    # Set x-axis limits from -2 to 2
    plt.xticks([-3, -2, -1, 0, 1, 2, 3])
    # ax[1].set_xticks([-2, -1, 0, 1, 2])

    # Add labels, title, and legend
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.legend()

    plt.suptitle(f"{source} rated by GPT and Claude")

    # Show plot
    plt.tight_layout()
    plt.show()

# Plot for each source
plot_hist_side_by_side_fixed_x(df, 'cnn')
plot_hist_side_by_side_fixed_x(df, 'foxnews')
plot_hist_side_by_side_fixed_x(df, 'abcnews')

df['score'].unique()