import rx
import numpy as np

E,P,cid = rx.psql.get(2014,'Soybeans')


def refactor (E,P, N=10000):
    pid = [[i,i] for i in P['Area Code']]
    p = P.Value.values

    eid = E[['source','target']].values
    e = E.Value.values

    ncol = eid.max() + 1
    return pid,p,eid,e,ncol,N


rxp = rx.reexport(*refactor(E,P))

rxp.run()
