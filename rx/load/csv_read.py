def get_trade(year,item,location):
    import pandas as pd

    df = pd.read_csv(location)
    df = df[ df.Year == int(year) ]
    df = df[ df.Item == item ]
    df = df[ df['Area Code']<270 ]


    P = df [df.Element == 'Production']

    return P

def get_percent(year,item1,item2,location):
    import pandas as pd

    df = pd.read_csv(location)
    df = df[ df.Year == int(year) ]
    df = df[ df['Area Code']<270 ]
    df = df [df.Element == 'Production']
    i1 = df[ df.Item == item1 ].set_index('Area Code')
    i2 = df[ df.Item == item2 ].set_index('Area Code')

    sm = i1.Value+i2.Value




    return i1.Value/sm,i2.Value/sm





r = get_trade(2013,'Soyabeans','data/Crops_Primary_Equivalent.csv')
print r.head()
w = get_percent(2013, 'Soyabean Cake','Soyabean Oil','data/Crops_Primary_Equivalent.csv')
print w.head()


if 0:

    imports = trade[trade.Element == 'Import Quantity']
    exports = trade[trade.Element == 'Export Quantity']

    imports.columns = '~'.join(imports.columns).replace('Reporter Country Code','target').replace('Partner Country Code','source').split('~')

    exports.columns = '~'.join(exports.columns).replace('Reporter Country Code','source').replace('Partner Country Code','target').split('~')

    D = pd.concat([imports,exports],axis = 0, sort = True)



    print ('Data Loaded \n\n\n')
    conn = None
    return D,P, cid.set_index('id').to_dict()['name']
