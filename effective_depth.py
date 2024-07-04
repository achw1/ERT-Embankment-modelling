#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 14:17:26 2023

@author: adrianwhite
"""


from scipy.optimize import fsolve


def effective_depth(a,b,m,n):
    
    def R(z, a, b, m, n):
        
        a2,b2,m2,n2,z2=a**2,b**2,m**2,n**2,z**2
        R_top= (b2-2*b*m+m2+4*z2)**-0.5 + (a2-2*a*n+n2+4*z2)**-0.5 -(a2-2*a*m+m2+4*z2)**-0.5 - (b2-2*b*n+n2+4*z2)**-0.5
        R_bottom=((a-m)**2)**-0.5 - ((b-m)**2)**-0.5 - ((a-n)**2)**-0.5 + ((b-n)**2)**-0.5
        
        return R_top/R_bottom

    def d(z, a, b, m, n):
        
        if z <= 0:
            return 0
        else:   
            return R(z, a, b, m, n) - R(0, a, b, m, n)
    
    max_len = max(a, b, m, n) - min(a, b, m, n)    
    depth=fsolve(lambda z: d(z, a, b, m, n)-0.5, 0.2 * max_len)[0].round(5)
    
    return depth

