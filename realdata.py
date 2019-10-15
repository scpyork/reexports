import rx
import numpy as np
year = 2013
item = 'Soybeans'

save = './output/'

E,P,cid = rx.psql.get_trade(year,item)

def save_inputs():
    global E, P , cid,save

    P.to_csv(save+'%s_%s_P.csv'%(item,year))
    E.to_csv(save+'%s_%s_E.csv'%(item,year))
    import pandas as pd
    pd.Series(cid).to_csv(save+'%s_%s_Cid.csv'%(item,year))
    print('saving inputs')

save_inputs()

def refactor (E,P, N=10000):

    #only take those which have exports / imports for Production
    pid = [[i,i] for i in P['Area Code'] if i in cid.keys()]
    p = P.Value.values

    eid = E[['source','target']].values
    e = E.Value.values

    ncol = eid.max() + 1
    return pid,p,eid,e,ncol,N


rxp = rx.reexport(*refactor(E,P))

rxp.run()

def save_DS():
    import pandas as pd
    global rxp,cid, year, item , P


    data = np.array(rxp.DS)

    countries = []
    rdict = cid

    for i in range(data.shape[0]):
        try: countries.append(rdict[i])
        except Exception as e:
            print e
            countries.append(i)

    df = pd.DataFrame(data, columns = countries,index = countries)
    df.to_csv(save+'%s_%s_reexport.csv'%(item,year))
    df.sum().to_csv(save+'%s_%s_reexpprodsum.csv'%(item,year))

    return df

df = save_DS()
