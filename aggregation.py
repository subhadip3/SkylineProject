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
     
         




        
def my_func(s,Rectangle,q,records_modified,myself,comp_count):
 
    	 
    d=len(s)
    n=len(s[0])
    '''for i in range(d):
      for j in range(n):
        print s[i][j].ide,
      print("\n")   
    '''
    c=np.zeros(n+1)
    fflag=0;
    flag=0;
    min1=1000000;
    for j in range(d):
       if(abs(Rectangle[j][1]-Rectangle[j][0])<min1):
	min1=abs(Rectangle[j][1]-Rectangle[j][0])
	minj=j;
    for i in range(n):
    
        #for j in range(d):
              if(records_modified[s[minj][i].ide][minj+1]<Rectangle[minj][0] or records_modified[s[minj][i].ide][minj+1]>Rectangle[minj][1]):
	          #print(records_modified[s[j][i].ide])
		  fflag=1;
                  storei=i
		  storej=j	 
	          break;
              #extra check
	      c[s[minj][i].ide]=c[s[minj][i].ide]+1 # c is a map mapping vector id to count
              if(c[s[minj][i].ide]==d):# all dimensions of 1 vector examined
                 comp_count[0]=comp_count[0]+1;
                 if(records_modified[s[minj][i].ide][1:]==myself):
                   continue;
		 if(check_membership(records_modified[s[minj][i].ide][1:],Rectangle)==1):     # element under consideration is not reverse skyline point
	             flag=1
                     break; 
        
    


       
    if(fflag==1):
        newflag=0;
        for i in range(storei+1):
	     if(records_modified[s[minj][i].ide][1:]==myself):
                 continue; 
             if(check_membership(records_modified[s[storej][i].ide][1:],Rectangle)==1):
	         #print(records_modified[s[storej][i].ide][1:])
                 newflag=1;
                 return 0;
        if(newflag==0):
           return 1; 
     

    if(flag==0):
       #print("H U R R A Y");
       return 1;
    else: 
      return 0;













  
    '''c=np.zeros(n+1)
    flag=0;
    
    for i in range(n):
    
        for j in range(d):
               
           c[s[j][i].ide]=c[s[j][i].ide]+1 # c is a map mapping vector id to count
           if(c[s[j][i].ide]==d):# all dimensions of 1 vector examined
              comp_count[0]=comp_count[0]+1;
              if(records_modified[s[j][i].ide][1:]==myself):
                 continue; 
	      print("Records modified:")
	      print(s[j][i].ide+1)
              print(records_modified[s[j][i].ide])
	      print("Rectangle inside")
	      print(Rectangle)
              	
              if(check_membership(records_modified[s[j][i].ide][1:],Rectangle)==1):     # element under consideration is not reverse skyline point
	          flag=1
                  break;  
              
           
        
        if(flag==1):
         break;
    if(flag==0):
      #print("H U R R A Y");
      return 1;
    else: 
      return 0;
        
    '''
