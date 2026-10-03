import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("orders.csv")
df["OrderDate"] = pd.to_datetime(df["OrderDate"])
print(df,"\n")

#2
df["TotalAmount"]=df["Quantity"]*df["Price"]
print(df["TotalAmount"],"\n")

#3
total = df["TotalAmount"].sum()
print(total,'\n')
avr = df["TotalAmount"].mean()
print(avr,'\n')
count_of_orders = df["TotalAmount"].count()
print(count_of_orders,'\n')

#4
over_500 = df[df["TotalAmount"]>500]
print(over_500,'\n')

#5
ordered = df.sort_values("OrderDate", ascending=False)
print(ordered,'\n')

#6
ordered = df[(df["OrderDate"] > '2023-06-03') & (df["OrderDate"] <= '2023-06-10')]
print(ordered,'\n')

#7
grouped = df.groupby("Category")
print(grouped.count(),'\n')
print(grouped["TotalAmount"].sum(),'\n')

#8
total_best = df["TotalAmount"].sort_values(ascending=False).head(3)
print(total_best,'\n')

#task 2
orders_by_date = df.groupby("OrderDate").size()
orders_by_date.plot(kind='bar', title='Кількість замовлень по датах')
plt.xlabel('Дата')
plt.ylabel('Кількість')
plt.show()

pie_salary_by_category = df.groupby("Category")["TotalAmount"].sum()
pie_salary_by_category.plot(kind='pie', title='діаграма розподілу доходів по категоріях', autopct='%1.1f%%')
plt.show()
