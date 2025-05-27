# GA Financial Census (2025)
Author: Takashi Yokokura, Internal Vice President 2024-25
_Not the best code, but I did my best :)_

## Overview: 
Census.py module for analyzing Qualtrics dataset, containing two, main class methods:
* `Census.count_single_choice()`: for questions limited to one selection, returns a dataframe of labels and counts 
* `Census.count_multi_choice()`: for questions not limited to one selection, returns a dataframe of labels and counts
These dataframes can then be plotted using modules of your choice, e.g., matplotlib.

Additional functionality:
* `Census.section(datarange, original_df)`: provide another instance of Census class for a subset of the data provided by `datarange`
* `Census.show_qlist()`: display list of questions corresponding to data stored in this instance
* `Census.pop_other(colname)`: pop question matching `colname` from data and print the responses. Used to clean data and display responses to 'Other (please specify) - Text'
* `alias_labels(df, als)`: returns a new dataframe from `df` with column `alias` of new, user-defined names for labels provided by dict `als`:
  ```
  new_df = Census.alias_labels(old_df, als = {'Some old label': 'New label'})
  new_df.alias
  ```
  Note `als` only has to be a dict of the labels that you want to replace.

## How to use
To handle the data, Census.py provides the `Census` class. From a high-level, data analysis proceeds as follows:
1. Initialize an instance of the class:
   ```
   import Census as Census
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
