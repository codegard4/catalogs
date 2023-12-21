import csv
import pickle
import numpy as np
from tqdm import tqdm
import os
def createGAIABins():
    ra_bins = 360
    dec_bins = 180
    path = ""#path to get to gaia catalog
    bins = np.zeros(ra_bins * dec_bins).reshape(ra_bins, dec_bins)
    for ra in tqdm(range(0,359)): 
        ra2 = "{:>03}".format(ra+1)
        folder = f"ra+{ra1}+{ra2}/"
        for dec in range(0,90):
            dec1 = "{:>03}".format(dec)
            dec2 = "{:>03}".format(dec+1)
            file = f"dec-{dec2}-{dec1}.csv"
            with open(path+folder+file, 'r') as f:
                csvFile = csv.reader(f)
                count = (sum(1 for row in csvFile))
                bins[ra][-dec-90] += count
        for dec in range(1,90):
            dec1 = "{:>03}".format(dec)
            dec2 = "{:>03}".format(dec+1)
            file = f"dec+{dec1}+{dec2}.csv"
            with open(path+folder+file, 'r') as f:
                csvFile = csv.reader(f)
                count = (sum(1 for row in csvFile))
                bins[ra][dec+90] += count
        file = "dec-000+001.csv"
        with open(path+folder+file, 'r') as f:
            csvFile = csv.reader(f)
            count = (sum(1 for row in csvFile))
            bins[ra][0] += count     
    with open(f"{os.getcwd()}/gaia_bins", "wb") as f:
        pickle.dump(bins, f)
    # return bins

if __name__ == "__main__":
    bins = createGAIABins()