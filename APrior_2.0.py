import numpy as np
import pandas as pd
import os
import time
from itertools import permutations,combinations
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


def calculate_support(transaction, counts_of_items, min_support_percent):
    # this will be the denominator
    transaction_size = len(transaction)
    # print(type(transaction_size))
    # print(counts_of_items)
    name_items = np.array(counts_of_items["item_name"])
    support_calculation = (counts_of_items["number_of_count"] / transaction_size) * 100
    df = pd.DataFrame({"item_name": name_items, "support": support_calculation})
    df_meet_min_support = pd.DataFrame(df.loc[df["support"] >= min_support_percent])
    print(df_meet_min_support)
    # check to see if item is in set
    return df_meet_min_support


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
        items_that_meet_support = calculate_support(df1, df3, support_percentage)
        # check the size of the items that agree with the support
        # print(len(items_that_meet_support["item_name"]))
        if len(items_that_meet_support["item_name"]) == 1:
            print("The most frequent item in the transaction is: " + str(items_that_meet_support.at[0,"item_name"]))
        items = np.array(items_that_meet_support["item_name"])
        comb = combinations(items,2)
        print(list(comb))

        #do these permutations last
        # perm = permutations(items)
        # print(list(perm))


        # if len(items_that_meet_support["item_name"] > 1):
        #     break





a_priori(str(number_to_item_list_of_store(int(store_num))), str(number_to_store(int(store_num))),
         int(support_percent), int(confidence_percent))
