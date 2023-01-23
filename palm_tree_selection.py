#!/usr/bin/env python

###Identify trees affected by drought from a distribution of % loss###

##import libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

##load dataset
plot_1 = pd.read_excel('F:/Working Projects/Imperial Palms/Filtered data/B034_1998_filtered.xlsx')

##clean and data
#remove nans and make all values numeric
plot_1['nb_fr'] = pd.to_numeric(plot_1['nb_fr'], errors='coerce')
plot_1.fillna(value=0,inplace=True)

##identification and format dataset to select trees for continued analysis
#plot_1['tree group'] = plot_1['tree_id'].str.replace(r'_\d{4}$', '', regex=True)

##creat list of trees to match in for loop
tree_list = sorted(plot_1['tree group'].unique())

##identify trees that are most affected by drought period
#similarly loop through and flag trees that have a certain amount less

                ##########First drought##########
less_than_quater = []
greater_than_quater = []
loss_range = []

#make a list of percentage loss
for tree in tree_list:

    tree_1 = plot_1[plot_1['tree group'] == tree]
    tree_1_group = tree_1.groupby('year').sum().reset_index()
    yield_mean1 = tree_1_group[tree_1_group['year'] == 2007]
    #yield_mean2 = tree_1_group[tree_1_group['year'] == 2007]
    yield_drop = tree_1_group[tree_1_group['year'] == 2008]
    #fr_yield_prior = (float(yield_mean1['nb_fr']) + float(yield_mean2['nb_fr']))/2
    fr_yield_prior = yield_mean1['nb_fr']
    fr_yield_after = yield_drop['nb_fr']
    #try:
    #    fr_loss = ((int(fr_yield_prior)-int(fr_yield_after))/int(fr_yield_prior)*100)
    #except ZeroDivisionError:
    #    fr_loss = 0
    #else:
    #    break
    fr_loss = ((fr_yield_prior.iloc[0]-fr_yield_after.iloc[0])/fr_yield_prior.iloc[0]*100)
    loss_range.append(fr_loss)

#remove nans
cleanedList = [x for x in loss_range if str(x) != 'nan']
cleanedList = [x for x in cleanedList if str(x) != '-inf']

##clean percentage distribution and remove outliers
#function to identify upper lower and upper quartile to remove outliers
def outliers(df):
    Q1= np.quantile(df, 0.25)
    Q3 = np.quantile(df, 0.75)
    IQR = Q3 - Q1
    upper_limit = Q3 + (1.5 * IQR)
    lower_limit = Q1 - (1.5 * IQR)
    return upper_limit, lower_limit
upper, lower = outliers(cleanedList)

#list comprehension to remove outliers
loss_range_rm = [i for i in loss_range if (i > lower) & (i < upper)]
first_drought = sns.histplot(loss_range_rm).set(title='Percnetage change distribution',ylabel='Count', xlabel='Percentage of fruit yield change')
plt.tight_layout()
plt.show()
#upper, lower = outliers(loss_range_rm)

##set upper and lower quartile to selecetl likely drought resistant and 
#susceptible trees
def up_low_quatil(df):
    Q1= np.quantile(df, 0.25)
    Q3 = np.quantile(df, 0.75)
    return Q3, Q1
upper, lower = up_low_quatil(loss_range_rm)

#select trees in upper and lower percentiles
for tree in tree_list:

    tree_1 = plot_1[plot_1['tree group'] == tree]
    tree_1_group = tree_1.groupby('year').sum().reset_index()
    yield_mean1 = tree_1_group[tree_1_group['year'] == 2007]
    #yield_mean2 = tree_1_group[tree_1_group['year'] == 2007]
    yield_drop = tree_1_group[tree_1_group['year'] == 2008]
    #fr_yield_mean_prior = (float(yield_mean1['nb_fr']) + float(yield_mean2['nb_fr']))/2
    fr_yield_prior = yield_mean1['nb_fr']
    fr_yield_after = yield_drop['nb_fr']
    fr_loss = ((fr_yield_prior.iloc[0]-fr_yield_after.iloc[0])/fr_yield_prior.iloc[0]*100)
    st_tree = str(tree)

    if fr_loss == float('-inf'):
        pass
    elif fr_loss >= upper:
        greater_than_quater.append(st_tree)
    elif fr_loss <= lower:
        less_than_quater.append(st_tree)

                  ##########Second drought##########
less_than_quater2 = []
greater_than_quater2 = []
loss_range2 = []

#make a list of percentage loss
for tree in tree_list:

    tree_1 = plot_1[plot_1['tree group'] == tree]
    tree_1_group = tree_1.groupby('year').sum().reset_index()
    yield_mean1 = tree_1_group[tree_1_group['year'] == 2016]
    #yield_mean2 = tree_1_group[tree_1_group['year'] == 2007]
    yield_drop = tree_1_group[tree_1_group['year'] == 2017]
    #fr_yield_prior = (float(yield_mean1['nb_fr']) + float(yield_mean2['nb_fr']))/2
    fr_yield_prior = yield_mean1['nb_fr']
    fr_yield_after = yield_drop['nb_fr']
    #try:
    #    fr_loss = ((int(fr_yield_prior)-int(fr_yield_after))/int(fr_yield_prior)*100)
    #except ZeroDivisionError:
    #    fr_loss = 0
    #else:
    #    break
    fr_loss = ((fr_yield_prior.iloc[0]-fr_yield_after.iloc[0])/fr_yield_prior.iloc[0]*100)
    loss_range2.append(fr_loss)

#remove nans
cleanedList2 = [x for x in loss_range2 if str(x) != 'nan']

##clean percentage distribution and remove outliers
#function to identify upper lower and upper quartile to remove outliers
upper2, lower2 = outliers(cleanedList2)

#list comprehension to remove outliers
loss_range_rm2 = [i for i in cleanedList2 if (i > lower2) & (i < upper2)]
second_drought = sns.histplot(loss_range_rm2).set(title='Percnetage change distribution',ylabel='Count', xlabel='Percentage of fruit yield change')
plt.tight_layout()
plt.show()

##set upper and lower quartile to selecetl likely drought resistant and 
#susceptible trees
upper2, lower2 = up_low_quatil(loss_range_rm2)

#select trees in upper and lower percentiles
for tree in tree_list:

    tree_1 = plot_1[plot_1['tree group'] == tree]
    tree_1_group = tree_1.groupby('year').sum().reset_index()
    yield_mean1 = tree_1_group[tree_1_group['year'] == 2016]
    #yield_mean2 = tree_1_group[tree_1_group['year'] == 2007]
    yield_drop = tree_1_group[tree_1_group['year'] == 2017]
    #fr_yield_mean_prior = (float(yield_mean1['nb_fr']) + float(yield_mean2['nb_fr']))/2
    fr_yield_prior2 = yield_mean1['nb_fr']
    fr_yield_after2 = yield_drop['nb_fr']
    fr_loss2 = ((fr_yield_prior2.iloc[0]-fr_yield_after2.iloc[0])/fr_yield_prior2.iloc[0]*100)
    st_tree2 = str(tree)

    if fr_loss2 == float('-inf'):
        pass
    if fr_loss2 >= upper2:
        greater_than_quater2.append(st_tree2)
    elif fr_loss2 <= lower2:
        less_than_quater2.append(st_tree2)

                ##########Cross validation##########

cross_validated_tolerant = set(less_than_quater) & set(less_than_quater2)
cross_validated_susceptible = set(greater_than_quater) & set(greater_than_quater2)

with open("F:/Working Projects/Imperial Palms/Identified trees/B052_1997_tolerant_inf_rem.txt", "w") as output:
    output.write(str(cross_validated_tolerant))
with open("F:/Working Projects/Imperial Palms/Identified trees/B052_1997_susceptible.txt", "w") as output:
    output.write(str(cross_validated_susceptible))

