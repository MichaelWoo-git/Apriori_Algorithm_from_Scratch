import numpy as np
import pandas as pd
import os
import time
from itertools import permutations, combinations

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


#  We first have to read in the csv files and make sure that the inputs received from the user are valid

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


#  The first go around the apriori algorithm we find the items that are most frequent K = 1
#  This is so that we can find the most frequent items in the transactions

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
    # print("When K = " + str(k_value))
    # print(rslt_df)
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
    # print("When K = " + str(k_value))
    # print(rslt_df)
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

#  Looping through the transactions and increasing K until we can longer support the support value

while boo:
    df_1, boo = ap_2(items, k_value, trans, support_percent)
    frames.append(df_1)
    k_value += 1

#  Here are the results after we find the most frequent sets in the list of transactions

print("Results of support that meet user standards of " + str(support_percent))
print(pd.concat(frames))
df_supp = pd.concat(frames)
df_supp.head()

#  Reset the index just to organize it

df_supp = df_supp.reset_index().drop('index', axis=1)
df_supp.head()


#  Generating the Associations (Permutations) and calculating the confidence of the item sets

def confidence(val):
    # first
    df_212 = df_supp.loc[df_supp['k_val'] == val]
    stuff_name = np.array(df_212["item_name"])
    support_arr = np.array(df_212['support'])

    # second
    df_temp = df_supp.loc[df_supp['k_val'] == val + 1]
    df_21231 = np.array(df_temp["item_name"])
    sup_arr = np.array(df_temp['support'])

    # variables to save
    sup_ov = list()
    sup_sing = list()
    perm_item = list()

    # When the item set is k =1 and the comparison is k = 2
    if val == 1:
        for w in df_21231:
            temp_list = list(df_21231)
            ov_sup = sup_arr[temp_list.index(w)]
            temp = set()
            for d in w:
                temp.add(d)
            perm = permutations(temp)
            perm_lst = list(perm)
            for y in perm_lst:
                perm_item.append(y)
                sup_ov.append(ov_sup)
                sup_sing.append(int(support_arr[np.where(stuff_name == y[0])]))

    # When the item set is k > 1 and the comparison is k += k + 1
    if val > 1:
        for w in df_21231:
            temp_list = list(df_21231)
            ov_sup = sup_arr[temp_list.index(w)]
            temp = set()
            for d in w:
                temp.add(d)
            perm = permutations(temp)
            perm_lst = list(perm)
            for y in perm_lst:
                try:
                    temp_set = []
                    for t in range(0, val):
                        temp_set.append(y[t])
                    lol = tuple(sorted(temp_set))
                    tp_lst = list(stuff_name)
                    ss = support_arr[tp_lst.index(lol)]
                    sup_ov.append(ov_sup)
                    sup_sing.append(ss)
                    perm_item.append(y)
                except:
                    # print("itemset below does not exist...")
                    # print(y)
                    sup_ov.append(ov_sup)
                    sup_sing.append(0)
                    perm_item.append(y)

    df_main = pd.DataFrame({"association": perm_item, "support_ov": sup_ov, "support_sing": sup_sing})
    df_main = df_main.assign(confidence=lambda x: round(((x.support_ov / x.support_sing) * 100), 0))
    return df_main


# Finding the max k value in the given set

max(df_supp["k_val"])

# Iterative calculating the assocations and confidence

df_frames = []
for lp in range(1, max(df_supp["k_val"]) + 1):
    # print(lp)
    df_0 = confidence(lp)
    df_0 = df_0[df_0.support_sing != 0]
    df_frames.append(df_0)

df_associations = pd.concat(df_frames)
df_associations.head()

# # Concat the dataframes

df_associations = pd.concat(df_frames)
df_associations.head()

#  Making sure that user parameters are met for confidence

df_associations = df_associations[df_associations['confidence'] >= confidence_percent]
df_associations.head()

#  Formatting the dataframe final

df_final = df_associations.reset_index().drop(['index', 'support_sing'], axis=1)
df_final.columns = ["Association", "Support", "Confidence"]
print("\nFinal Associations that meet the user standards....")
print("Support: " + str(support_percent) + "%" + "\t" + "Confidence: " + str(confidence_percent) + '%')
print(df_final)
