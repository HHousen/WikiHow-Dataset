'''
This code is used to create article and summary files from the csv file.
The output of the file will be a directory of text files representing seoarate articles and their summaries.
Each summary line starts with tag "@summary" and the article is followed by "@article".
'''
import os
import re
from tqdm import tqdm
from pathlib import Path
import pandas as pd

# read data from the csv file (from the location it is stored)
data_csv = Path("./wikihowAll.csv")
df = pd.read_csv(data_csv).astype(str)

print("Opening The Title Files")
with open("all_test.txt", 'r') as all_test_file:
    all_test = all_test_file.read().splitlines()
with open("all_train.txt", 'r') as all_train_file:
    all_train = all_train_file.read().splitlines()
with open("all_val.txt", 'r') as all_val_file:
    all_val = all_val_file.read().splitlines()
print("Title Files Opened Successfully")

dataset = {
    "train": {"source": [], "target": []},
    "val": {"source": [], "target": []},
    "test": {"source": [], "target": []}
}

# The path where the articles are to be saved
path = "wikihow"
if not os.path.exists(path): os.makedirs(path)

# go over the all the articles in the data file
for idx, row in tqdm(df.iterrows(), desc="Loading and Splitting", total=len(df)):
    abstract = row["headline"]      # headline is the column representing the summary sentences
    article = row["text"]           # text is the column representing the article

    #  a threshold is used to remove short articles with long summaries as well as articles with no summary
    if len(abstract) < (0.75*len(article)):
        # remove extra commas in abstracts
        abstract = abstract.replace(".,",".")
        # remove extra commas in articles
        article = re.sub(r'[.]+[\n]+[,]',".\n", article)
        # remove extra spacing
        article = article.strip()
        abstract = abstract.strip()
        # remove newline characters
        article = article.replace("\n", " ")
        abstract = abstract.replace("\n", " ")
        

        # titles are created using the alphanumeric characters from the article titles
        title = row['title']
        title = "".join(x for x in title if x.isalnum())
        
        if title in all_train:
            all_train.remove(title)
            split_name = "train"
        elif title in all_val:
            all_val.remove(title)
            split_name = "val"
        elif title in all_test:
            all_test.remove(title)
            split_name = "test"
        else:
            print("Missing Document Detected! Title: " + str(title))
            continue
        
        dataset[split_name]["source"].append(article)
        dataset[split_name]["target"].append(abstract)

for split_name, current_split in tqdm(dataset.items(), desc="Split"):
    for source_or_target, data in tqdm(current_split.items(), desc="Source and Target"):
        with open(os.path.join(path, split_name+"."+source_or_target), 'w') as f:
            for item in tqdm(data, desc="Document"):
                f.write("%s\n" % item)