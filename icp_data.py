from os.path import join
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import seaborn as sns
from matplotlib import rcParams

"""Functions"""

"""Load results"""
#filename=input("Enter the csv file name: ")
filename="QC_V3.xlsx"
path='C:/Users/yyan/Documents/Data/ICPMS/Alldata/'
filepath=join(path,filename)
df=pd.read_excel(filepath,sheetname="LRB_2018",parse_cols="A:AF")

"""Data filter process"""
#description=df.describe() # statistics of element Be to U
### Look for elements that has NaN values
nanlist=[]
nan=df.isnull().any()
nan_index=nan.index ### Same as df.column.values()
for i in range(0,nan_index.size):
    if nan[i]==True:
        nanlist.append(nan_index[i])
### If nanlist contains "date_of_run", remove that row whose date_of_run is NaN
if "Date_of_run" in nanlist:
    df=df.dropna(subset=[0]) ## 0 indicated date_of_run is 0th column
### Create element list that has no NaN values
ele_list=list(df)
ele_list.pop(0) ## remove date_of_run from element list
ele_nonan_list=[] ## create a list of elements whose value are not NaN
for item in ele_list:
    if item not in nanlist:
        ele_nonan_list.append(item)

"""Statistics"""
### Cacluate MDL of each element
df_MDL=pd.DataFrame(index=ele_list,columns=["MDL"])
for item in ele_nonan_list:
    mean=df[item].mean()
    std=df[item].std()
    MDL=mean+2.365*std ##2.365 is t student 99% and >100 samples
    df_MDL.loc[item,"MDL"]=MDL
for item in nanlist:
    mean=df[item].dropna().mean()## Note this is unnecessary b/c the mean function does not count NaN values, so not nuecessary to drop NaN values
    std=df[item].dropna().std() ## Not necessary as above
    MDL=mean+2.365*std
    df_MDL.loc[item,"MDL"]=MDL

"""Histogram Plot"""
### Use As as first example
fig=plt.figure(figsize=(12,6))
As_hist=fig.add_subplot(121)
Cd_hist=fig.add_subplot(122)
Hg_hist=fig.add_subplot(221)
Pd_hist=fig.add_subplot(222)

As_hist.hist(df.As,bins=80)
#As_hist.set_xlable("As ppb")


"""Output"""
#print(filepath)
#print(df.head())
#print(description)
#print(nanlist)
#plt.show()

"""Association rule"""

"""End of script"""
print("end of script")
