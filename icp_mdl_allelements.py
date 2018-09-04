from os.path import join
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import seaborn as sns
from matplotlib import rcParams

"""Functions"""
def find_outlier_index_iqr(data,para=None):#iqr means internal quartile range
    ## data needs to be a pandas.series type, returns you a list of index
    para=para or 1.5
    quartile1,quartile3=np.percentile(data,[25,75])
    iqr=quartile3-quartile1
    lowbound=quartile1-(iqr*para)
    upbound=quartile3+(iqr*para)
    newdata=data.where((data>upbound)|(data<lowbound))## returns data.series type
    outlier_data=newdata[newdata.notnull()]## the not NaN values are outliers
    return outlier_data.index.tolist() # returns list type

"""Load results"""
#filename=input("Enter the csv file name: ")
filename="QC.xlsx"
path="C:\\users\yyan\\Documents\\Data\\ICPMS\\Alldata"
filepath=join(path,filename)
df=pd.read_excel(filepath,sheet_name="LRB_2018",parse_cols="A:AF")

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

"""Plot"""
### Setup the figure with plots
"""fig=plt.figure(figsize=(12,6))
As_hist=fig.add_subplot(121)
Cd_hist=fig.add_subplot(122)
As_scatter=fig.add_subplot(221)
Cd_scatter=fig.add_subplot(222)"""
## Histogram
"""As_hist.hist(df.As,bins=100)
As_hist.set_xlabel("As ppb")
Cd_hist.hist(df.Cd,bins=100)
Cd_hist.set_xlabel("Cd ppb")"""
#---Scatter plot---------
"""num_all_test=df.index.values
As_scatter.scatter(num_all_test,df.As)
As_scatter.set_xlabel("As")
Cd_scatter.scatter(num_all_test,df.Cd)
Cd_scatter.set_xlabel("Cd")"""

"""Output"""
#plt.show()

"""End of script"""
print("end of script")