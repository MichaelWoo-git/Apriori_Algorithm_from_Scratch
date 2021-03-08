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
        return items_names, trans, support_percentage, confidence_percentage, k_value


def ap_1(items_names, trans, support_percentage, confidence_percentage, k_value):
    counter = np.zeros(len(items_names), dtype=int)
    for i in trans:
        i = list((map(str.strip, i.split(','))))
        s1 = set(i)
        nums = 0
        for x in items_names:
            s2 = set()
            s2.add(x)
            if s2.issubset(s1):
                counter[nums] += 1
            nums += 1
    counter = list(map(lambda x: int((x / len(trans)) * 100), counter))
    df3 = pd.DataFrame({"item_name": items_names, "support": counter})
    rslt_df = df3[df3['support'] > support_percentage]
    print("When K = " + str(k_value))
    print(rslt_df)
    items = np.array(rslt_df["item_name"])
    support_count = np.array(rslt_df["support"])
    k_value += 1
    return items, support_count, k_value, rslt_df


def ap_2(item_comb, k_value, trans, support_percentage):
    boo = True
    comb = combinations(item_comb, k_value)
    comb = list(comb)
    print(comb)
    counter = np.zeros(len(comb), dtype=int)
    print(counter)
    if k_value > 1:
        for i in trans:
            i = list((map(str.strip, i.split(','))))
            s1 = set(i)
            nums = 0
            for x in comb:
                s2 = set()
                x = np.asarray(x)
                for q in x:
                    s2.add(q)
                if s2.issubset(s1):
                    counter[nums] += 1
                nums += 1
    counter = list(map(lambda x: int((x / len(trans)) * 100), counter))
    df3 = pd.DataFrame({"item_name": comb, "support": counter})
    rslt_df = df3[df3['support'] > support_percentage]
    print("When K = " + str(k_value))
    print(rslt_df)
    items = np.array(rslt_df["item_name"])
    supp = np.array(rslt_df["support"])
    if len(items) == 0:
        print("hello")
        boo = False
        # calculate confidence
        return rslt_df, boo
        # exit(12321)
    # return items, supp, k_value
    return rslt_df, boo


frames = []
items_names, trans, support_percent, confidence_percent, k_value = a_priori_read(
    str(number_to_item_list_of_store(int(store_num))), str(number_to_store(int(store_num))),
    int(support_percent), int(confidence_percent))

items, supp, k_value, df = ap_1(items_names, trans, support_percent, confidence_percent, k_value)
frames.append(df)
boo = True
while boo:
    df_1, boo = ap_2(items, k_value, trans, support_percent)
    print("here is df")
    print(df_1)
    frames.append(df_1)
    k_value += 1
print("results are below")
print(pd.concat(frames))
