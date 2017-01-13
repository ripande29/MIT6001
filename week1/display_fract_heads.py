# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 22:27:38 2016

@author: XZ01M2
"""

import comp_prob_inference
import matplotlib.pyplot as plt
n = 100000
heads_so_far = 0
fraction_of_heads = []
for i in range(n):
    if comp_prob_inference.flip_fair_coin() == 'heads':
        heads_so_far += 1
    fraction_of_heads.append(heads_so_far / (i+1))
    
plt.figure(figsize=(8, 4))
plt.plot(range(1, n+1), fraction_of_heads)
plt.xlabel('Number of flips')
plt.ylabel('Fraction of heads')
