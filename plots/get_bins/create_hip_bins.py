import numpy as np
import math
import pickle
import os
from tqdm import tqdm 

def createHIPBins():
    a = np.zeros(shape=(360,180))
    path = ""#path to hip csv file
    with open(f'{path}/hip_main.csv', 'r') as f:
        lines = f.readlines()
        i = 0
        for line in lines:
            line = line.split(",")
            try: 
                r,d = float(line[8]), float(line[9])
                a[floor(r)][floor(d)-90] += 1
            except:
                pass
    with open(f"{os.getcwd()}/hip_bins", "wb") as f:
        pickle.dump(a, f)
    # return a
if __name__ == "__main__":
    createHIPBins()
            
