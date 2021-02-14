import numpy as np
import pandas as pd


def a_priori(item_list, transaction):
    df2 = pd.read_csv(item_list)
    df1 = pd.read_csv(transaction)
    # print(df1.head())
    # print(df2.head())
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
    # Continue when K = 2
a_priori("data/amazon_item_names.csv", "data/amazon_transactions.csv")
