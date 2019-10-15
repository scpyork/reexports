'''
http://www.fao.org/waicent/faostat/agricult/cb-f.htm

'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('data/Crops_Primary_Equivalent.csv')
df = df[df['Area Code']<270]
DS = df[df.Element == 'Domestic supply quantity']

DS = DS[[u'Area Code', u'Area', u'Item Code', u'Item', u'Year', u'Unit', u'Value', u'Flag']]

SV = df[df.Element == 'Production']

soycat =  ['Soyabean Cake','Soyabean Oil','Soyabeans']


areas = set(DS.Area)
years = set(DS.Year)


shell = pd.DataFrame(np.zeros((len(areas)*len(years),DS.shape[1])),columns = DS.columns)

shell = pd.DataFrame()
shell['Area'] = np.tile(list(areas),len(years))
shell['Year'] = np.tile(list(years),len(areas))



soy = [
shell.merge(DS[DS.Item == i], on=['Area','Year'],how='outer')
for i in soycat
]

svm = [
shell.merge(SV[SV.Item == i], on=['Area','Year'],how='outer')
for i in soycat
]


s= pd.concat(svm)

mysoy = s[s.Item.apply(lambda x: x in soycat)]

#mysoy.groupby(by=['Year','Item']).mean().Value.plot()


pdf = pd.concat([mysoy[mysoy.Item==c].groupby(by='Year').mean()['Value'] for  c in soycat],axis = 1 )


from sklearn import preprocessing


pdf = pd.DataFrame(preprocessing.normalize(pdf.T).T,index=pdf.index)


pdf.columns = soycat
#pdf = pdf.divide(pdf.sum(axis=1),axis=0)


#pdf.plot(kind = 'area')
#plt.show()
#shell = pd. DataFrame([[a,y] for a in areas for y in years],columns=['Area Code','Year'])

year = 2013

rt = SV[SV.Year == 2013]

rtg = [rt[rt.Item == i ].set_index('Area Code').Value  for i in soycat]
rtg = [rt[rt.Item == i ].set_index('Area').Value  for i in soycat]

ratio = rtg[0].divide(rtg[1],axis=0)






print 'fi'




myds = DS[DS.Year==2013]
myds = myds[myds.Item=='Soyabeans']


'''

In [38]: plt.scatter(range(len(rxp.DS)),np.log10(np.sum(rxp.DS,axis=1).astype('f
    ...: loat')),s=10)
/home/dp626/anaconda2/bin/ipython:1: RuntimeWarning: divide by zero encountered in log10
  #!/home/dp626/anaconda2/bin/python
Out[38]: <matplotlib.collections.PathCollection at 0x7f809406f9d0>

In [39]: plt.scatter(myds['Area Code'],np.log10(myds.Value),s=10)
/home/dp626/anaconda2/bin/ipython:1: RuntimeWarning: divide by zero encountered in log10
  #!/home/dp626/anaconda2/bin/python
Out[39]: <matplotlib.collections.PathCollection at 0x7f809407e310>

In [40]: plt.legend()
Out[40]: <matplotlib.legend.Legend at 0x7f809c01cf90>

In [41]: plt.show()
'''
