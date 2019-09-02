'''A test reexport algorithm to check results agains simon crofts matlab script.'''
import tensorflow as tf
import numpy as np
#pip install tensorflow==2.0.0-beta1

print ('---------------Extra Functions------------------')
""
@tf.function
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
DS = tf.zeros(shape = [ncol,ncol],dtype=tf.dtypes.float64, name = 'Demand_Matrix')
N = tf.constant(N,tf.float64)
Pd = tf.sparse.to_dense(Pd,validate_indices=False,name = 'Production_Diagonal')/N
E = tf.sparse.to_dense(E,validate_indices=False, name = 'Trade_Matrix')/N



@tf.function
def rxp(DS,Pd,E):

    #with tf.name_scope("DS") as scope:
        with tf.name_scope('1-Allocate_Production'):
            DS = tf.add(DS,Pd, name = 'Add_Fraction')
        ### Step 2 - Trade
        # fraction of export divided by the fraction import (transpose) for timestep. #tmp1 = zeronan( E / tf.transpose(rp_sum(DS,E.shape)) )
        with tf.name_scope('2-Perform-Trade'):
            tmp1 = zeronan(E/tf.reshape(tf.reduce_sum(DS,axis=0),(-1,1),name = 'Step_1'))

            with tf.name_scope('Fix-over-exports'):
                #find row normalisation factors
                tmp2 = tf.reduce_sum(tmp1,axis = 1, name = 'normalisation')
                # if multiplication factor is greater than one, divide the row by that much
                tmp2 = tf.reshape(tf.where(tmp2>1,tmp2,1),(-1,1),name='where')

            tmp1 = tf.divide(tmp1,tmp2, name= 'normalise')
        ## Proportional Change - Update Domestic Supply
        with tf.name_scope('3-Update_Domestic_supply'):
            with tf.name_scope('Prduction_Percent'):
                dE  = tf.linalg.diag( 1 - tf.math.reduce_sum(tmp1, 1))
            dE=dE +tmp1
            DS = tf.tensordot(DS,dE,axes=1,name = 'dot_dE-DS')

        return DS







print ('---------------Check------------------')

check = sum( tf.reduce_sum(DS,axis=1) - tf.linalg.diag_part(Pd)*N )

print (tf.reduce_sum(DS,axis=1))
print ('')
print ('Difference from production: %.2e \nPassed: %s'%(check,np.array(check<1e-8)) )

print ('---------------fi------------------')

import os,shutil

logdir = './logs/'
shutil.rmtree(logdir)

writer = tf.summary.create_file_writer(logdir)

# Bracket the function call with
# tf.summary.trace_on() and tf.summary.trace_export().
tf.summary.trace_on(graph=True, profiler=True)
# Call only one tf.function when tracing.
z = rxp(DS,Pd,E)


#foo_to_g = tf.autograph.to_graph(tf.function(rxp))
#foo_to_g(DS,Pd,E)

tfrxp = tf.function(rxp)
for i in range(10):
        DS = rxp(DS,Pd,E)



with writer.as_default():
  tf.summary.trace_export(
      name="rxp_trace",
      step=1,
      profiler_outdir=logdir)


os.system('tensorboard --logdir %s'%logdir)
