import numpy as np
import pandas as pd
import os
import time

print("Welcome to Apriori 2.0!")
store_num = input("Please select your store \n 1. Amazon \n 2. Nike \n 3. Best Buy \n 4. K-Mart \n 5. Walmart\n")
print(store_num)
support_percent = input("Please enter the percentage of Support you want?\n")
print(support_percent)
confidence_percent = input("Please enter the percentage of Confidence you want?\n")
print(confidence_percent)


def number_to_store(store_number):
    switcher = {
        1: "data/amazon_transactions.csv",
        2: "data/nike_transaction.csv",
        3: "data/best_buy_transaction.csv",
        4: "data/k_mart_transaction.csv",
        5: "data/walmart_transaction.csv"
    }
    return switcher.get(store_number)


def number_to_item_list_of_store(store_number):
    switcher_dict = {
        1: "data/amazon_item_names.csv",
        2: "data/nike_item_names.csv",
        3: "data/best_buy_item_names.csv",
        4: "data/k_mart_item_names.csv",
        5: "data/walmart_item_names.csv"
    }
    return switcher_dict.get(store_number)


def a_priori(item_list, transaction, support_percentage, confidence_percentage):
    if support_percentage > 100 or confidence_percentage > 100 or support_percentage < 0 or confidence_percentage < 0:
        print("Support Percent or Confidence Percent is Invalid. \n Enter a valid number between 0 and 100.\n")
        print("Restarting Apriori 2.0.....\n")
        time.sleep(2)
        os.system("python APrior_2.0.py")

    if support_percentage >= 0 and support_percentage <= 100 and confidence_percentage >= 0 and confidence_percentage <= 100:
        df2 = pd.read_csv(item_list)
        df1 = pd.read_csv(transaction)
        print(df1.head())
        print(df2.head())
        trans = df1["transaction"]
        item_name = np.array(df2["item_name"])
        counter = np.zeros(len(item_name), dtype=int)
        # When K =1
        for row in trans:
            row = row.split(',')
            for item in row:
                if (item in item_name):
                    re = np.where(item_name == item)
                    counter[re[0]] += 1
                    print(item_name[re[0]])
                    print(counter)
        df3 = pd.DataFrame({"item_name": item_name, "number_of_count": counter})
        print(df3)


a_priori(str(number_to_item_list_of_store(int(store_num))), str(number_to_store(int(store_num))),
         int(support_percent), int(confidence_percent))
