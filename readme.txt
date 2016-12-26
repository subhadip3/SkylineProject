Running the codes requires 2 files to be given as command line arguments
eg: python krslBrute.py FinalDataset1000c.txt b.txt 
First one is the dataset, the format for which is provided in FinalDataset1000c.txt
Second one is b.txt, the description of which is as follows.
1st line contains the dimensions to be compared.
2nd line contains the disk size(for R-tree)
3rd line contains pointer size and key size(for R-tree)
4th line contains k.

The query point is hard coded inside as [0,0,0,0,0,0,0,0,0,0]
krslBrute is the code for finding reverse k-dominant skylines as described in algorithm1.
krslWithAggregation is the code for finding reverse k-dominant skylines as described in algorithm2.
krslSir is the code for finding reverse k-dominant skylines as described in algorithm3.
The files aggregation.py and aggregationSir.py are called internally while running 
krslWithAggregation.py and krslSir.py respectively and contain the part where the main 
difference arises between the 3 codes.
 
