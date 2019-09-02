Sample output of the `test_alg.py` file comparing it to both the matlab code and its own results.

```
In [143]: run tests/test_alg.py
---------------Extra Functions------------------
<function zeronan at 0x7fc9084e7668>
---------------Define Inputs------------------
(<tf.Tensor: id=2244726, shape=(3, 3), dtype=float64, numpy=
array([[1000.,    0.,    0.],
       [   0.,    0.,    0.],
       [   0.,    0.,  500.]])>, <tf.Tensor: id=2244728, shape=(3, 3), dtype=float64, numpy=
array([[  0., 200., 300.],
       [100.,   0., 200.],
       [  0.,   0.,   0.]])>)
---------------Prepare Inputs------------------
(2500, <tf.Tensor: id=2339751, shape=(3, 3), dtype=float64, numpy=
array([[1.4166e+02, 2.0000e-02, 1.0832e+02],
       [0.0000e+00, 0.0000e+00, 0.0000e+00],
       [0.0000e+00, 0.0000e+00, 1.2500e+02]])>)
(5000, <tf.Tensor: id=2434752, shape=(3, 3), dtype=float64, numpy=
array([[2.83326667e+02, 2.00000000e-02, 2.16653333e+02],
       [0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
       [0.00000000e+00, 0.00000000e+00, 2.50000000e+02]])>)
(7500, <tf.Tensor: id=2529753, shape=(3, 3), dtype=float64, numpy=
array([[4.24993333e+02, 2.00000000e-02, 3.24986667e+02],
       [0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
       [0.00000000e+00, 0.00000000e+00, 3.75000000e+02]])>)
(10000, <tf.Tensor: id=2624754, shape=(3, 3), dtype=float64, numpy=
array([[5.6666e+02, 2.0000e-02, 4.3332e+02],
       [0.0000e+00, 0.0000e+00, 0.0000e+00],
       [0.0000e+00, 0.0000e+00, 5.0000e+02]])>)
---------------Check------------------
tf.Tensor([1000.    0.  500.], shape=(3,), dtype=float64)

Difference from production: 1.62e-10
Passed: True
---------------fi------------------
```
