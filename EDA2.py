import pandas as pd
import numpy as mp
import matplotlib.pyplot as plt
import seaborn as sns

data1=pd.read_csv("amazon_india_2025.csv")
print(data1.shape)
print(data1.info())

data1=data1.drop_duplicates()
print(data1.shape)



#converting orginal_price(str) to float
data1["original_price_inr"]=(data1["original_price_inr"].astype(str)
                             .str.strip()
                             .str.replace("Rs","",regex=False).str.replace(",","",regex=False)
                             .str.replace("₹","",regex=False))

data1["original_price_inr"]=data1["original_price_inr"].astype(float)


# number of prime vs non-prime users

data1["is_prime_eligible"] = (
    data1["is_prime_eligible"]
    .astype(str)
    .str.strip()
    .str.lower()
    .replace({"1": "Yes", "true": "Yes", "0": "No", "false": "No","yes":"Yes","no":"No"})
)

counts = data1["is_prime_eligible"].value_counts(dropna=False)
print(counts)



"filling age groups which are missing based upon the spending "
young_age=data1[data1["customer_age_group"]=="18-25"]
nextgen_age=data1[data1["customer_age_group"]=="26-35"]
middle_age=data1[data1["customer_age_group"]=="36-45"]
old_age=data1[data1["customer_age_group"]=="46-55"]
older_age=data1[data1["customer_age_group"]=="55+"]


avg_18_25 = young_age["subtotal_inr"].mean()
avg_26_35=nextgen_age["subtotal_inr"].mean()
avg_36_45=middle_age["subtotal_inr"].mean()
avg_46_55=old_age["subtotal_inr"].mean()
avg_55=older_age["subtotal_inr"].mean()




data1.loc[
    (data1["customer_age_group"].isna()) &
    (data1["subtotal_inr"] <= avg_18_25),
    "customer_age_group"
] = "18-25"


data1.loc[
    (data1["customer_age_group"].isna()) &
    (data1["subtotal_inr"] <= avg_26_35),
    "customer_age_group"
] = "26-35"




data1.loc[
    (data1["customer_age_group"].isna()) &
    (data1["subtotal_inr"] >= avg_36_45),
    "customer_age_group"
] = "36-45"


data1.loc[
    (data1["customer_age_group"].isna()) &
    (data1["subtotal_inr"] <= avg_46_55),
    "customer_age_group"
] = "46-55"


data1.loc[
    (data1["customer_age_group"].isna()) &
    (data1["subtotal_inr"] <= avg_55),
    "customer_age_group"
] = "55+"


#filling all the other missing values
data1["festival_name"]=data1["festival_name"].fillna("no_festival")
data1["customer_age_group"]=data1["customer_age_group"].fillna("unknown")
data1["delivery_charges"]=data1["delivery_charges"].fillna(0)
data1["customer_rating"]=data1["customer_rating"].fillna("unknown")


# "according to logic of membership the prime members should have 0 delivery "
#       "charges but it is an anomly"
a=data1.loc[(data1["is_prime_eligible"]=="Yes") & (data1["delivery_charges"]!=0)]


#this is to find the unique different categories present and subcategory
# where it is been sold more and genertaed more revenue
a=data1["category"].unique()
print(a)
b=data1["subcategory"].unique().max()
print(b)

print("FESTIVAL NAME")
print(data1["festival_name"].value_counts())


print("category")
print(data1["category"].value_counts())



print("REVENUE BY PRIME ELIGIBILITY")
print(
    data1.groupby("is_prime_eligible")["subtotal_inr"].sum()
)

print("age vs total")
print(
    data1.groupby("customer_age_group")["subtotal_inr"].sum())


print("festival vs total")
print(data1.groupby("festival_name")["subtotal_inr"].sum())


print("total revenue")
print(data1["discounted_price_inr"].sum())




print("Prime vs Non-Prime revenue bar chart")
c= data1.groupby("is_prime_eligible")["subtotal_inr"].sum().reset_index()
sns.barplot(
    data=c,
    x="is_prime_eligible",
    y="subtotal_inr"
)
plt.xlabel("Membership Type")
plt.ylabel("revenue")
plt.title("Prime vs Non-Prime Customers")
plt.show()


print("revenue by age group")
x = data1.groupby("customer_age_group")["subtotal_inr"].sum().reset_index()


sns.barplot(
    data=x,
    x="customer_age_group",
    y="subtotal_inr"
)
plt.xlabel("age_group")
plt.ylabel("revenue")
plt.title("revenue by different age groups")
plt.show()




grouped1=data1.groupby("subcategory")["subtotal_inr"].sum().reset_index()
sns.barplot(
    data=grouped1,
    x="subcategory",
    y="subtotal_inr"
)
plt.xlabel("different_categories")
plt.ylabel("revenue")
plt.title("revenue from different categories")
plt.show()







