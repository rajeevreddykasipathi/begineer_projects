import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from IPython.display import display




pd.set_option("display.max_columns",None)
data=pd.read_csv("onlinedeliverydata.csv")
data.info()
print(data.shape,"number of rows and number of columns")
data.columns=data.columns.str.strip()
data["Age"]=data["Age"].fillna(data["Age"].mean())

#using git as of now and checking weather it is working or notgit


a=data["Age"].value_counts().reset_index()
print(a)
a.columns=["age","ordered"]
# sns.barplot(data=a,x="age",y="ordered")
# plt.show()

# b=data.groupby("Order Time")["Long delivery time"].value_counts().reset_index("Long delivery time")
# print(b)
# b.columns=["long delivery time","order time"]
# sns.barplot(b,x="long delivery time",y="order time")
# plt.show()

count=data.groupby("Order Time")["Long delivery time"].value_counts().reset_index()
b=pd.pivot_table(count,
    index="Order Time",
    columns="Long delivery time",
    values="count"
)
# display(b)
# b.to_csv("my_pivot.csv")
# b.plot(kind="bar")
# plt.show()
#
# #ordered based on income
# ordered_most=data["Monthly Income"].value_counts()
# ordered_most.plot(kind="bar")
# plt.show()

review=data.groupby("Good Taste")["Good Quantity"].value_counts().reset_index(name="review")
print(review)
v=pd.pivot_table(review,
    index="Good Taste",
    columns="Good Quantity",
    values="review")
print(v)