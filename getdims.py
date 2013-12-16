# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 11:13:12 2013

@author: amyskerry
"""

import csv

dimfile='/Users/amyskerry/Documents/projects/turk/NDE_dim/appraisals.csv'

def extractdims(datafile):
    with open(datafile, 'rU') as csvfile:
        reader = csv.reader(csvfile)
        dimdata=[]
        for dimnum, row in enumerate(reader):
            if dimnum==0:
                varnames=row
                minindex=row.index('LowEnd')
                midindex=row.index('Middle')
                maxindex=row.index('HighEnd')
                Qindex=row.index('Dquestion')
                qlabelindex=row.index('Dqname')
                qnumindex=row.index('Dnum')
            else:
                dimdata.append(row)
        numdims=len(dimdata)
    return minindex,midindex,maxindex,Qindex,qlabelindex,qnumindex,dimdata,numdims  

[minindex,midindex,maxindex,Qindex,qlabelindex,qnumindex,dimdata,numdims]=extractdims(dimfile)          
                

            
                
                