file1 = open('score_file_v17.txt', 'r')
from matplotlib import colors
from operator import itemgetter
import numpy as np
from scipy.stats import ttest_ind
from scipy.special import stdtr
from error_analysis import main
file2 = open('score_file_v18.txt', 'r')
text1 = file1.read()
text1 = text1.splitlines()

text2 = file2.read()
text2 = text2.splitlines()
total_sum1 = []
total_sum2 = []

def mean(a):
    return sum(a) / len(a)

a = [0,2,3,4]

for i in range(2,len(text1),16):
    total_sum1.append(itemgetter(*a)(text1[i].split(', ')))
for i in range(2,len(text2),16):
    total_sum2.append(itemgetter(*a)(text2[i].split(', ')))
##    print(itemgetter(*a)(text2[i].split(', ')))

total_sum1 = [[float(i) for i in a] for a in total_sum1]
total_sum2 = [[float(i) for i in a] for a in total_sum2]
for x in total_sum1:
    if sum(x) >0:
        print(x)
highSum1 = [tot  for tot in total_sum1 if sum(tot)>0]
highSum2 = [tot for tot in total_sum2 if sum(tot)>0] 

avetot1 = list(map(mean, zip(*total_sum1)))
avetot2 = list(map(mean, zip(*total_sum2)))
avehigh1 = list(map(mean, zip(*highSum1)))
avehigh2 = list(map(mean, zip(*highSum2)))
print(avetot1, avetot2, avehigh1, avehigh2)

tot1list = list(zip(*total_sum1))
tot2list = list(zip(*total_sum2))
high1list = list(zip(*highSum1))
high2list = list(zip(*highSum2))

print(len(highSum1))
print(len(highSum2))
print(len(total_sum1))
print(len(total_sum2))



t, p = ttest_ind(tot1list[0], tot1list[2], equal_var=False)
print("ttest_ind_tot1_google_hybrid: t = %g  p = %g" % (t, p))

t, p = ttest_ind(tot1list[1], tot1list[2], equal_var=False)
print("ttest_ind_tot1_ngram_hybrid: t = %g  p = %g" % (t, p))

t, p = ttest_ind(tot1list[3], tot1list[2], equal_var=False)
print("ttest_ind_tot1_pm_hybrid: t = %g  p = %g" % (t, p))

t, p = ttest_ind(tot2list[0], tot2list[2], equal_var=False)
print("ttest_ind_tot2_google_hybrid: t = %g  p = %g" % (t, p))

t, p = ttest_ind(tot2list[1], tot2list[2], equal_var=False)
print("ttest_ind_tot2_ngram_hybrid: t = %g  p = %g" % (t, p))

t, p = ttest_ind(tot2list[3], tot2list[2], equal_var=False)
print("ttest_ind_tot2_pm_hybrid: t = %g  p = %g" % (t, p))

t, p = ttest_ind(high1list[0], high1list[2], equal_var=False)
print("ttest_ind_high1_google_hybrid: t = %g  p = %g" % (t, p))

t, p = ttest_ind(high1list[1], high1list[2], equal_var=False)
print("ttest_ind_high1_ngram_hybrid: t = %g  p = %g" % (t, p))

t, p = ttest_ind(high1list[3], high1list[2], equal_var=False)
print("ttest_ind_high1_pm_hybrid: t = %g  p = %g" % (t, p))

t, p = ttest_ind(high2list[0], high2list[2], equal_var=False)
print("ttest_ind_high2_google_hybrid: t = %g  p = %g" % (t, p))

t, p = ttest_ind(high2list[1], high2list[2], equal_var=False)
print("ttest_ind_high2_ngram_hybrid: t = %g  p = %g" % (t, p))

t, p = ttest_ind(high2list[3], high2list[2], equal_var=False)
print("ttest_ind_high2_pm_hybrid: t = %g  p = %g" % (t, p))


file3 = open('score_file_v20.txt', 'w')


for line in highSum2:
    line = [str(x) for x in line]
    file3.write(', '.join(line) + '\n')
file3.close()
g_list = []
nga = []
pm2 =[]
hb =[]

count1 = 0
for i in range(4,len(text1),16):
    count1 += 1
    g_list.append([a for a in text1[i].split(', ')])
    nga.append([a for a in text1[i+1].split(', ')])
    pm2.append([a for a in text1[i+3].split(', ')])
    hb.append([a for a in text1[i+6].split(', ')])

cov1 = [len([ a for a in g_list if len(a[0])]),len([ a for a in nga if len(a[0])]), len([ a for a in hb if len(a[0])]), len([ a for a in pm2 if len(a[0])])]
cov1 = [x/count1 for x in cov1]
print(cov1)

g_list = []
nga = []
pm2 =[]
hb =[]



count2 = 0
for i in range(4,len(text2),16):
    count2 += 1
    g_list.append([a for a in text2[i].split(', ')])
    nga.append([a for a in text2[i+1].split(', ')])
    pm2.append([a for a in text2[i+3].split(', ')])
    hb.append([a for a in text2[i+6].split(', ')])


cov2 = [len([ a for a in g_list if len(a[0])]),len([ a for a in nga if len(a[0])]), len([ a for a in hb if len(a[0])]), len([ a for a in pm2 if len(a[0])])]
print(cov2)
cov2 = [x/count2 for x in cov2]
##
##print(len([ a for a in g_list if len(a[0])]))
##print(len([ a for a in nga if len(a[0])]))
##print(len([ a for a in pm2 if len(a[0])]))
##print(len([ a for a in hb if len(a[0])]))




import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
##
##raw_data = {'Model': ['Google', 'N-gram-anchor', 'Hybrid', 'Probabilistic Model'],
##        'Random Set': avehigh1,
##        'Set2': avehigh2}
##df = pd.DataFrame(raw_data, columns = ['Model', 'Random Set', 'Set2'])
##
### Setting the positions and width for the bars
##pos = list(range(len(df['Random Set']))) 
##width = 0.25 
##
### Plotting the bars
##fig, ax = plt.subplots(figsize=(10,5))
##
### Create a bar with pre_score data,
### in position pos,
##plt.bar(pos, 
##        #using df['pre_score'] data,
##        df['Random Set'], 
##        # of width
##        width, 
##        # with alpha 0.5
##        alpha=0.5, 
##        # with color
##        color='#EE3124', 
##        # with label the first value in first_name
##        label=df['Model'][0]) 
##
### Create a bar with mid_score data,
### in position pos + some width buffer,
##plt.bar([p + width for p in pos], 
##        #using df['mid_score'] data,
##        df['Set2'],
##        # of width
##        width, 
##        # with alpha 0.5
##        alpha=0.25, 
##        # with color
##        color='blue', 
##        # with label the second value in first_name
##        label=df['Model'][1]) 
##
##
### Set the y axis label
##ax.set_ylabel('Score')
##
### Set the chart's title
##ax.set_title('Mean Reciprocal Rank')
##
### Set the position of the x ticks
##ax.set_xticks([p +1 * width for p in pos])
##
### Set the labels for the x ticks
##ax.set_xticklabels(df['Model'])
##
### Setting the x-axis and y-axis limits
##plt.xlim(min(pos)-width, max(pos)+width*4)
##plt.ylim([0, max(df['Random Set'] + df['Set2']-0.4)] )
##
### Adding the legend and showing the plot
##plt.legend(['Random Set', 'Selected Set'], loc='upper right')
##plt.show()
##
##raw_data = {'Model': ['Google', 'N-gram-anchor', 'Hybrid', 'Probabilistic Model'],
##        'Random Set': avetot1,
##        'Set2': avetot2}
##df = pd.DataFrame(raw_data, columns = ['Model', 'Random Set', 'Set2'])
##
### Setting the positions and width for the bars
##pos = list(range(len(df['Random Set']))) 
##width = 0.25 
##
### Plotting the bars
##fig, ax = plt.subplots(figsize=(10,5))
##
### Create a bar with pre_score data,
### in position pos,
##plt.bar(pos, 
##        #using df['pre_score'] data,
##        df['Random Set'], 
##        # of width
##        width, 
##        # with alpha 0.5
##        alpha=0.5, 
##        # with color
##        color='#EE3124', 
##        # with label the first value in first_name
##        label=df['Model'][0]) 
##
### Create a bar with mid_score data,
### in position pos + some width buffer,
##plt.bar([p + width for p in pos], 
##        #using df['mid_score'] data,
##        df['Set2'],
##        # of width
##        width, 
##        # with alpha 0.5
##        alpha=0.25, 
##        # with color
##        color='blue', 
##        # with label the second value in first_name
##        label=df['Model'][1]) 
##
##
### Set the y axis label
##ax.set_ylabel('Score')
##
### Set the chart's title
##ax.set_title('Mean Reciprocal Rank')
##
### Set the position of the x ticks
##ax.set_xticks([p +1 * width for p in pos])
##
### Set the labels for the x ticks
##ax.set_xticklabels(df['Model'])
##
### Setting the x-axis and y-axis limits
##plt.xlim(min(pos)-width, max(pos)+width*4)
##plt.ylim([0, max(df['Random Set'] + df['Set2']-0.3)] )
##
### Adding the legend and showing the plot
##plt.legend(['Random Set', 'Selected Set'], loc='upper right')
##plt.show()

raw_data = {'Model': ['Google', 'N-gram-anchor', 'Hybrid', 'Probabilistic Model'],
        'Random Set': cov1,
        'Set2': cov2}
df = pd.DataFrame(raw_data, columns = ['Model', 'Random Set', 'Set2'])

# Setting the positions and width for the bars
pos = list(range(len(df['Random Set']))) 
width = 0.25 

# Plotting the bars
fig, ax = plt.subplots(figsize=(10,5))

# Create a bar with pre_score data,
# in position pos,
plt.bar(pos, 
        #using df['pre_score'] data,
        df['Random Set'], 
        # of width
        width, 
        # with alpha 0.5
        alpha=0.5, 
        # with color
        color='#EE3124', 
        # with label the first value in first_name
        label=df['Model'][0]) 

# Create a bar with mid_score data,
# in position pos + some width buffer,
plt.bar([p + width for p in pos], 
        #using df['mid_score'] data,
        df['Set2'],
        # of width
        width, 
        # with alpha 0.5
        alpha=0.25, 
        # with color
        color='blue', 
        # with label the second value in first_name
        label=df['Model'][1]) 


# Set the y axis label
ax.set_ylabel('Coverage')

# Set the chart's title
ax.set_title('Suggestion Coverage')

# Set the position of the x ticks
ax.set_xticks([p +1 * width for p in pos])

# Set the labels for the x ticks
ax.set_xticklabels(df['Model'])

# Setting the x-axis and y-axis limits
plt.xlim(min(pos)-width, max(pos)+width*4)
plt.ylim([0, max(df['Random Set'] + df['Set2']-0.5)] )

# Adding the legend and showing the plot
plt.legend(['Random Set', 'Selected Set'], loc='upper right')
plt.show()

file2 = open('score_file_v18.txt', 'r')
file1 = open('score_file_v17.txt', 'r')
error2 = main(file2.read())
error2 = list([x[1] for x in error2])


y = error2
N = len(y)
x = range(N)
width = 1/1.5
plt.bar(x, y, width, color="navajowhite")

plt.xlabel('Error Options')
plt.ylabel('Number of Occurrence')
plt.title('Error Analysis')
ind = np.arange(N)
ax = plt.subplot(111)
ax.set_xticks(ind + width/2.)
ax.set_xticklabels(range(1,8))


plt.show()
fig = plt.gcf()

error1 = main(file1.read())
print(error1)
error1 = list([x[1] for x in error1])
print(error1)


y = error1
N = len(y)
x = range(N)
width = 1/1.5
plt.bar(x, y, width, color="navajowhite")

plt.xlabel('Error Options')
plt.ylabel('Number of Occurrence')
plt.title('Error Analysis')
ind = np.arange(N)
ax = plt.subplot(111)
ax.set_xticks(ind + width/2.)
ax.set_xticklabels(range(1,8))


plt.show()
fig = plt.gcf()

