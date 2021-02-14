import random
import numpy as np
import pandas as pd

# items from walmart
store_name = "Walmart"
item_name = ["HP Pavilion Gaming Laptop", "HyperX Gaming Headset",
             "Logitech C270 HD WEBCAM HD 720p ",
             "Logitech G203 Prodigy Wired Gaming Mouse",
             "Eastsport Tech Backpack",
             "Conquer Compact Standing Desk Height Adjustable",
             "Mid-Back Office Chair Ergonomic Desk Chair ",
             "Sharpie S-Gel Gel Pens",
             "Hydro Flask 40oz ",
             "HyperX Gaming Pad "]

# random size of transaction
ran_size = list()
# create the size of transaction
trans = list()
# generate a random number between 1,10 in a size 20 list.
for i in range(20):
    ran_size.append(random.randint(1, 10))
print(ran_size)


# a function that generates a random number between 0 and 9 to chose from item_name list
def ran_fun():
    return random.randint(0, 9)


# Generate transaction given the number of transaction form the ran_size list of size 20
for q in ran_size:
    temp = list()
    i = 0
    while (q != i):
        print(i)
        temp.append(item_name[ran_fun()])
        i = len(set(temp))
    trans.append(set(temp))

print(len(trans))
trans = np.array(trans).reshape(-1, 1)
print(pd.DataFrame(trans))
trans = pd.DataFrame(trans)

# CONVERTS THE DATAFRAME INTO A CSV FILE
# trans.to_csv("walmart_transaction.csv")
df_2 = pd.DataFrame(item_name)
# df_2.to_csv("walmart_items.csv")
