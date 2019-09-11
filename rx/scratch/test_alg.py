'''A test reexport algorithm to check results agains simon crofts matlab script.'''
import tensorflow as tf
#pip install tensorflow==2.0.0-beta1
######################################
#@tf.function
def rp_sum(tmp, shape,axis = 0):
    '''
    tmp -> data
    shape -> tf shape [row,col]
    axis -> 0 for row based operation, 1 otherwise
    '''
    ##tmp = tf.convert_to_tensor(tmp,shape = shape)
    dummy = tf.reshape(tf.tile(tf.reduce_sum(tmp,axis), [shape[axis]]) , shape)
    if axis: dummy = tf.transpose(dummy)
    return dummy

#@tf.function
def zeronan(x):
    '''
    replace non finite values with 0
    '''
    return tf.where(tf.math.is_finite(x), x, tf.zeros_like(x))

print ('---------------------------------')

@tf.function
def rxp(DS,E,Pd,N=1000):
    debug = {}
    DS = tf.add(DS,Pd)
    ### Step 2 - Trade
    # fraction of export divided by the fraction import (transpose) for timestep.
    #tmp1 = zeronan( E / tf.transpose(rp_sum(DS,E.shape)) )
    tmp1 = zeronan(E/tf.reshape(tf.reduce_sum(DS,axis=0),(-1,1)))
    #find row normalisation factors
    tmp2 = tf.reduce_sum(tmp1,axis = 1)
    # if multiplication factor is greater than one, divide the row by that much
    debug['overexport'] = tmp2>1
    tmp1 = tmp1 / tf.reshape(tf.where(tmp2>1,tmp2,1),(-1,1))
    ## Proportional Change - Update Domestic Supply
    dE  = tf.linalg.diag( 1 - tf.math.reduce_sum(tmp1, 1) ) + tmp1
    DS = tf.tensordot(DS,dE,axes=1)


    return DS,debug

def setup(Pd,E,N):
    '''
        The re-export alogrithm

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

    print('Running with %d itterations'%N)

    ncol = Pd.dense_shape[0]
    DS = tf.zeros(shape = [ncol,ncol],dtype=tf.dtypes.float64)
    N = tf.constant(N,tf.float64)
    Pd = tf.sparse.to_dense(Pd,validate_indices=False)/N
    E = tf.sparse.to_dense(E,validate_indices=False)/N

    Pd = zeronan(Pd)#for some reason there are nans... replace these (filter out at load)


    return DS,E,Pd
    #for _ in tf.range(1,N):


#@tf.function
def rxpt(Pd, E, N = 10000):

    DS,E,Pd = setup(Pd,E,N)
    overexport = []
    for _ in range(1,N+1):
        DS,debug = rxp(DS,E,Pd)
        overexport.append(debug['overexport'])

    print DS


    check = sum( tf.reduce_sum(DS,axis=1) - tf.linalg.diag_part(Pd)*N )

    print (tf.reduce_sum(DS,axis=1))
    print ('')
    print ('Difference from production: %.2e \nPassed: %s'%(check,np.array(check<1e-8)) )




if __name__ == '__main__':
    #data
    import numpy as np
    ncol = 3
    #sparse production and exports
    pid = [[0,0],[2,2]]
    p = np.array([1000,500], dtype= np.float64)

    eid = [[0,1],[0,2],[1,0],[1,2]]
    e = np.array([200,300,100,200], dtype = np.float64)


    Pd = tf.SparseTensor(indices=pid,values=p,dense_shape=[ncol,ncol])
    E = tf.SparseTensor(indices=eid,values=e,dense_shape=[ncol,ncol])
    ncol = tf.Variable(ncol)

    print (tf.sparse.to_dense(Pd)
    ,tf.sparse.to_dense(E)
    )

    print ('---------------------------------')

    rxpt(Pd,E)

'''
array([[721.48846,   0.     , 278.50928],
       [  0.     ,   0.     ,   0.     ],
       [  0.     ,   0.     , 500.     ]], dtype=float64)>)
'''
print ('fi')
