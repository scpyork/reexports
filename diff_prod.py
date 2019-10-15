import pandas as pd
import numpy as np

cb = pd.read_csv('data/Crops_Primary_Equivalent.csv')

p = pd.read_csv('data/Production/Crops.csv')

cb = cb[cb.Year==2013]
p = p[p.Year==2013]

cb= cb[cb.Item=='Soyabeans']
p= p[p.Item== 'Soybeans']


cb= cb[cb.Unit=='tonnes']
p= p[p.Unit== 'tonnes']


cb= cb[cb.Element=='Production']
p= p[p.Element== 'Production']

cb= cb[cb['Area Code']<270]
p= p[p['Area Code']<270]


print 'length c, p',len(set(cb['Area Code'])),len(set(p['Area Code']))

cdif = set(cb['Area Code']) ^ set(p['Area Code'])
elemdiff = p[[i in cdif for i in p['Area Code']]]
print cdif,'different', elemdiff

allc = set(cb['Area Code']) | set(p['Area Code'])
template = pd.DataFrame(np.zeros(len(allc)),index = list(allc),columns= ['Value'])

cb = cb.set_index('Area Code')
p = p.set_index('Area Code')

cb1 = cb['Area Value'.split()]
cb2 = pd.DataFrame(template['Value']+cb1['Value'])
cb2['Area']= cb1.loc[template.index].Area.values

p1 = p['Area Value'.split()]
p2 = pd.DataFrame(template['Value']+p1['Value'])
p2['Area']= p1.loc[template.index].Area.values


nonnan = p[p.Flag >0]


vdiff = pd.DataFrame(p2.Value-cb2.Value,columns = ['Value']).dropna()
vdiff['Area'] = p2['Area']
vdiff = vdiff[vdiff.Value!=0]
vdiff['pflag'] = p.loc[vdiff.index].Flag.values
vdiff['cflag'] = cb.loc[vdiff.index].Flag.values
#-ve cb is smaller
print vdiff

dvdiff = pd.DataFrame(p2.Value/cb2.Value,columns = ['Value']).dropna()
dvdiff['Area'] = p2['Area']
dvdiff = dvdiff[dvdiff.Value!=1]
dvdiff['pflag'] = p.loc[dvdiff.index].Flag.values
dvdiff['cflag'] = cb.loc[dvdiff.index].Flag.values
#-ve cb is smaller
print dvdiff

print 'fi'
