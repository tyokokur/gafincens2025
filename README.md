# GA Financial Census (2025)
Author: Takashi Yokokura, Internal Vice President 2024-25

## Overview: 
Census.py module for analyzing Qualtrics dataset, containing two main functions:
* `count_single_choice`: for questions limited to one selection, returns a dataframe of labels and counts 
* `count_multi_choice`: for questions not limited to one selection, returns a dataframe of labels and counts

To handle the data, Census.py provides the `Census` class. From a high-level, data analysis proceeds as follows:
1. Initialize an instance of the class:
   ```
   census_class = Census.Census(filepath, datarange=(start, stop))
   ```
    `filepath`: location of the file (e.g., 'C:/Users/username/Desktop/Qualtrics_export.csv')
   
    `(start, stop)`: range of relevant data columns to proceed with
2. A summary of the data will be provided for reference. Sample output:
   ```
   Initialization completed.
   Data recorded
	    from column R: 
		    "What division is your program in? - Selected Choice"
	    to column BS: 
		    "If you would like to provide more information on accessibility, please do so here."
   362 responses.
   54 questions asked.
   ```
