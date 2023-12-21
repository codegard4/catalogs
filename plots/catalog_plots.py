import math
import pickle
import pandas as pd
import plotly as plt
import plotly.express as px
import numpy as np
from datetime import datetime
from tqdm import tqdm
import os

def scales(ra_range, dec_range, rabins, decbins):
    """
    Generates scales for RA and Declination based on specified ranges and number of bins.
    Args:
        ra_range (List): Range of RA values.
        dec_range (List): Range of Declination values.
        rabins (int): Number of RA bins.
        decbins (int): Number of Declination bins.
    Returns:
        Tuple: Lists of RA and Declination scales.
    """
    ra = np.arange(ra_range[1],ra_range[0],-(ra_range[1] - ra_range[0]) / rabins)
    dec = np.arange(dec_range[1],dec_range[0],-(dec_range[1] - dec_range[0]) / decbins)
    decs = []
    ras = []
    for i in dec:
        decs.append(str(int(i)))
    for i in ra:
        ras.append(str(int(i)))
    return ras, decs

def getSAOBins():
    """
    Retrieves SAO bins from the pickle file. 
    Returns:
        Numpy array: SAO bins.
    """
    try:
        with open(f"{os.getcwd()}/sao_bins", "rb") as f:
            unpickled_array = pickle.load(f)
        return unpickled_array
    except Exception as e:
        print(e)
    
def plotSAO():
    """
    Plots SAO Sky coverage using the SAO bins.
    Returns:
        None
    """
    a = getSAOBins()
    b = [list(x) for x in zip(*a)]
    ras, decs = scales([360, 0],[-90, 90],360, 180)
    fig = px.imshow(
        b,
        labels=dict(x="Right Ascension", y="Declination"),
        y = decs,
        x = ras,
        title = "SAO2000 Sky coverage"
    )
    fig.update_layout(
    autosize = False,
    width = 800,
    height = 600)
    fig.show()
    plt.offline.plot(fig, filename= f'{os.getcwd()}/sao2000.html')

def getUCACBins():
    """
    Retrieves UCAC4 bins from the pickle file.
    Returns:
        Numpy array: UCAC4 bins.
    """
    try:
        with open(f"{os.getcwd()}/ucac_bins", "rb") as f:
            unpickled_array = pickle.load(f)
        return unpickled_array
    except Exception as e: 
        print(e)

def plotUCAC():
    """
    Plots UCAC4 Sky coverage using the UCAC4 bins.
    Returns:
        None
    """
    bins = getUCACBins()
    ras, decs = scales([360, 0],[-90, 90], 360, 180)
    a = [list(x) for x in zip(*bins)]
    fig = px.imshow(
        a,
        labels = dict(x="Right Ascension", y = "Declination"),
        y = decs,
        x = ras,
        title = "UCAC Sky Coverage"
    )
    fig.update_layout(
    autosize = False,
    width = 800,
    height = 600)
    fig.show()
    plt.offline.plot(fig, filename = f'{os.getcwd()}/ucac4.html')

def getGSCBins():
    """
    Retrieves GSC bins from the pickle file.
    Returns:
        Numpy array: GSC bins.
    """
    try:
        with open(f"{os.getcwd()}/gsc240_bins", "rb") as f:
            unpickled_array = pickle.load(f)
        return unpickled_array
    except Exception as e: 
        print(e)
        
def plotGSC():
    """
    Plots GSC Sky coverage using the GSC bins.
    Returns:
        None
    """
    a = getGSCBins()
    b = [list(x) for x in zip(*a)]
    ras, decs = scales([360,0],[-90,90],360,180)
    fig = px.imshow(
        b,
        labels=dict(x="Right Ascension", y = "Declination"),
        y = decs,
        x = ras,
        title = "GSC240 Sky coverage"
    )
    fig.update_layout(
    autosize = False,
    width = 800,
    height = 600)
    fig.show()
    plt.offline.plot(fig, filename = f'{os.getcwd()}/gsc240.html')

    
def getHIPBins():
    """
    Retrieves HIP bins from the pickle file.
    Returns:
        Numpy array: HIP bins.
    """
    try:
        with open(f"{os.getcwd()}/hip_bins", "rb") as f:
            unpickled_array = pickle.load(f)
        return unpickled_array
    except Exception as e: 
        print(e)

def plotHIP():
    """
    Plots HIP Sky coverage using the HIP bins.
    Returns:
        None
    """
    bins = getHIPBins()
    ras, decs = scales([360, 0],[-90, 90], 360, 180)
    a = [list(x) for x in zip(*bins)]
    fig = px.imshow(
        a,
        labels = dict(x="Right Ascension", y = "Declination"),
        y = decs,
        x = ras,
        title = "HIP Sky Coverage"
    )
    fig.update_layout(
    autosize = False,
    width = 800,
    height = 600)
    fig.show()
    plt.offline.plot(fig, filename = f'{os.getcwd()}/hip.html')
    
def get2MASSBins():
    """
    Retrieves 2MASS bins from the pickle file.
    Returns:
        Numpy array: 2MASS bins.
    """
    try:
        with open(f"{os.getcwd()}/2mass_bins", "rb") as f:
            unpickled_array = pickle.load(f)
        return unpickled_array
    except Exception as e: 
        print(e)
    
def plot2MASS():
    """
    Plots 2MASS Sky coverage using the 2MASS bins.
    Returns:
        None
    """
    bins = get2MASSBins()
    
    ras, decs = scales([360, 0],[-90, 90], 360, 180)
    a = [list(x) for x in zip(*bins)]
    # print(bins)
    fig = px.imshow(
        a,
        labels = dict(x="Right Ascension", y = "Declination"),
        y = decs,
        x = ras,
        title = "2MASS Sky Coverage"
    )
    fig.update_layout(
    autosize = False,
    width = 800,
    height = 600)
    fig.show()
    plt.offline.plot(fig, filename = f'{os.getcwd()}/2mass.html')

def getGAIABins():
    """
    Retrieves GAIA bins from the pickle file
    Returns:
        Numpy array: GAIA bins.
    """
    try:
        with open(f"{os.getcwd()}/gaia_bins", "rb") as f:
            unpickled_array = pickle.load(f)
        return unpickled_array
    except Exception as e: 
        print(e)
    
    
def plotGAIA():
    """
    Plots GAIA Sky coverage using the GAIA bins.
    Returns:
        None
    """
    bins = getGAIABins()
    
    ras, decs = scales([360, 0],[-90, 90], 360, 180)
    a = [list(x) for x in zip(*bins)]
    fig = px.imshow(
        a,
        labels = dict(x="Right Ascension", y = "Declination"),
        y = decs,
        x = ras,
        title = "GAIA Sky Coverage"
    )
    fig.update_layout(
    autosize = False,
    width = 800,
    height = 600)
    fig.show()
    plt.offline.plot(fig, filename = f'{os.getcwd()}/gaia.html')
    
if __name__ == "__main__":
    plotSAO()
    plotUCAC()
    plotGSC()
    plotHIP()
    plot2MASS()
    plotGAIA()