# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 22:34:30 2016

@author: XZ01M2
"""

from simpsons_paradox_data import *

female_and_A_only = joint_prob_table[gender_mapping['female'], department_mapping['A']]
admitted_given_female_A = female_and_A_only/np.sum(female_and_A_only)
print("admitted_given_female_A")
print(admitted_given_female_A)

male_and_A_only = joint_prob_table[gender_mapping['male'], department_mapping['A']]
admitted_given_male_A = male_and_A_only/np.sum(male_and_A_only)
print("admitted_given_male_A")
print(admitted_given_male_A)

female_and_B_only = joint_prob_table[gender_mapping['female'], department_mapping['B']]
admitted_given_female_B = female_and_B_only/np.sum(female_and_B_only)
print("admitted_given_female_B")
print(admitted_given_female_B)

male_and_B_only = joint_prob_table[gender_mapping['male'], department_mapping['B']]
admitted_given_male_B = male_and_B_only/np.sum(male_and_B_only)
print("admitted_given_male_B")
print(admitted_given_male_B)

female_and_C_only = joint_prob_table[gender_mapping['female'], department_mapping['C']]
admitted_given_female_C = female_and_C_only/np.sum(female_and_C_only)
print("admitted_given_female_C")
print(admitted_given_female_C)

male_and_C_only = joint_prob_table[gender_mapping['male'], department_mapping['C']]
admitted_given_male_C = male_and_C_only/np.sum(male_and_C_only)
print("admitted_given_male_C")
print(admitted_given_male_C)

female_and_D_only = joint_prob_table[gender_mapping['female'], department_mapping['D']]
admitted_given_female_D = female_and_D_only/np.sum(female_and_D_only)
print("admitted_given_female_D")
print(admitted_given_female_D)

male_and_D_only = joint_prob_table[gender_mapping['male'], department_mapping['D']]
admitted_given_male_D = male_and_D_only/np.sum(male_and_D_only)
print("admitted_given_male_D")
print(admitted_given_male_D)

female_and_E_only = joint_prob_table[gender_mapping['female'], department_mapping['E']]
admitted_given_female_E = female_and_E_only/np.sum(female_and_E_only)
print("admitted_given_female_E")
print(admitted_given_female_E)

male_and_E_only = joint_prob_table[gender_mapping['male'], department_mapping['E']]
admitted_given_male_E = male_and_E_only/np.sum(male_and_E_only)
print("admitted_given_male_E")
print(admitted_given_male_E)

female_and_F_only = joint_prob_table[gender_mapping['female'], department_mapping['F']]
admitted_given_female_F = female_and_F_only/np.sum(female_and_F_only)
print("admitted_given_female_F")
print(admitted_given_female_F)

male_and_F_only = joint_prob_table[gender_mapping['male'], department_mapping['F']]
admitted_given_male_F = male_and_F_only/np.sum(male_and_F_only)
print("admitted_given_male_F")
print(admitted_given_male_F)