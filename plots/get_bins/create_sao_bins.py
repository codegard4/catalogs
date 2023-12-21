import numpy as np
import math
import pickle
import os
from tqdm import tqdm 

def radToDeg(radians):
    return math.degrees(radians)

def createSAOBins():
    a = np.zeros(shape=(360,180))
    path = os.getcwd() #path to sao.dat file
    with open(f'{path}/sao.dat', 'r') as f:
        lines = f.readlines()
        for line in tqdm(lines): 
            line = str.encode(line)
            r = floor(radToDeg(float(line[183:193].decode())))
            d = -floor(radToDeg(float(line[193:204].decode())))
            if(d > -50 or d < -20):
                a[r][-d-90] += 1
    
    with open("./sao_bins", "wb") as f:
            pickle.dump(a, f)
    # return a

if __name__ == "__main__":
    createSAOBins()