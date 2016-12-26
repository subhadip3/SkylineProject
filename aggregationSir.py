import sys
import time
import math
import numpy as np
import itertools

#from test import hello
from functools import reduce



def check_membership(list1,list2):
    flag=1
    i=0
    boundary_count=0
    while i<len(list1):
        limits=list2[i]
        if(list1[i]<limits[0] or list1[i]>limits[1]):
            return 0
        if(list1[i]==limits[0] or list1[i]==limits[1]):
            boundary_count=boundary_count+1
        i=i+1
    if boundary_count==len(list1):
        return 0
    return 1
     
         




        
def my_func(s,Rectangle,q,records_modified,myself,comp_count,k):
 
    	 
    d=len(s)
    n=len(s[0])
    '''for i in range(d):
      for j in range(n):
        print s[i][j].ide,
      print("\n")   
    '''
    count=np.zeros(n+1)
    for i in range(d):
    
        for j in range(n):
             comp_count[0]=comp_count[0]+1;
	     if(records_modified[s[i][j].ide][1:]==myself):
                continue;
	     comp_count[0]=comp_count[0]+1;
	     if(records_modified[s[i][j].ide][i+1]<Rectangle[i][0] or records_modified[s[i][j].ide][i+1]>Rectangle[i][1]):
	        break;
             count[s[i][j].ide]=count[s[i][j].ide]+1;
	     comp_count[0]=comp_count[0]+1;
	     if(count[s[i][j].ide]==k or count[s[i][j].ide]==d):
		return 0;
    return 1;
		





    
