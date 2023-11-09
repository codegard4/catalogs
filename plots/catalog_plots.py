# import math
# import pandas as pd
# import math
# import pickle
# import plotly as plt
# import plotly.express as px
# import numpy as np
# from datetime import datetime
# from astropy import coordinates as coord
# from astropy import units as u
# from astropy.time import Time
# from tqdm import tqdm
# from astropy.coordinates import SkyCoord
# from datetime import datetime
# from astropy.time import Time

import math
from datetime import datetime
import pickle

import pandas as pd
import plotly as plt
import plotly.express as px
import numpy as np
from tqdm import tqdm


def createSAOBins():
    sao_num,dec_rad_2000,ra_rad_2000 = [],[],[]
    with open('../Plots/sao.dat', 'r') as f:
        lines = f.readlines()
        for line in tqdm(lines): 
            line = str.encode(line)
            sao_num.append(int(line[0:6].decode()))
            ra_rad_2000.append(float(line[183:193].decode()))
            dec_rad_2000.append(float(line[193:204].decode()))
    catalog = pd.DataFrame(list(zip(sao_num,dec_rad_2000,ra_rad_2000)), columns = ['sao_num','dec_rad_2000','ra_rad_2000'])
    xarr = np.array(catalog.iloc[:,2]) #RA
    yarr = np.array(catalog.iloc[:,1]) #DEC
    print(max(xarr)*180/math.pi)
    print(max(yarr)*180/math.pi)
    print(max(yarr)*90/math.pi)
    a = np.zeros(shape=(180, 45))
    for i in tqdm(range(len(xarr))):
        # rastar = int((xarr[i] * 180)/math.pi)
        # decstar = int((yarr[i] * 180)/math.pi)
        
        rastar = int(xarr[i] * 90/math.pi)
        decstar = int(yarr[i] * 90/math.pi)
        a[rastar][decstar] = a[rastar][decstar]+1
        if(decstar > 45):
            print(decstar)
    with open("../Plots/sao_bins", "wb") as f:
            pickle.dump(a, f)
          
        
def getSAOBins():
    try:
        with open("../Plots/sao_bins", "rb") as f:
            unpickled_array = pickle.load(f)
        return unpickled_array
    except Exception as e: 
        print(e)
        bins_sao = createSAOBins()
        return bins_sao
    
def plotSAO():
    a = getSAOBins()
    b = [list(x) for x in zip(*a)]
    ras, decs = scales([360,0],[0,90],180,45)
    fig = px.imshow(b,
            labels=dict(x="Right Ascension", y="Declination"),
            y = decs,
            x = ras,
            title = "sao2000 Sky coverage"
           )
    fig.show()
    plt.offline.plot(fig, filename='../Plots/sao2000.html')

def scales(ra_range, dec_range, rabins, decbins):
    ra = np.arange(ra_range[1],ra_range[0],-(ra_range[1] - ra_range[0]) / rabins)
    dec = np.arange(dec_range[1],dec_range[0],-(dec_range[1] - dec_range[0]) / decbins)
    decs = []
    ras = []
    for i in dec:
        decs.append(str(int(i)))
    for i in ra:
        ras.append(str(int(i)))
    # print(ras, decs)
    return ras, decs

def createUCACBins():
    ra_bins = 360
    dec_bins = 180
    assert(ra_bins <= 1440)
    assert(dec_bins <=900)
    rafac = int(1440/ra_bins)
    decfac = int(900/dec_bins)
    bins = np.arange(ra_bins * dec_bins).reshape(ra_bins, dec_bins)
    with open(f'..ucac4/u4i/u4index.asc', 'r') as f:
        for line in f:
            x = line.split(" ")
            x = [i for i in x if i]
            count = int(x[1])
            dec = int(x[2])
            ra = int(x[3])
            for i in range(0,dec_bins):
                for j in range(0,ra_bins):
                    if(dec // decfac == i):
                        if(ra // rafac == j):
                            bins[j][i] = bins[j][i] + count
    with open("../Plots/ucac_bins", "wb") as f:
        pickle.dump(bins, f)
    return bins


def getUCACBins():
    try:
        with open("../Plots/ucac_bins", "rb") as f:
            unpickled_array = pickle.load(f)
        return unpickled_array
    except Exception as e: 
        print(e)
        bins_ucac = createUCACBins()
        return bins_ucac

def plotUCAC():
    bins_raw = getUCACBins()
    bins_ucac = []
    for row in range(len(bins_raw)):
        bins_ucac.append(bins_raw[row].split(" "))
    ras, decs = scales([0,360],[-90,90],360,180)
    a = [list(x) for x in zip(*bins_ucac)]
    fig = px.imshow(a,
                    labels=dict(x="Right Ascension", y="Declination"),
                    y = decs,
                    x = ras,
                    title = "UCAC4 Sky Coverage"
                   )
    fig.update_layout(
    autosize=False,
    width=800,
    height=600)
    fig.show()
    plt.offline.plot(fig, filename='../Plots/ucac4.html')

if __name__ == "__main__":
    # createSAOBins()
    # createUCACBins()
    getUCACBins()
    getSAOBins()
    plotSAO()
    plotUCAC()
