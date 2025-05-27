# GA Financial Census (2025)
Author: Takashi Yokokura, Internal Vice President 2024-25

_Not the best code, but I did my best :)_

## Overview: 
Census.py module for analyzing Qualtrics dataset, containing two workhorse class methods:
* `Census.count_single_choice()`: for questions limited to one selection, returns a dataframe of labels and counts 
* `Census.count_multi_choice()`: for questions not limited to one selection, returns a dataframe of labels and counts
These dataframes can then be plotted using modules of your choice, e.g., matplotlib.

Additional functionality:
* `Census.section(datarange, original_df)`: provide another instance of Census class for a subset of the data provided by `datarange`
* `Census.show_qlist()`: display list of questions corresponding to data stored in this instance
* `Census.pop_other(colname)`: pop question matching `colname` from data and print the responses. Used to clean data and display responses to 'Other (please specify) - Text'
* `alias_labels(df, als)`: returns a new dataframe from `df` with column `alias` of new, user-defined names for labels provided by dict `als`

Notebook used to analyze 2025 GA Financial Census data can be found in `./notebook`.

## How to use
To handle the data, Census.py provides the `Census` class. From a high-level, data analysis proceeds as follows:
1. Initialize an instance of the class:
   ```
   import Census as Census
   census_inst = Census.Census(filepath, datarange=(start, stop))
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
3. If some questions cannot be plotted, pop them using `Census.pop_other(colname)`:
   ```
   list_of_unwanted_qs = [census_inst.qlist[1], census_inst.qlist[3], census_inst.qlist[4]] # Pop first and fourth questions
   for i in list_of_unwanted_qs: census_inst.pop_other(i)
   census_inst.show_qlist() # Updated question list
   ```
4. A summary of the popping will be provided from reference. Sample output:
   ```
   Popping Q1 (column S): 
	What division is your program in? - Other (please specify) - Text
	Responses: ['Some other division', 'Another division', 'Divison III']
   Popping Q4 (column U): 
		Which department are you in? - Other (please specify) - Text
		Responses: None
   Popping Q5 (column V): 
		Please specify which department you are in
		Responses: None
	
   1. What division is your program in? - Selected Choice
   2. Which department are you in? - Selected Choice
   3. What is your degree program?
   ```
5. Analyze the data using `Census.count_single_choice()` or `Census.count_multi_choice()` class methods depending on the question type.
   ```
   df_single = census_inst.count_single_choice(census_inst.qlist[0]) # Analyze first question (single choice)
   df_multi  = census_inst.count_multi_choice(census_inst.qlist[1])  # Analyze second question (mulit choice)
   ```
6. If new label names are desired, use `alias_labels(df, als)`:
   ```
   new_df = Census.alias_labels(old_df, als = {'Some old label': 'New label'})
   new_df.alias
   ```
   Note `als` only has to be a dict of the labels that you want to replace.
