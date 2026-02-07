import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

pd.set_option("display.max_columns",None)
data=pd.read_csv("onlinedeliverydata.csv")
data.info()
print(data.shape,"number of rows and number of columns")

data["Age"]=data["Age"].fillna(data["Age"].mean())




a=data["Age"].value_counts().reset_index()
print(a)
a.columns=["age","ordered"]
sns.barplot(data=a,x="age",y="ordered")
plt.show()