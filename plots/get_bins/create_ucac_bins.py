import numpy as np
import math
import pickle
from tqdm import tqdm
import os
from math import floor

def createUCACBins():
    ra_bins = 360
    dec_bins = 180
    path = ""
    bins = np.zeros(360*180).reshape(360, 180)
    path = ""#path to u4index.asc file
    with open(f'{path}/u4index.asc', 'r') as f:
        i = 0
        for line in tqdm(f):
            i+=1
            x = line.split(" ")
            x = [i for i in x if i]
            count = int(x[1])
            dec = floor(-90 + 0.2*(int(x[2])))
            ra = floor((int(x[3])-1) / 4)
            bins[ra][dec+89] = count
    with open(f"ucac_bins", "wb") as f:
        pickle.dump(bins, f)
    # return bins

if __name__ == "__main__":
    createUCACBins()
