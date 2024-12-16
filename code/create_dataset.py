import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('final_result_consistency.csv', sep = '\t')
df['len'] = df['content'].apply(lambda x: len(x))
df = df[df['len'] < 10000]
df['len'].hist()
plt.show()
df_abc = df[df['source'] == 'abcnews'].head(50)
df_fox = df[df['source'] == 'foxnews'].head(50)
df_cnn = df[df['source'] == 'cnn'].head(52)

result = pd.concat([df_abc, df_fox, df_cnn], axis = 0, ignore_index = True)
result.to_csv('exp_dataset.csv', sep = '\t', index = False)
result['len'].hist()
plt.show()
result['source'].value_counts()

result_df = pd.DataFrame()
for file in ['h1_result.csv', 'h1_result_2.csv', 'h1_result_3.csv', 'h1_result_4.csv', 'h1_result_5.csv']:
    df = pd.read_csv(file, sep = '\t')
    result_df = pd.concat([result_df, df], axis = 0, ignore_index = True)

# result_df = result_df[result_df['score']!=-999]
result_df = result_df[result_df['link'] != 'https://www.cnn.com/2024/12/01/politics/joe-biden-pardon-hunter-biden-statement/index.html']
result_df.to_csv('full_dataset.csv', sep = '\t', index = False, encoding = 'utf-8-sig')
result_df.groupby(['link', 'model'])['score'].value_counts()
result_df.shape
df.shape
# print(result_df[result_df['score'] == -999]['link'].iloc[0])
result_df[result_df['score']==-999]

# df_cnn.tail(2).to_csv('cnn_addon.csv', sep = '\t', encoding = 'utf-8-sig', index = False)
# df_claude_add = result[result['link'] == 'https://www.cnn.com/2024/12/01/politics/joe-biden-pardon-hunter-biden-statement/index.html']
# df_claude_add.to_csv('claude_add.csv', sep = '\t', index = False)
result_df['score'].hist()
plt.show()
#%%
