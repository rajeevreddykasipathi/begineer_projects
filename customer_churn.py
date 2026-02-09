import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


data1=pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
print("shape of data: ",data1.shape)
print(data1.info())


#converting seniorcitizen 1,0 to yes and no
data1["SeniorCitizen"]=data1["SeniorCitizen"].astype(str)
data1["SeniorCitizen"]=data1["SeniorCitizen"].replace({"1":"yes","0":"no"})


#checking if charges is matching with tenure
checking=data1.loc[(data1["TotalCharges"]==0)&(data1["tenure"]>0)]
print(checking)

#to find the total discount given and to min the number of discount given
b=data1["tenure"]*data1["MonthlyCharges"]
data1["TotalCharges"]=data1["TotalCharges"].str.strip()
data1["TotalCharges"]=pd.to_numeric(data1["TotalCharges"])
print(data1.info())
discount=data1.loc[b<data1["TotalCharges"]]
extramoney=data1.loc[b>data1["TotalCharges"]]
exactmoney=data1.loc[b==data1["TotalCharges"]]
add=(b-discount["TotalCharges"])*(-1)
print("sum of all the discount",add.sum(),"\nnumber of dicount given",len(add.dropna()))
add1=(b-extramoney["TotalCharges"])
print(add1.sum(),len(add1.dropna()))
print(len(exactmoney))


#ensuring all are yes and no
internet_cols = [
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies"
]
data1.loc[
    data1["InternetService"] == "No",
    internet_cols
] = "No"

ensure=data1.loc[(data1=="No internet service").any(axis=1)]
print(len(ensure))


#churn rate
churn=data1.loc[data1["Churn"]=="No"]
print(f"overvall churn percentegae recorder is : {(len(churn)/len(data1))*100}")
g1=data1.groupby("Churn")["TotalCharges"].sum()
print(f"tottal revune by chirn and no-churn:{g1}")

g2=data1.groupby("Churn")["MonthlyCharges"].mean()
g3=data1.groupby("Churn")["TotalCharges"].mean()
print(f"avg of churn and non-churn monthly charges {g2}")
print(f"avg of churn and non-churn total charges {g3}")



#churn and tenure relationship
bins = [0, 6, 12, 24, 36, data1["tenure"].max()]
labels = [
    "0–6 months",
    "6–12 months",
    "1–2 years",
    "2–3 years",
    "3+ years"
]

data1["tenure_group"] = pd.cut(
    data1["tenure"],
    bins=bins,
    labels=labels,
    right=True,
    include_lowest=True
)

#paymentmethod and paperlessbilling while churning
pivot2=pd.pivot_table(data1,index=["Churn"],columns=["PaymentMethod","PaperlessBilling"],values="customerID",aggfunc="count")
print(pivot2)

#finding the churn vs other services provided
grp2=data1["InternetService"].value_counts()
print(grp2)
dsl_churn=data1[data1["InternetService"]=="DSL"]
fiber_churn=data1[data1["InternetService"]=="Fiber optic"]
pivot3=pd.pivot_table(dsl_churn,index=["OnlineSecurity","TechSupport","StreamingTV"],columns=["Churn"],
                      values="customerID",aggfunc="count")
print(pivot3)
pivot4=pd.pivot_table(fiber_churn,index=["OnlineSecurity","TechSupport","StreamingTV"],columns=["Churn"],
                      values="customerID",aggfunc="count")
pivot3_div=pivot3.div(pivot3.sum(axis=1),axis=0)*100
pivot4_div=pivot4.div(pivot4.sum(axis=1),axis=0)*100
print("fiber optic vs churn rate")
print(pivot4_div)
print("dsl vs churn rate")
print(pivot3_div)

#phone service and multiple lines
data1["MultipleLines"]=data1["MultipleLines"].astype(str).str.strip().replace("No phone service","No")

churn_phone=pd.pivot_table(data1,index=["PhoneService"],columns="Churn",
                      values="customerID",aggfunc="count")
print(churn_phone.div(churn_phone.sum(axis=1),axis=0)*100)
churn_multiple=pd.pivot_table(data1,index=["MultipleLines"],columns="Churn",
                      values="customerID",aggfunc="count")
print(churn_multiple.div(churn_multiple.sum(axis=1),axis=0)*100)
revenue_multiple=pd.pivot_table(data1,index=("MultipleLines","Churn"),columns="tenure_group",values="TotalCharges",
                                aggfunc=sum,fill_value=0)
print(revenue_multiple.div(revenue_multiple.sum(axis=1),axis=0)*100)

#Analyze churn % by:
#Gender,SeniorCitizen,Partner,Dependents
demo_cols = ["gender", "SeniorCitizen", "Partner", "Dependents"]
for col in demo_cols:
    churn_byfactors=pd.pivot_table(data1,index=col,columns=["Churn"],values="customerID",
                                   aggfunc="count",fill_value=0)
    print(churn_byfactors.div(churn_byfactors.sum(axis=1),axis=0)*100)


#VISUALIZATION FOR TENURE,PAYMENT,CONTRACT
pivot_tenure=pd.pivot_table(data1,index="tenure_group",columns="Churn",values="customerID",aggfunc="count")
pivot_tenure1=pivot_tenure.div(pivot_tenure.sum(axis=1),axis=0)*100
pivot_tenure1["Yes"].plot(kind="bar")
plt.ylabel("tenure groups")
plt.title("tenures vs churn")
plt.show()

pivot_method=pd.pivot_table(data1,index="PaymentMethod",columns="Churn",values="customerID",aggfunc="count")
pivot_method1=pivot_method.div(pivot_method.sum(axis=1),axis=0)*100
pivot_method1["Yes"].plot(kind="bar")
plt.ylabel("different payment methods")
plt.title("payment method vs churn")
plt.show()

pivot=pd.pivot_table(data1,index="Contract",columns="Churn",values="customerID",aggfunc="count")
pivot1=pivot.div(pivot.sum(axis=1),axis=0)*100
pivot1["Yes"].plot(kind="bar")
plt.ylabel("different contracts")
plt.title("contract vs churn")
plt.show()

revenue_churn = data1.groupby("Churn")["TotalCharges"].sum()

revenue_churn.plot(kind="bar")
plt.ylabel("Total Revenue")
plt.title("Revenue Contribution: Churn vs Non-Churn")
plt.show()
