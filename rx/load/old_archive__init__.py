author = 'Simon Croft, Dan Ellis'
import load
import pandas as pd
import tensorflow as tf
import numpy as np
#pip install tensorflow==2.0.0-beta1

__loc__ = '../'
__pfiles__ = 'Crops.csv|Crops_processed.csv'
__comodities__ = 'Soybeans|Oil, soybean'.split('|')
__year__ = 2016
__unit__ = 'tonnes'

__nit__ = 10000

#what to add to production array
production = [ pd.read_csv(__loc__+i) for i in __pfiles__.split('|')]
production = pd.concat(production)

codes = load.getcats(production)
nelem = max(filter( lambda x: x < 500, codes.area.keys())) # no countries

nitem = len(__comodities__)
ncol = nitem*nelem
#filter year
production = production[production.Year == __year__]
production = production[production.Unit == __unit__][['Area Code','Item','Value']]
production = production[production['Area Code'] <= nelem]

p = []
pid = []

for i,c in enumerate(__comodities__):
    pvals = production[production['Item'] == c]
    pid.extend( pvals['Area Code'].values + (nelem*i) -1 )
    p.extend(pvals.Value)

print ( 'Production sparseness: ', float(len(p))/ncol)
pid = [[i,i] for i in pid]

Pd = tf.SparseTensor(indices=pid,values=p,dense_shape=[ncol,ncol])


## TRADE
trade = pd.read_csv(__loc__+'Detailed_trade_matrix.csv')
trade = trade[trade.Year == __year__]
trade = trade[trade.Unit == __unit__]
trade = trade[trade['Reporter Country Code'] <= nelem]
trade = trade[trade['Partner Country Code'] <= nelem]

#keep = [u'Reporter Country Code', u'Partner Country Code', u'Item Code', u'Item', u'Year', u'Unit', u'Value', u'Flag']
keep = [u'Reporter Country Code',u'Partner Country Code', u'Item','Value', u'Flag']
imports = trade[trade.Element == 'Import Value'][keep]

#keep = [ u'Partner Country Code',u'Reporter Country Code', u'Item Code', u'Item', u'Year', u'Unit', u'Value', u'Flag']

keep = [ u'Partner Country Code',u'Reporter Country Code', u'Item','Value', u'Flag']
exports = trade[trade.Element == 'Export Quantity'][keep]

imports.columns = exports.columns = [ 'target','source','Item','Value','Flag']


trade = pd.concat([imports,exports])

eid = []
e = []
for i,c in enumerate(__comodities__):
    vals = trade[trade['Item'] == c]['source target Value'.split()]
    eid.extend( (vals[['source','target']]+(nelem*i)-1).values)
    e.extend(vals.Value)
print ( 'Trade sparseness: ', float(len(e))/ncol**2 )

E = tf.SparseTensor(indices=eid,values=e,dense_shape=[ncol,ncol])
ncol = tf.Variable(ncol)
