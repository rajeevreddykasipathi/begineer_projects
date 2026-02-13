import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data=pd.read_csv("banking_loan.csv",sep=";")
print(data.head())
print("shape of the data:",data.shape)
print(data.info())
data=data[data["job"]!="unknown"]
print("shape of the data:",data.shape)

#remove duplicates
data=data.drop_duplicates()

#hich age group have taken the loan mostly
bins=[19,26,35,45,60,data["age"].max()]
labels=["19-26","26-35","35-45","45-60","60+"]

data["diff_age"]=pd.cut(data["age"],bins=bins,labels=labels,right=True,include_lowest=True)

age_loan=pd.pivot_table(data,index="loan",columns="diff_age",values="age",aggfunc="count")
print(age_loan)
#we can infer that age group of 26-25 and 45-60 have a more loans than other age groups


#which types of jobs takes loans and can help in contacting them more
job_loan=pd.pivot_table(data,index="job",columns="loan",values="age",aggfunc="count")
job_div=job_loan.div(job_loan.sum(axis=1),axis=0)*100
print(job_loan)
print(job_div)

#highest % loan takers are enterpernuer
#highest loan takers are blue collar


ed_loan=pd.pivot_table(data,index="education",columns="loan",values="age",aggfunc="count")
ed_div=ed_loan.div(ed_loan.sum(axis=1),axis=0)*100
print(ed_loan)
print(ed_div)
#studied in secondary and tertiary ed people took more loans(maybe to study)

grp1=data.groupby("default")["housing"]
print(grp1)
a=data[(data["housing"]=="yes")&(data["default"]=="yes")&(data["y"]=="yes")]
print(a)

grp2=data.groupby("default")["loan"]
print(grp2)
b=data[(data["loan"]=="yes")&(data["default"]=="yes")&(data["y"]=="yes")]
print(b)

#people with hosuing loan and personal are only few people who took the term deposit


#housing vs job and hos=using vs age(which age group mostly people take loan)
house_age=pd.pivot_table(data,index="housing",columns="diff_age",values="age",aggfunc="count")
house_div=house_age.div(house_age.sum(axis=0),axis=1)*100
print(house_age)
print(house_div)

house_job=pd.pivot_table(data,index="housing",columns="job",values="age",aggfunc="count")
house_job_div=house_job.div(house_job.sum(axis=0),axis=1)*100
print(house_job)
print(house_job_div)

#coversion rate by age
con_age=pd.pivot_table(data,index="y",columns="diff_age",values="age",aggfunc="count")
con_age_div=con_age.div(con_age.sum(axis=0),axis=1)*100
print(con_age)
print(con_age_div)
#more 60+ age group said yes

#conversion rate by job
con_job=pd.pivot_table(data,index="y",columns="job",values="age",aggfunc="count")
con_job_div=con_job.div(con_job.sum(axis=0),axis=1)*100
print(con_job)
print(con_job_div)


#conversion rate by education
con_ed=pd.pivot_table(data,index="y",columns="job",values="age",aggfunc="count")
con_ed_div=con_ed.div(con_ed.sum(axis=0),axis=1)*100
print(con_ed)
print(con_ed_div)

#conversion rate by balance
g1=data.groupby("y")["balance"]
print("avg balance in each person account who took term deposit:",g1.mean())
print("minium balance person who took term deposit:",g1.min())
print("max balance person who took term deposit:",g1.max())

#campaign
bins=[0,4,8,13,19,25,32,38,45]
labels=["0-4","4-8","8-13","13-19","19-25","25-32","32-38","38-45"]
data["campaign_group"]=pd.cut(data["campaign"],bins=bins,labels=labels,include_lowest=True,right=True)
# con_campaign=pd.pivot_table(data,index="y",columns="campaign_group",values="age",aggfunc="count")
# print(con_campaign)
campaign_rate = pd.crosstab(
    data["campaign_group"],
    data["y"],
    normalize="index"   #used to calculate percentage
) * 100

print(campaign_rate)

# campaign_rate.plot(kind="bar", figsize=(10,5))
# plt.ylabel("Percentage")
# plt.title("Campaign Contacts vs Subscription Rate")
# plt.show()

#duration vs y
g3=data.groupby("y")["duration"]
print(g3.mean())
print(g3.max())
print(g3.min())

#pervious campaign vs rate
poutcome_y=pd.crosstab(data["poutcome"],data["y"],normalize="index")*100
print(poutcome_y)
# print(g4.max())
# print(g4.min())


house_default_y=pd.crosstab([data["default"],data["housing"]],data["y"],normalize="index")*100
print(house_default_y)

#month vs y
month_order=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
month_y=pd.crosstab(data["month"],data["y"],normalize="index")*100
month_y=month_y.reindex(month_order)
print(month_y)

#contact vs subscribers
cont_sub=pd.crosstab(data["contact"], data["y"], normalize="index")*100
print(cont_sub)
cont_sub.plot(kind="bar")
plt.xlabel("type of contact")
plt.ylabel("percentage of contact")
plt.show()

#loan vs conversion rate
loan_con=pd.crosstab(data["loan"], data["y"], normalize="index")*100
print(loan_con)
loan_con.plot(kind="bar")
plt.xlabel("loans taken or not")
plt.ylabel("percentage of conversion rate")
plt.title("loan vs conversion rate")
plt.show()

#checking outliers
sns.boxplot(x="y", y="balance", data=data)
plt.show()


