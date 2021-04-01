#  Imports

import numpy as np
import pandas as pd
import os
import time
from itertools import permutations, combinations
from IPython.display import display

# this will display the max column width so we can see the associations involved....
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)

#  Prompts to choose which store you want

print("Welcome to Apriori 2.0!")
store_num = input("Please select your store \n 1. Amazon \n 2. Nike \n 3. Best Buy \n 4. K-Mart \n 5. Walmart\n")
print(store_num)
support_percent = input("Please enter the percentage of Support you want?\n")
print(support_percent)
confidence_percent = input("Please enter the percentage of Confidence you want?\n")
print(confidence_percent)


#  These are my dictionaries to choose which store to get based in Key-Value Pairs

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


def ns(store_number):
    switcher_store = {
        1: "Amazon",
        2: "Nike",
        3: "Best Buy",
        4: "K-Mart",
        5: "Walmart"
    }
    return switcher_store.get(store_number)


#  We first have to read in the csv files and make sure that the inputs received from the user are valid


def a_priori_read(item_list, transaction, support_percentage, confidence_percentage):
    # Create two different functions one that is solo for read in the file data and the other that is algorithmic with the data
    if support_percentage > 100 or confidence_percentage > 100 or support_percentage < 0 or confidence_percentage < 0:
        print("Support Percent or Confidence Percent is Invalid. \n Enter a valid number between 0 and 100.\n")
        print("Restarting Apriori 2.0.....\n")
        time.sleep(2)
        os.system("python Aprior_Algo")
    if support_percentage >= 0 and support_percentage <= 100 and confidence_percentage >= 0 and confidence_percentage <= 100:
        df_item_list = pd.read_csv(item_list)
        df_transactions = pd.read_csv(transaction)
        print(df_transactions.head())
        print(df_item_list.head())
        trans = np.array(df_transactions["transaction"])
        items_names = np.array(df_item_list["item_name"])
        k_value = 1
        return items_names, trans, support_percentage, confidence_percentage, k_value


#  The first go around of the Apriori Algorithm we find the items that are most frequent when K=1
#  This is so that we can find the most frequent items given the transactions

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
    df3 = pd.DataFrame({"item_name": items_names, "support": counter, "k_val": np.full(len(items_names), k_value)})
    rslt_df = df3[df3['support'] >= support_percentage]
    print("When K = " + str(k_value))
    print(rslt_df)
    items = np.array(rslt_df["item_name"])
    support_count = np.array(rslt_df["support"])
    k_value += 1
    return items, support_count, k_value, rslt_df


#  Then we use this function below to find item sets that are most frequent when K > 1

def ap_2(item_comb, k_value, trans, support_percentage):
    boo = True
    comb = combinations(item_comb, k_value)
    comb = list(comb)
    counter = np.zeros(len(comb), dtype=int)
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
    df3 = pd.DataFrame({"item_name": comb, "support": counter, "k_val": np.full(len(comb), k_value)})

    # Making sure that user parameters are met for support
    rslt_df = df3[df3['support'] >= support_percentage]
    print("When K = " + str(k_value))
    print(rslt_df)
    items = np.array(rslt_df["item_name"])
    supp = np.array(rslt_df["support"])
    if len(items) == 0:
        boo = False
        return rslt_df, boo
    return rslt_df, boo


#  Calls of functions and variable saving


frames = []
items_names, trans, support_percent, confidence_percent, k_value = a_priori_read(
    str(number_to_item_list_of_store(int(store_num))), str(number_to_store(int(store_num))),
    int(support_percent), int(confidence_percent))

items, supp, k_value, df = ap_1(items_names, trans, support_percent, confidence_percent, k_value)
frames.append(df)
boo = True

#  Increasing K by 1 until we can longer support the support value


while boo:
    df_1, boo = ap_2(items, k_value, trans, support_percent)
    frames.append(df_1)
    k_value += 1

#  Combine the dataframes we have from when we increase K


print("results of item-sets that meet support are below")
display(pd.concat(frames))
df_supp = pd.concat(frames)
# df_supp.head()


#  Reset the index just to organize it and the results after we find the most frequent sets in the list of transactions

df_supp = df_supp.reset_index().drop('index', axis=1)
df_supp


#  This is the FUNCTION that generates the Associations (Permutations) and calculating the Confidence of the item sets


def confidence(val):
    # Since we already have our support for our items what we need to worry about is the confidence levels

    # item_set before the arrow
    df_before = df_supp.loc[df_supp['k_val'] == val]
    stuff_name_before = np.array(df_before["item_name"])
    support_arr_before = np.array(df_before['support'])

    # item_set of the overall set
    df_overall = df_supp.loc[df_supp['k_val'] == val + 1]
    df_ov = np.array(df_overall["item_name"])
    suppport_ov = np.array(df_overall['support'])

    # variables to save
    sup_ov = list()
    sup_sing = list()
    perm_item = list()

    # When the item set is k =1 and the comparison is k = 2
    if val == 1:
        for i_set in df_ov:
            temp_list = list(df_ov)
            # I want to select the support of that overall set
            ov_sup = suppport_ov[temp_list.index(i_set)]
            temp = set()
            # This is where we generate our permutations
            for indiv_item in i_set:
                temp.add(indiv_item)
            perm = permutations(temp)
            perm_lst = list(perm)
            # for each permutation in the perm_list
            for perm_item_set in perm_lst:
                perm_item.append(perm_item_set)
                sup_ov.append(ov_sup)
                sup_sing.append(int(support_arr_before[np.where(stuff_name_before == perm_item_set[0])]))

    # When the item set is k > 1 and the comparison is k += k + 1
    if val > 1:
        for i_set in df_ov:
            temp_list = list(df_ov)
            ov_sup = suppport_ov[temp_list.index(i_set)]
            temp = set()
            for indiv_item in i_set:
                temp.add(indiv_item)
            perm = permutations(temp)
            perm_lst = list(perm)
            for perm_item_set in perm_lst:
                try:
                    temp_set = []
                    for dex in range(0, val):
                        temp_set.append(perm_item_set[dex])
                    item_set_before = tuple(temp_set)
                    tp_lst = list(stuff_name_before)
                    ss = support_arr_before[tp_lst.index(item_set_before)]
                    sup_ov.append(ov_sup)
                    sup_sing.append(ss)
                    perm_item.append(perm_item_set)
                except:
                    #                     print("itemset below does not exist...")
                    #                     print(y)
                    sup_ov.append(ov_sup)
                    sup_sing.append(0)
                    perm_item.append(perm_item_set)

    df_main = pd.DataFrame({"association": perm_item, "support_ov": sup_ov, "support_sing": sup_sing})
    df_main = df_main.assign(confidence=lambda x: round(((x.support_ov / x.support_sing) * 100), 0))
    return df_main


# Finding the max k value in the given set


try:
    max(df_supp["k_val"])
except:
    print("No max was found...")

# This is where I iteratively call the confidence() function


df_frames = []
try:
    if len(df_supp["k_val"]) != 0:
        for lp in range(1, max(df_supp["k_val"]) + 1):
            # print(lp)
            #
            df_0 = confidence(lp)
            df_0 = df_0[df_0.support_sing != 0]
            df_frames.append(df_0)
        df_associations = pd.concat(df_frames)
        print(df_associations.head())
except:
    print("No items or transactions meet the user requirements!")

#  Concat the Dataframes
try:
    df_associations = pd.concat(df_frames)
    print(df_associations)
except:
    print("No items or transactions meet the user requirements!")

#  Making sure that user parameters are met for confidence


try:
    df_associations = df_associations[df_associations['confidence'] >= confidence_percent]
    print(df_associations)
except:
    print("No items or transactions meet the user requirements!")

#  Formatting the Dataframe Final


try:
    df_final = df_associations.reset_index().drop(['index', 'support_sing'], axis=1)
    df_final.columns = ["Association", "Support", "Confidence"]
except:
    print("No items or transactions meet the user requirements!")

# Final Associations


try:
    print("Store Name: " + str(ns(int(store_num))))
    print("\nFinal Associations that meet the user standards....")
    print("Support: " + str(support_percent) + "%" + "\t" + "Confidence: " + str(confidence_percent) + '%')
    print(df_final)
except:
    print("\nNo Associations were generated based on the parameters set!")
