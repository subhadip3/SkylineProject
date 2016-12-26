import numpy as np
import sys
import time
import math
import itertools
from functools import reduce
from aggregationSir import my_func
#from r_treeBBS import *
#execfile("aggregation.py") 
maximum_size=3
minimum_size=2
global root
global heap
global number_of_comparisons
global reverse_skyline
global global_skyline
global k_reverse_skyline

root=[]
skyline=[]
heap=[]


#Leaf node for r-tree
#contains parent and record(which is a list of the form (id,data,mindist)

class leaf_node:
    __slots__ = ["parent", "record"]
    def append_record(self,element):
        self.record.append(element)
    def add_parent(self,parent):
        self.parent=parent


#non leaf node for r-tree
#contains parent and(which is a list of the form (child,mbr,mindist) where mbr is of the form [(min vertex,max vertex)]
class non_leaf_node:
    __slots__ = ["parent","record"]
    def append_record(self,element):
        self.record.append(element)
    def add_parent(self,parent):
        self.parent=parent


# Takes data of the form [id,data] and inserts it into the r-tree

def rtree_insert(temp):
    global root
    if(root==[]):
        node=leaf_node()
        node.record=[]
        temp_tuple=(temp[0],temp[1:])
        node.record.append(temp_tuple)
        root=node
        root.parent=[]
    else:
        chosen_leaf=chooseleaf(root,temp)
        temp_tuple=(temp[0],temp[1:])
        chosen_leaf.record.append(temp_tuple)
        if (len(chosen_leaf.record)<=maximum_size):
            if chosen_leaf==root:
                return
            else:
                chosen_leaf_parent=chosen_leaf.parent
                chosen_leaf_parent_record=chosen_leaf_parent.record
                i=0
                while i < len(chosen_leaf_parent_record):
                    element=chosen_leaf_parent_record[i]
                    if(element[0]==chosen_leaf):
                        break
                    i=i+1
                temp_list=list(chosen_leaf_parent.record[i])
                temp_list[1]=find_mbr_node_leaf(chosen_leaf)
                chosen_leaf_parent.record[i]=tuple(temp_list)

                chosen_node=chosen_leaf_parent

                while(chosen_node!=root):
                    chosen_node_parent=chosen_node.parent
                    chosen_node_parent_record=chosen_node_parent.record
                    i=0
                    while i < len(chosen_leaf_parent_record):
                        element=chosen_node_parent_record[i]
                        if(element[0]==chosen_node):
                            break
                        i=i+1

                    temp_tuple_list=list(chosen_node_parent_record[i])
                    temp_tuple_list[1]=find_mbr_node_non_leaf(chosen_node)
                    chosen_node_parent_record[i]=tuple(temp_tuple_list)

                    chosen_node=chosen_node_parent
        elif (len(chosen_leaf.record)>maximum_size):
            (temp1,temp2)=split_node(chosen_leaf.record)
            leaf_node_1=leaf_node()
            leaf_node_1.record=temp1
            leaf_node_2=leaf_node()
            leaf_node_2.record=temp2
            if(chosen_leaf==root):

                root=non_leaf_node()
                element=[]
                element.append((leaf_node_1,find_mbr_node_leaf(leaf_node_1)))
                element.append((leaf_node_2,find_mbr_node_leaf(leaf_node_2)))
                leaf_node_1.parent=root
                leaf_node_2.parent=root
                root.record=element
                root.parent=[]
            else:
                chosen_leaf_parent=chosen_leaf.parent
                leaf_node_1.parent=chosen_leaf_parent
                leaf_node_2.parent=chosen_leaf_parent
                chosen_leaf_parent_record=chosen_leaf_parent.record
                i=0
                while i < len(chosen_leaf_parent_record):
                    element=chosen_leaf_parent_record[i]
                    if(element[0]==chosen_leaf):
                        break
                    i=i+1
                del chosen_leaf_parent_record[i]
                chosen_leaf_parent_record.append((leaf_node_1,find_mbr_node_leaf(leaf_node_1)))
                chosen_leaf_parent_record.append((leaf_node_2,find_mbr_node_leaf(leaf_node_2)))
                chosen_leaf_parent.record=chosen_leaf_parent_record
                chosen_node=chosen_leaf_parent
                while(len(chosen_node.record)>maximum_size):
                    chosen_node_parent=chosen_node.parent
                    (temp1,temp2)=split_node_non_leaf(chosen_node.record)
                    node_1=non_leaf_node()
                    node_1.parent=chosen_node_parent
                    node_1.record=temp1
                    node_2=non_leaf_node()
                    node_2.parent=chosen_node_parent
                    node_2.record=temp2
                    for node_element in node_1.record:
                        node_element_child=node_element[0]
                        node_element_child.parent=node_1
                    for node_element in node_2.record:
                        node_element_child=node_element[0]
                        node_element_child.parent=node_2


                    if chosen_node==root:
                        root=non_leaf_node()
                        element=[]
                        element.append((node_1,find_mbr_node_non_leaf(node_1)))
                        element.append((node_2,find_mbr_node_non_leaf(node_2)))
                        node_1.parent=root
                        node_2.parent=root
                        root.parent=[]
                        root.record=element
                        chosen_node=root
                        break
                    else:
                        chosen_node_parent_record=chosen_node_parent.record
                        i=0
                        while i < len(chosen_node_parent_record):
                            element=chosen_node_parent_record[i]
                            if(element[0]==chosen_node):
                                break
                            i=i+1
                        del chosen_node_parent_record[i]
                        chosen_node_parent_record.append((node_1,find_mbr_node_non_leaf(node_1)))
                        chosen_node_parent_record.append((node_2,find_mbr_node_non_leaf(node_2)))
                        chosen_node=chosen_node_parent
                while(chosen_node!=root):
                    chosen_node_parent=chosen_node.parent
                    chosen_node_parent_record=chosen_node_parent.record
                    i=0
                    while i < len(chosen_leaf_parent_record):
                        element=chosen_node_parent_record[i]
                        if(element[0]==chosen_node):
                            break
                        i=i+1
                    temp_tuple_1=list(chosen_node_parent_record[i])
                    temp_tuple_1[1]=find_mbr_node_non_leaf(chosen_node)
                    chosen_node_parent_record[i]=tuple(temp_tuple_1)
                    chosen_node=chosen_node_parent


def split_node_non_leaf(record_temp):
    record=list(record_temp)
    (temp1,temp2)=pickseeds_non_leaf(record)
    record.remove(temp1)
    record.remove(temp2)
    split_record_1=[]
    split_record_2=[]
    split_record_1.append(temp1)
    split_record_2.append(temp2)

    if len(record)==(minimum_size-1):
        record.append(temp1)
        split_record_1=record
    else:
        while len(record)!=0:
            return_record=picknext_non_leaf(record,split_record_1,split_record_2)
            record.remove(return_record)
            old_area_1=calculate_area_non_leaf_node(split_record_1)
            old_area_2=calculate_area_non_leaf_node(split_record_2)
            split_record_1.append(return_record)
            split_record_2.append(return_record)
            if calculate_area_non_leaf_node(split_record_1)< calculate_area_non_leaf_node(split_record_2):
                split_record_2.remove(return_record)
            elif calculate_area_non_leaf_node(split_record_1)>calculate_area_non_leaf_node(split_record_2):
                split_record_1.remove(return_record)
            elif old_area_1>old_area_2:
                split_record_1.remove(return_record)
            elif old_area_1<old_area_2:
                split_record_2.remove(return_record)
            elif len(split_record_1) < len(split_record_2):
                split_record_2.remove(return_record)
            else:
                split_record_1.remove(return_record)
            if (len(record)+len(split_record_1) == minimum_size) and len(record)!=0:
                split_record_1=split_record_1 + record
                break
            elif (len(record)+len(split_record_2) == minimum_size) and len(record)!=0:
                split_record_2=split_record_2 + record
                break
    return (split_record_1,split_record_2)



# takes a record and two other records and return a member of record

def picknext_non_leaf(record,rectangle_1,rectangle_2):
    difference=0
    return_record=record[0]
    record_rectangle_1_area=calculate_area_non_leaf_node(rectangle_1)
    record_rectangle_2_area=calculate_area_non_leaf_node(rectangle_2)
    for record_entry in record:
        rectangle_1.append(record_entry)
        d1=calculate_area_non_leaf_node(rectangle_1)-record_rectangle_1_area
        rectangle_2.append(record_entry)
        d2=calculate_area_non_leaf_node(rectangle_2)-record_rectangle_2_area
        rectangle_1.remove(record_entry)
        rectangle_2.remove(record_entry)
        if abs(d1-d2)>difference:
            difference=abs(d1-d2)
            return_record=record_entry
    return return_record


def calculate_area_non_leaf_node(record):
    if len(record)==1:
        temp=[]
        data_record=record[0]
        mbr_needed=list(data_record[1])
        for temp_tuple in mbr_needed:
            temp.append(temp_tuple[1]-temp_tuple[0])
        temp_area=reduce(lambda x,y: x*y,temp,1)
        return temp_area
    else:
        first_record=list(record[0])
        mbr_needed=first_record[1]
        min_mbr_values=[]
        max_mbr_values=[]
        for temp_tuple in mbr_needed:
            min_mbr_values.append(temp_tuple[0])
            max_mbr_values.append(temp_tuple[1])
    for single_element in record:
        mbr_needed=single_element[1]
        i=0
        while i<len(mbr_needed):
            temp_tuple=mbr_needed[i]
            if temp_tuple[0]<=min_mbr_values[i]:
               min_mbr_values[i]=temp_tuple[0]
            if temp_tuple[1]>=max_mbr_values[i]:
               max_mbr_values[i]=temp_tuple[1]
            i=i+1
    temp=map(lambda x,y:abs(x-y), min_mbr_values,max_mbr_values)
    temp_area=reduce(lambda x,y: x*y,temp,1)
    return temp_area


def pickseeds_non_leaf(record):
    max_area=0
    seed_1=record[0]
    seed_2=record[1]
    for temp1 in record:
        for temp2 in record:
            if temp1!=temp2:
                temp3=[temp1,temp2]
                temp1_record=[]
                temp1_record.append(temp1)
                temp2_record=[]
                temp2_record.append(temp2)
                temp1_area=calculate_area_non_leaf_node(temp1_record)
                temp2_area=calculate_area_non_leaf_node(temp2_record)
                temp3_area=calculate_area_non_leaf_node(temp3)
                d=temp3_area-(temp1_area+temp2_area)
                if  d >= max_area:
                    max_area=d
                    seed_1=temp1
                    seed_2=temp2
    return (seed_1,seed_2)


#takes a leaf node and returns the mbr
def find_mbr_node_non_leaf(node):
    mbr=[]
    node_record=list(node.record)
    initial_record_mbr=node_record[0][1]
    min_limits=[]
    max_limits=[]
    for mbr_tuple in initial_record_mbr:
        min_limits.append(mbr_tuple[0])
        max_limits.append(mbr_tuple[1])


    for element in node_record:
        node_element_mbr=element[1]
        i=0
        while i<len(node_element_mbr):
            min_limits[i]=min([min_limits[i],node_element_mbr[i][0]])
            max_limits[i]=max([max_limits[i],node_element_mbr[i][1]])
            i=i+1
    mbr_returned=[]
    i=0
    while i<len(min_limits):
        temp_tuple=(min_limits[i],max_limits[i])
        mbr_returned.append(temp_tuple)
        i=i+1
    return mbr_returned

def find_mbr_node_leaf(node):
    mbr=[]
    node_record=node.record
    min_limits=list(node_record[0][1])
    max_limits=list(node_record[0][1])
    for element in node_record:
        node_element_data=element[1]
        i=0
        while i<len(node_element_data):
            min_limits[i]=min([min_limits[i],node_element_data[i]])
            max_limits[i]=max([max_limits[i],node_element_data[i]])
            i=i+1
    mbr_returned=[]
    i=0
    while i<len(min_limits):
        temp_tuple=(min_limits[i],max_limits[i])
        mbr_returned.append(temp_tuple)
        i=i+1
    return mbr_returned


#Takes a node and a new argument and returns a leaf node
def chooseleaf(node,new_element):
    if(isinstance(node,leaf_node)):
        return node
    else:
        new_element_data=list(new_element[1:])
        node_list=node.record
        area_difference_after_expansion=2**10000
        for element in node_list:
            tuple_element_mbr=element[1]
            temp=[]
            for limit_dimensions in tuple_element_mbr:
                difference_limits=abs(limit_dimensions[0]-limit_dimensions[1])
                temp.append(difference_limits)
            area_before_addition=reduce(lambda x,y: x*y,temp,1)
            temp=[]
            difference_limits=[]
            i=0
            while i<len(new_element_data):
                limit_dimensions=tuple_element_mbr[i]
                new_min_limit=min([new_element_data[i],limit_dimensions[0]])
                new_max_limit=max([new_element_data[i],limit_dimensions[1]])
                difference_limits=abs(new_max_limit-new_min_limit)
                temp.append(difference_limits)
                i=i+1
            area_after_addition=reduce(lambda x,y: x*y,temp,1)
            if(area_after_addition-area_before_addition < area_difference_after_expansion):
                area_difference_after_expansion=area_after_addition-area_before_addition
                required_child=element[0]
                area_before_expansion=area_before_addition
            elif(area_after_addition-area_before_addition == area_difference_after_expansion):
                if (area_before_addition < area_before_expansion):
                    area_difference_after_expansion=area_after_addition-area_before_addition
                    required_child=element[0]
                    area_before_expansion=area_before_addition
        return chooseleaf(required_child,new_element)


#Takes a a leaf node record and splits it into 2 records

def split_node(record_temp):
    record=list(record_temp)
    (temp1,temp2)=pickseeds(record)
    record.remove(temp1)
    record.remove(temp2)
    split_record_1=[]
    split_record_2=[]
    split_record_1.append(temp1)
    split_record_2.append(temp2)

    if len(record)==(minimum_size-1):
        record.append(temp1)
        split_record_1=record
    else:
        while len(record)!=0:
            return_record=picknext(record,split_record_1,split_record_2)
            record.remove(return_record)
            old_area_1=calculate_area_leaf(split_record_1)
            old_area_2=calculate_area_leaf(split_record_2)
            split_record_1.append(return_record)
            split_record_2.append(return_record)
            if calculate_area_leaf(split_record_1)< calculate_area_leaf(split_record_2):
                split_record_2.remove(return_record)
            elif calculate_area_leaf(split_record_1)>calculate_area_leaf(split_record_2):
                split_record_1.remove(return_record)
            elif old_area_1>old_area_2:
                split_record_1.remove(return_record)
            elif old_area_1<old_area_2:
                split_record_2.remove(return_record)
            elif len(split_record_1) < len(split_record_2):
                split_record_2.remove(return_record)
            else:
                split_record_1.remove(return_record)
            if (len(record)+len(split_record_1) == minimum_size) and len(record)!=0:
                split_record_1=split_record_1 + record
                break
            elif (len(record)+len(split_record_2) == minimum_size) and len(record)!=0:
                split_record_2=split_record_2 + record
                break
    return (split_record_1,split_record_2)



# takes a record and two other records and return a member of record

def picknext(record,rectangle_1,rectangle_2):
    difference=0
    return_record=record[0]
    record_rectangle_1_area=calculate_area_leaf(rectangle_1)
    record_rectangle_2_area=calculate_area_leaf(rectangle_2)
    for record_entry in record:
        rectangle_1.append(record_entry)
        d1=calculate_area_leaf(rectangle_1)-record_rectangle_1_area
        rectangle_2.append(record_entry)
        d2=calculate_area_leaf(rectangle_2)-record_rectangle_2_area
        rectangle_1.remove(record_entry)
        rectangle_2.remove(record_entry)
        if abs(d1-d2)>difference:
            difference=abs(d1-d2)
            return_record=record_entry
    return return_record


#takes a record of leaf node and calculates area
def calculate_area_leaf(record):
    if len(record)==1:
        return 0
    first_record=record[0]
    max_dimensions=list(first_record[1])
    min_dimensions=list(first_record[1])
    for single_element in record:
        element_dimensions=single_element[1]
        i=0
        while i<len(element_dimensions):
            if element_dimensions[i]<=min_dimensions[i]:
               min_dimensions[i]=element_dimensions[i]
            if element_dimensions[i]>=max_dimensions[i]:
               max_dimensions[i]=element_dimensions[i]
            i=i+1
    temp=map(lambda x,y:abs(x-y), max_dimensions,min_dimensions)
    temp_area=reduce(lambda x,y: x*y,temp,1)
    return temp_area



def pickseeds(record):
    max_area=0
    tie_breaker=0
    seed_1=record[0]
    seed_2=record[1]
    for temp1 in record:
        for temp2 in record:
            if temp1!=temp2:
                temp3=[temp1,temp2]
                temp_area=calculate_area_leaf(temp3)
                if  temp_area >= max_area:
                    if temp_area==max_area and temp_area==0:
                        temp=map(lambda x,y:abs(x-y),temp1[1],temp2[1])
                        tie_breaker_temp=reduce(lambda x,y: x+y,temp,0)
                        if(tie_breaker_temp>tie_breaker):
                            seed_1=temp1
                            seed_2=temp2
                            tie_breaker=tie_breaker_temp
                    else:
                        max_area=temp_area
                        seed_1=temp1
                        seed_2=temp2
    return (seed_1,seed_2)



def print_rtree(node):
    queue=[node]
    i=0
    print(queue)
    while queue!=[]:
        print("Level ",i,"is :")
        temp_queue=[]
        for element in queue:
            if isinstance(element,leaf_node):
                print("Reached leaf nodes")
                print(element.record)
                print("breaking")
            else:
                print(element)
                record_element=element.record
                print(record_element)
                for element_1 in record_element:
                    print(element_1[1])
                    temp_queue.append(element_1[0])
                    if isinstance(element,leaf_node):
                        print("no break")
                        print("Reached leaf nodes")
        queue=temp_queue
        i=i+1


#Function to find dominators between 2 lists


def find_dominate(list1,list2):
    dom_1=0
    dom_2=0
    j=0
    while j < len(list1):
        i=int(j)
        if(float(list1[i])>float(list2[i])):
            dom_2=dom_2+1
        elif(float(list2[i])>float(list1[i])):
            dom_1=dom_1+1
        else:
            dom_1=dom_1+1
            dom_2=dom_2+1
        j=j+1
    if(dom_1==dom_2):
        return 0
    elif(dom_1==len(list1)):
        return 1
    elif(dom_2==len(list1)):
        return 2
    else:
        return 0

def find_min_point_mbr(mbr):
    min_points=[]
    for element in mbr:
        min_points.append(element[0])
    return min_points

def find_distance_between_points(point1,point2):
    i=0
    distance=0
    while i<len(point1):
        distance=distance+abs(point1[i]-point2[i])
        i=i+1
    return distance

def check_same_quadrant(list1,list2,list3):
    i=0;
    while i<len(list1):
        if (list1[i]-list3[i])*(list2[i]-list3[i])<0:
            return 0
        i=i+1
    return 1


def check_global_dominance(list1,list2,list3):
    if check_same_quadrant(list1,list2,list3)==0:
        return 0
    i=0
    list1_dominates=0
    list2_dominates=0
    while i<len(list1):
        if((abs(list1[i]-list3[i]))<(abs(list2[i]-list3[i]))):
            list1_dominates=list1_dominates+1
        elif((abs(list1[i]-list3[i]))>(abs(list2[i]-list3[i]))):
            list2_dominates=list2_dominates+1
        else:
            list1_dominates=list1_dominates+1
            list2_dominates=list2_dominates+1
        i=i+1
    if(list1_dominates==list2_dominates):
        return 0
    elif(list1_dominates==len(list1)):
        return 1
    elif(list2_dominates==len(list1)):
        return 2
    else:
        return 0

#list1 is potential RSL and list2 is query point
def construct_rectangle_query(list1,list2):
    i=0
    rectangle=[]
    while i<len(list1):
        limits=[]
        if list1[i]<list2[i]:
            lower_limit=list1[i]-(list2[i]-list1[i])
            upper_limit=list2[i]
        elif list1[i]>list2[i]:
            upper_limit=list1[i]+(list1[i]-list2[i])
            lower_limit=list2[i]
        else:
            upper_limit=list1[i]
            lower_limit=upper_limit
        if lower_limit<0:
            lower_limit=0
        if upper_limit<0:
            upper_limit=0
        limits.append(lower_limit)
        limits.append(upper_limit)
        rectangle.append(limits)
        i=i+1
    return rectangle
#returns 1 if list1 is a member of list2
#check boundary condition
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

#returns 1 if list1 is a k-dominant member of list2,else 0
def check_k_membership(list1,list2,k):
    count=0
    flag=0
    i=0
    while i<len(list1):
        limits=list2[i]
        if(list1[i]>=limits[0] and list1[i]<=limits[1]):
            count=count+1
            if(list1[i]>limits[0] and list1[i]<limits[1]):
                flag=1
        i=i+1
    if(flag==1 and count>=k):
        return 1
    return 0

def find_min_point_mbr_from_q(mbr,q):
    min_points=[]
    i=0
    while i<len(mbr):
        element=mbr[i]
        if(abs(q[i]-element[0])<abs(q[i]-element[1])):
            min_points.append(element[0])
        else:
            min_points.append(element[1])
        i=i+1
    return min_points





def bbrs(root,q,k,records):
    class struct_node:
       val=0
       ide=0	
    s=[]
    for i in range(len(records[0])-1):

	tempo=[] 
        for j in range(len(records)):
        
            nn=struct_node()
            nn.val=abs(records[j][i+1]-q[i]);
            nn.ide=j;             
            tempo.append(nn);
            
        
        tempo=sorted(tempo, key=lambda x:x.val )
        #sort(tempo.begin(),tempo.end(),myfunc);
        s.append(tempo);
    global reverse_skyline
    global global_skyline
    global heap
    global k_reverse_skyline
    global number_of_comparisons
    reverse_skyline=[]
    heap=[]
    k_reverse_skyline=[]
    global_skyline=[]
    #print(root.record)	
    heap_insert(root,q)
    heap=sorted(heap,key=lambda x:float(x[1]))
 #   print(heap)
    while heap!=[]:
        first_item=heap[0]
	#print("First item of heap")
	#print(first_item)
	
        if first_item[0]==0:#means leaf
            dominated=0
            if global_skyline!=[]:
                for skyline_point in global_skyline:
                    dominate_value=check_global_dominance(skyline_point[1],first_item[2],q)
                    number_of_comparisons=number_of_comparisons+1
  #                  print(dominate_value)
                    if(dominate_value==1):
                        dominated=1
                        break
            if(dominated!=1):
                global_skyline.append(first_item[3])
   #            print(global_skyline)
                rectangle=construct_rectangle_query(first_item[2],q)
		#print("Rectangle")		
		#print(rectangle);
                is_k_reverse_skyline=1
                #print("Sending check for rectangle corresponding to ",first_item[2]) 
                comp_count=[] 
	        comp_count.append(0);
                is_k_reverse_skyline=my_func(s,rectangle,q,records_modified,first_item[2],comp_count,k) 
		number_of_comparisons=number_of_comparisons+comp_count[0];
                '''for element in records:
                        element_data=element[1:]
                        if element_data!=first_item[2]:
                            number_of_comparisons=number_of_comparisons+1
                            if check_membership(element_data,rectangle)==1:
                                is_reverse_skyline=0
                                break
                if is_reverse_skyline==1:
                    reverse_skyline.append(first_item[3])
                    is_k_reverse_skyline=1
                    for element in records:
                        element_data=element[1:]
                        if element_data!=first_item[2]:
                            number_of_comparisons=number_of_comparisons+1 
                            if check_k_membership(element_data,rectangle,k)==1:
                                is_k_reverse_skyline=0
                                break'''
                if is_k_reverse_skyline==1:
                        k_reverse_skyline.append(first_item[3])
        else:
            heap_insert(first_item[3][0],q)
            heap=sorted(heap,key=lambda x:float(x[1]))
        heap.remove(first_item)


def heap_insert(element,q):
    global number_of_comparisons
    if isinstance(element,leaf_node):
        element_record=element.record
        for data in element_record:
            dominated=0
            only_data=data[1]
            id=data[0]
            if global_skyline!=[]:
                for skyline_point in global_skyline:
                    number_of_comparisons=number_of_comparisons+1
                    dominate_value=check_global_dominance(skyline_point[1],only_data,q)
                    if(dominate_value==1):
                        dominated=1
                        break
            if(dominated!=1):
                d=find_distance_between_points(only_data,q)
                heap.append([0,d,only_data,data])
    if isinstance(element,non_leaf_node):
        element_record=element.record
        for data in element_record:
            dominated=0
            mbr=data[1]
            min_points=find_min_point_mbr_from_q(mbr,q)
            if(check_membership(q,mbr)==0):
                min_points=find_min_point_mbr_from_q(mbr,q)
  #          min_points=find_min_point_mbr(mbr)
                if global_skyline!=[]:
                    for skyline_point in global_skyline:
                        number_of_comparisons=number_of_comparisons+1
                        dominate_value=check_global_dominance(skyline_point[1],min_points,q)
                        if(dominate_value==1):
                            dominated=1
                            break
            if(dominated!=1):
                d=find_distance_between_points(min_points,q)
                heap.append([1,d,min_points,data])



number_of_comparisons=0

start_time=time.time()

data_records=open(sys.argv[1],mode="r")
whole_file=data_records.readlines()
records=[]
for file_line in whole_file:
    file_line=file_line.rstrip('\n')
    #print(file_line) 	
    records.append(file_line.split(',' ))
data_records.close()

#for i in range(len(records)):
#   print(records[i])

query_details=open(sys.argv[2],mode="r")
query_file=query_details.readlines()
temp=query_file[0].rstrip('\n')
dimensions_compared=temp.split()

dimensions_compared_temp=[]
for element in dimensions_compared:
    dimensions_compared_temp.append(int(element))
dimensions_compared=dimensions_compared_temp


temp=query_file[1].rstrip('\n')
#print(temp)
disk_size=int(temp)


temp=query_file[2].rstrip('\n')
temp2=temp.split()
pointer_size=int(temp2[0])
key_size=int(temp2[1])
temp=query_file[3].rstrip('\n')
k=int(temp)

query_details.close()

records_modified=[]
for record_element in records:
    record_element_modified=[]
    i=0
    while i < (len(record_element)):
        if i in dimensions_compared or i==0:
            if i==0:
                record_element_modified.append(int(record_element[i]))
            else:
                record_element_modified.append(float(record_element[i]))
        i=i+1
    records_modified.append(record_element_modified)



maximum_size=int(disk_size/(key_size+pointer_size))
minimum_size=int(maximum_size/2)+1


root=[]
#q=[1.23219e+09, 1.6226e+09, 1.11538e+08, 3.38788e+08, 2.14747e+09, 4.38792e+08, 1.91117e+09, 2.69542e+08, 2.16276e+09, 1.16088e+08]  
q=[0,0,0,0,0,0,0,0,0,0]
#q=[3288,109,12,567,89,3122,241,225,139,3539]
#records_modified=[[1,1.5,1,1],[2,2,2,2],[4,4,4,4]]
for temp in records_modified:
    rtree_insert(temp)
	


#print(root);

bbrs(root,q,k,records_modified)
end_time=time.time()

global_skyline_id=[]
for element in global_skyline:
    global_skyline_id.append(element[0])
reverse_skyline_id=[]
for element in reverse_skyline:
    reverse_skyline_id.append(element[0])
k_reverse_skyline_id=[]
for element in k_reverse_skyline:
    k_reverse_skyline_id.append(element[0])

print("Number of global skylines are ",len(global_skyline))
#print("Number of reverse skylines are ",len(reverse_skyline))
print("Number of k-dominant reverse skylines are ",len(k_reverse_skyline_id))
print("k-dominant reverse skylines are",k_reverse_skyline_id)



print("The time taken to run the program is ",end_time-start_time)
print("number of comparisons are",number_of_comparisons)





