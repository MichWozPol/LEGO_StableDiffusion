import os

path = "../../../databases/Lego_db"
counter = 5000

for i in os.listdir(path):
    old_name=f"{path}/{i}"
    new_name=f"{path}/{str(counter)}.jpg"
    os.rename(old_name, new_name)
    counter += 1