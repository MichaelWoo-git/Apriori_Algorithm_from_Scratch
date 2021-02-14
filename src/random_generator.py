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
for i in range(20):
    ran_size.append(random.randint(1, 10))
print(ran_size)


# a function that generates a random number between 0 and 9
def ran_fun():
    return random.randint(0, 9)
for q in ran_size:
    temp = list()
    i = 0
    while (q != i):
        print(i)
        temp.append(item_name[ran_fun()])
        i = len(set(temp))
    trans.append(set(temp))
# print(len(trans))
trans = np.array(trans).reshape(-1, 1)
print(pd.DataFrame(trans))
trans = pd.DataFrame(trans)
trans.to_csv("src/walmart_transaction.csv")
df_2 = pd.DataFrame(item_name)
df_2.to_csv("src/walmart_items.csv")
