# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 20:09:56 2016

@author: XZ01M2
"""
import numpy as np

A = np.zeros((3,3))
B = np.zeros((3,2))
p = np.zeros((3,))
a = np.zeros((3,1))
w = np.zeros((3,1))
A[0,:] = [0.25, 0.75, 0]
A[1,:] = [0, 0.25, 0.75]
A[2,:] = [0, 0, 1]

B[0,:] = [ 1, 0 ]
B[1,:] = [ 0, 1 ]
B[2,:] = [1,0 ]

p[0] =  1
p[1] =  1
p[2] =  1

#test = B[:,0]
#print( test.shape)
#test2 = test.T
#print( test2.shape)

emissProb =  B[:,0]  

print((emissProb*p)@A)



print("hello")
