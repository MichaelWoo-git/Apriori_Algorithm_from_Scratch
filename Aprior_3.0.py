import numpy as np
import pandas as pd
import os
import time
from itertools import permutations, combinations

# The begining of the algorithm prompts
print("Welcome to Apriori 2.0!")
store_num = input("Please select your store \n 1. Amazon \n 2. Nike \n 3. Best Buy \n 4. K-Mart \n 5. Walmart\n")
print(store_num)
support_percent = input("Please enter the percentage of Support you want?\n")
print(support_percent)
confidence_percent = input("Please enter the percentage of Confidence you want?\n")
print(confidence_percent)

# These are my dictionaries to choose which store to get based in Key-Value Pairs
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


def a_priori_read(item_list, transaction, support_percentage, confidence_percentage):
    # Create two different functions one that is solo for read in the file data and the other that is algorithmic with the data
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
        trans = np.array(df1["transaction"])
        items_names = np.array(df2["item_name"])
        k_value = 1
        ap(items_names, trans, support_percentage, confidence_percentage, k_value)


def ap(items_names, trans, support_percentage, confidence_percentage, k_value):
    counter = np.zeros(len(items_names), dtype=int)
    # print(counter)
    if k_value == 1:
        for i in trans:
            i = list((map(str.strip, i.split(','))))
            s1 = set(i)
            # print(s1)
            # print(s1)
            nums = 0
            for x in items_names:
                s2 = set()
                s2.add(x)
                # print(i)
                # print(s2)
                # print(s2.issubset(s1))
                if s2.issubset(s1):
                    counter[nums] += 1
                # print(counter)
                nums += 1
    if k_value > 1:
        for i in trans:
            i = list((map(str.strip, i.split(','))))
            s1 = set(i)
            # print(s1)
            nums = 0
            for x in items_names:
                s2 = set()
                x = np.asarray(x)
                # print(x)
                for q in x:
                    #   print(q)
                    s2.add(q)
                # print(i)
                # print(s2)
                # print(s2.issubset(s1))
                if s2.issubset(s1):
                    counter[nums] += 1
                # print(counter)
                nums += 1

    # print(counter)
    counter = list(map(lambda x: int((x / len(trans)) * 100), counter))
    df3 = pd.DataFrame({"item_name": items_names, "freq": counter})
    # print(df3)
    rslt_df = df3[df3['freq'] > support_percentage]

    print(rslt_df)
    if not rslt_df.empty:
        print(k_value)
        k_value += 1
        df_items = pd.read_csv(str(number_to_item_list_of_store(int(store_num))))
        names_of_items = np.array(df_items["item_name"])
       # print(names_of_items)
        item_combs = np.array(df_items["item_name"])
        comb = combinations(item_combs, k_value)
        comb = list(comb)
        # print(len(comb))
        # for t in comb:
        #     for r in t:
        #         print(r)
        ### create permutations here
        ap(comb, trans, support_percentage, confidence_percentage, k_value)


a_priori_read(str(number_to_item_list_of_store(int(store_num))), str(number_to_store(int(store_num))),
              int(support_percent), int(confidence_percent))
