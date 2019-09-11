import tensorflow as tf
#pip install tensorflow==2.0.0-beta1

class reexport:
    '''
    The reexport class
    '''
    def __init__(self, pid,p,eid,e,ncol, N=10000):
        '''
        Inputs:
            pid : production ids in shape of [[x,x],[y1,y1]...] - diagonal
            p   : values of production
            eid : export matrix values [[x,y],[x1,y1],....]
            ncol: total number of COLUMNS
            N   : number of partitions (default 10000)
        '''

        Pd = tf.SparseTensor(indices=pid,values=p,dense_shape=[ncol,ncol])
        E = tf.SparseTensor(indices=eid,values=e,dense_shape=[ncol,ncol])

        self.setup(Pd,E,N)

    def setup(self,Pd,E,N):
        '''
            The re-export alogrithm setup

            Inputs:
            > Pd - Production Diagonal (tf.SparseTensor, tf.float64)
            > E  - Export Matrix (tf.SparseTensor, tf.float64)
            > N  - Optional number of iterations - default = 10000 (int)

            Output:
            <  Domestic Supply Matrix (tf.Tensor)

            Internal Variables:
            ncol - number of columns
            DS   - domestic supply
            tmpX - temporary variables for comparison
            dE   - proportional change in exports

        '''
        ncol = Pd.dense_shape[0]
        DS = tf.zeros(shape = [ncol,ncol],dtype=tf.dtypes.float64)
        N = tf.constant(N,tf.float64)
        Pd = tf.sparse.to_dense(Pd,validate_indices=False)/N
        E = tf.sparse.to_dense(E,validate_indices=False)/N
        Pd = self.zeronan(Pd)

        self.DS = DS
        self.Pd = Pd
        self.E  = E
        self.N = N
        print('N = %d'%N)


    def algorithm(self,DS):
        '''
        For comments see tests folder
        '''
        DS = tf.add(DS,self.Pd)
        ### Step 2 - Trade
        tmp1 = self.zeronan(self.E/tf.reshape(tf.reduce_sum(DS,axis=0),(-1,1)))
        tmp2 = tf.reduce_sum(tmp1,axis = 1)
        # if multiplication factor is greater than one, divide the row by that much
        tmp1 = tmp1 / tf.reshape(tf.where(tmp2>1,tmp2,1),(-1,1))
        ## Proportional Change - Update Domestic Supply
        dE  = tf.linalg.diag( 1 - tf.math.reduce_sum(tmp1, 1) ) + tmp1
        DS = tf.tensordot(DS,dE,axes=1)
        return DS

    def zeronan(self, x):
        return tf.where(tf.math.is_finite(x), x, tf.zeros_like(x))

    def run(self):
        '''
        Use this to run the rexport algorithm for the values in setup
        '''
        # zero DS to avoid mistakes
        DS = self.DS*0
        for _ in range(1,self.N+1):
            DS = self.algorithm(DS)
        self.DS = DS
        self.check()
        return DS

    def check(self):
        check = abs(tf.reduce_sum(self.DS,axis=1) - tf.linalg.diag_part(self.Pd)*self.N)
        print ('')
        import numpy as np
        mean = np.mean(check)
        max  = np.max(check)
        total  = np.sum(check)

        print ('Avg   Difference from production: %.2e \nPassed: %s'%(mean,mean < 1e-5) )
        print ('Max   Difference from production: %.2e \nPassed: %s'%(max,max < 1e-4) )
        print ('Total Difference from production: %.2e \nPassed: %s'%(total,total<1e-3) )



        return check






if __name__ == '__main__':
        print('You are running the class directly, doing sample test. ')

        import numpy as np
        ncol = 3
        #sparse production and exports
        pid = [[0,0],[2,2]]
        p = np.array([1000,500], dtype= np.float64)

        eid = [[0,1],[0,2],[1,0],[1,2]]
        e = np.array([200,300,100,200], dtype = np.float64)

        rxp = reexport(pid,p,eid,e,ncol,1000)

        rxp.run()
