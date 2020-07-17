import re
import math
import pandas as pd
from operator import itemgetter
from sklearn import preprocessing

data = pd.read_csv("C:\\Users\\Admin\\Desktop\\javaNegFIN\\Stats_recordLink.csv")
PATH_STATS_FILE="C:\\Users\\Admin\\Desktop\\javaNegFIN\\Stats_recordLink_New.csv"
df=data.iloc[1:5,2:]
x = df.values #returns a numpy array
print(x)
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
df = pd.DataFrame(x_scaled)
#print(df)

d1=data.iloc[:,0:2]
d1=d1.join(df)
print(d1)
d1.to_csv(PATH_STATS_FILE, header=["ANTECEDANTS", "CONSEQUENTS", "SUPPORT", "CONFIDENCE", "LIFT", "all_CONFIDENCE", "KULCZYNSKI", "COSINE"], index=False)