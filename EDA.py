import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data1=pd.read_csv("titanic_original.csv")

#remove the row which doesnot contain all n ull values
data1.dropna(how="all",inplace=True)
#handle missing values
data1["age"]=data1["age"].fillna(data1["age"].median())
data1["embarked"]=data1["embarked"].fillna("S")
data1["boat"]=data1["boat"].fillna(0)
data1["cabin"] = data1["cabin"].where(
    data1["pclass"] != 2,
    data1["cabin"].ffill()
)
print(data1.info())

#remove duplicates
data1.drop_duplicates()

#first class passengers : filter data
first_class=data1[data1["pclass"]==1]
print(first_class)




# survival rate of women less than 18 who travelled in third class
survival=data1[data1["survived"]==1]
survival_women=survival[survival["sex"]=="female"]
age_survival_women=survival_women[survival_women["age"]<18]
class_women=age_survival_women[age_survival_women["pclass"]==3]
print(len(class_women))

#number of male solo traveller
solo_traveller=data1.loc[(data1["sibsp"]==0) & (data1["parch"]==0) & (data1["sex"]=="male")]
print(len(solo_traveller))



# survival_rate_women.plot(kind="bar")
# plt.show()

# oldest passenger on ship who survived
old_passenger=data1.loc[(data1["survived"]==1) & (data1["age"]==data1.loc[data1["survived"]==1,"age"].max())]
print(old_passenger)

a=survival.loc[survival["age"].idxmax()]
print(a)


#bar chart: survival rate by class
survival_by_class=data1.groupby("pclass")["survived"].mean()
survival_by_class.plot(kind="bar")
plt.show()

#histogram of different ages
sns.histplot(data1["age"],kde=True,bins=20,edgecolor="black")
plt.title("age died")
plt.xlabel("AGE")
plt.ylabel("frequency")
plt.show()


# relation between age and fare
plt.scatter(data1["age"],data1["fare"],alpha=0.5)
plt.xlabel("age")
plt.ylabel("fare")
plt.show()






