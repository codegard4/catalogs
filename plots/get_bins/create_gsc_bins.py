import csv
import pickle
import numpy as np
from tqdm import tqdm
import os
def createGSCBins():
    ra_bins = 360
    dec_bins = 180
    bins = np.zeros(ra_bins * dec_bins).reshape(ra_bins, dec_bins)
    path = "" #path to gsc catalog csv folder
    for decl in tqdm(range(180)):
        for decl_decimal in range(10):
            for ra in range(360):
                declf = "{:>03}".format(decl)
                decl_decimalf = "{:>04}".format(decl_decimal)
                raf = "{:>03}".format(ra)
                file = f"{declf}/{decl_decimalf}/{raf}.csv"
                try:
                    with open(f'{path}/{file}', 'r') as f:
                        csvFile = csv.reader(f)
                        count = (sum(1 for row in csvFile))
                        bins[ra][decl] += count
                except Exception as e:
                    pass
    with open(f"{os.getcwd()}/gsc240_bins", "wb") as f:
        pickle.dump(bins, f)
    # return bins

if __name__ == "__main__":
    createGSCBins()