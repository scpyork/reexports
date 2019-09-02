'''A test reexport algorithm to check results agains simon crofts matlab script.'''
import tensorflow as tf
import numpy as np
#pip install tensorflow==2.0.0-beta1

print ('---------------Extra Functions------------------')

def zeronan(x):
    '''replace non finite values with 0'''
    return tf.where(tf.math.is_finite(x), x, tf.zeros_like(x))

print(zeronan)

print ('---------------Define Inputs------------------')
N = 10000


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



print ('---------------Prepare Inputs------------------')


ncol = Pd.dense_shape[0]
DS = tf.zeros(shape = [ncol,ncol],dtype=tf.dtypes.float64)
N = tf.constant(N,tf.float64)
Pd = tf.sparse.to_dense(Pd,validate_indices=False)/N
E = tf.sparse.to_dense(E,validate_indices=False)/N



for _ in range(1,N+1):

    DS = tf.add(DS,Pd)
    ### Step 2 - Trade
    # fraction of export divided by the fraction import (transpose) for timestep. #tmp1 = zeronan( E / tf.transpose(rp_sum(DS,E.shape)) )
    tmp1 = zeronan(E/tf.reshape(tf.reduce_sum(DS,axis=0),(-1,1)))
    #find row normalisation factors
    tmp2 = tf.reduce_sum(tmp1,axis = 1)
    # if multiplication factor is greater than one, divide the row by that much
    tmp1 = tmp1 / tf.reshape(tf.where(tmp2>1,tmp2,1),(-1,1))
    ## Proportional Change - Update Domestic Supply
    dE  = tf.linalg.diag( 1 - tf.math.reduce_sum(tmp1, 1) ) + tmp1
    DS = tf.tensordot(DS,dE,axes=1)

    if (int(_%int(N/4)) == 0) :
        #print(e_n)
        print(_,DS)


print ('---------------Check------------------')

check = sum( tf.reduce_sum(DS,axis=1) - tf.linalg.diag_part(Pd)*N )

print (tf.reduce_sum(DS,axis=1))
print ('')
print ('Difference from production: %.2e \nPassed: %s'%(check,np.array(check<1e-8)) )

print ('---------------fi------------------')













'''
Historic repmat function if you wish to reproduce the same style as matlab code.


def rp_sum(tmp, shape,axis = 0):
    \'''
    tmp -> data
    shape -> tf shape [row,col]
    axis -> 0 for row based operation, 1 otherwise
    \'''
    dummy = tf.reshape(tf.tile(tf.reduce_sum(tmp,axis), [shape[axis]]) , shape)
    if axis: dummy = tf.transpose(dummy)
    return dummy

'''
