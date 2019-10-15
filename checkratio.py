import rx, re
import numpy as np

 #Area Code,Area,Item Code,Item,Element Code,Element,Year Code,Year,Unit,Value,Flag

cols = '''SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'trade_matrix';'''


itemlist = rx.psql.get('SELECT DISTINCT "Item" FROM comtrade','faostat')

countries = rx.psql.get('SELECT DISTINCT "Area" FROM comtrade','faostat')
years = rx.psql.get('SELECT DISTINCT "Year" FROM comtrade','faostat')


soy = filter(lambda i:re.search(r'soy',i, re.IGNORECASE), itemlist.values.flatten())





def query(item):
    return '''SELECT "Area","Area Code","Year","Item","Value"
    FROM %s
    WHERE "Item" = '%s' AND "Element" = 'Production'
    AND "Unit"='tonnes' AND "Value" > 0 AND "Area Code" < 300
     ;'''%('comtrade',item)

dfs = [rx.psql.get(query(item),'faostat').sort_values(['Area','Year']) for item in soy]
soy_df = dict(zip(soy,dfs))

yd = {}
problem = []
for y in years.values.flatten():
    dummy = []

    m= [df[df.Year == y] for df in dfs]
    for a in countries.values.flatten():

        try:
            vals = [m2[m2.Area == a].Value.values[0] for m2 in m]
            dummy.append([y,a,vals[0]/vals[2], (vals[1]-(vals[0]+vals[2]))/vals[1]])
        except:
            problem.append([a,y])

    yd[y]= dummy
