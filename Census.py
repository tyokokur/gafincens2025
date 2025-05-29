""" 
Module providing Census class and three helper functions to analyze Qualtrics data 

...

Classes
-------
Census
    class used to analyze Qualtrics data, designed for 
      the UC Berkeley Graduate Assembly 2025 Financial Census

Functions
---------
num_to_exel_col(n)
    Returns Excel-based column name corresponding to inputted number
    
alias_labels(df, als)
    Returns new dataframe from df with new column "alias" composed of first 
     column updated using input als dict. If certain values are not aliased, 
     original values are maintained
    
move_to_bot(df, cond)
    Returns new dataframe from df reordered with row matching cond moved to 
     the last row. Helpful for questions with 'Other' as one of many options
"""

import numpy as np, pandas as pd

class Census:
    """ 
    A class used to analyze Qualtrics data, designed for 
     the UC Berkeley Graduate Assembly 2025 Financial Census
    
    ...

Attributes
----------
data_df : pandas DataFrame
    extracted data from csv with each row as a survey response
qlist : list of str
    questions asked in survey (columns of data_df)
datarange : tuple of int
    range of columns (questions) to store
num_popped : int
    tracker of columns popped to maintain correct original spreadsheet column names

Methods
-------
count_single_choice(colname, sort=True)
    For a single-choice question, returns df of choices and number of responses 
     indicating that choice

count_multi_choice(colname, sort=True)
    For a multi-choice ("select all that apply") question, returns df of choices 
     and number of responses indicating that choice

section(datarange, orig_df)
    Returns a new Census class instance using the inputted datarange

show_qlist()
    Prints formatted list of questions stored corresponding to column names
    
pop_other(colname)
    Removes question corresponding to colname from self.data_df and print the 
     responses received for that question
    
_init_from_file(filepath, header=1, datarange)
    Internal function initializing Census class instance from local file
"""
    
    def __init__(self, filepath='', header=1, datarange=(17,None), from_file=True, 
                 orig_df=pd.DataFrame({'empty':[0]}), orig_datarange=(None,None)):
        """
        Parameters
        ----------
        filepath : str
            Local location of Qualtrics csv file to analyze
        header : int
            Row of column names (default 1)
        datarange : (int, int)
            Column indices corresponding to start and stop of data to store from input file
             (default (17, None))
        from_file : bool
            Whether to initialize instance from file (e.g., from Qualtrics CSV) or from 
             Census.c
        """
        if from_file:
            df = self._init_from_file(filepath=filepath, header=header, datarange=datarange)
            self.orig_datarange = datarange
            datarange = (0, 0)
        else:
            df = orig_df.iloc[:, datarange[0]:datarange[1]]
            self.orig_datarange = orig_datarange
        
        # Update 
        self.data_df = df
        self.qlist   = df.columns.to_list()
        self.datarange=datarange
        self.num_popped = 0
        
        # Report
        firstcol= self.orig_datarange[0]+datarange[0]
        lastcol = df.shape[1]+self.orig_datarange[0]+datarange[0]-1
        print('Initialization completed.')
        print('Data recorded')
        print('\tfrom column {}: \n\t\t"{}"'.format(num_to_exel_col(firstcol), self.qlist[0]))
        print('\tto column {}: \n\t\t"{}"'.format(num_to_exel_col(lastcol), self.qlist[-1]))
        print('{} responses.\n{} questions asked.'.format(*df.shape))
        return
    
    def count_single_choice(self, colname, sort=True):
    """For a single-choice question, returns df of choices and number of responses 
        indicating that choice
        
        Parameters
        ----------
        colname : str
            Name of column corresponding to question being asked
        sort : bool, optional
            Whether the data should be sorted (alpha, numer, etc.) based on the questions
        
        Returns
        -------
        df : pandas DataFrame
            Columns 'labels' for response option and 'counts' for number of
             responses which indicated that option
    """
        data  = self.data_df[colname]
        labels= data[data.notna()].unique()
        if sort: labels.sort()
        counts = [data[data==labels[i]].count() for i in range(len(labels))]
        df = pd.DataFrame([labels, counts]).T
        df.columns = ['labels', 'counts']
        return df
    
    def count_multi_choice(self, colname, sort=True):
        data = self.data_df[colname].str.split(',', expand=True)
        labels = pd.unique(data[data.notna()].values.flatten())
        labels = labels[pd.notnull(labels)]
        if sort: labels.sort()
        flat = data.values.flatten()
        counts = [flat[flat == i].size for i in labels]
        df = pd.DataFrame([labels, counts]).T
        df.columns = ['labels', 'counts']
        return df
        
    def section(self, datarange=(None,None), orig_df=pd.DataFrame({'empty':[0]})):
        return Census(from_file=False, datarange=datarange, orig_df=orig_df, orig_datarange=self.orig_datarange)
        
    def show_qlist(self):
        print(*['\t{}. {}\n'.format(ind+1, i) for ind, i in enumerate(self.qlist)])
        return
    
    def pop_other(self, colname):
        ind = self.data_df.columns.get_loc(colname)
        print_fil = lambda x: print('\tResponses: '+str([i for i in x[x.notna()]]))
        
        print('Popping Q{} (column {}): \n\t{}'.format(ind+self.num_popped+1, num_to_exel_col(self.datarange[0]+self.orig_datarange[0]+ind+self.num_popped), self.qlist[ind]))
        self.num_popped += 1
        
        other = self.data_df.pop(self.qlist[ind])
        self.qlist.pop(ind)
              
        if other.count() > 0: 
            print_fil(other)
        else: 
            print('\tResponses: None')
    
    def _init_from_file(self, filepath, header=1, datarange=(17,None)): 
        from pathlib import Path
        p = Path(filepath)
        df = pd.read_csv(p, header=header)
        df = df.drop([0]) # Discard IP addresses
        df = df[df['Response Type']!='Survey Preview'].reset_index(drop=True) # No previews
        df = df.iloc[:, datarange[0]:datarange[1]] # Discard unnecessary data
        return df
        
def num_to_exel_col(n):
    # Source: https://stackoverflow.com/questions/23861680/convert-spreadsheet-number-to-column-letter
    d, m = divmod(n,26) # 26 is the number of ASCII letters
    return '' if n < 0 else num_to_exel_col(d-1)+chr(m+65)

def alias_labels(df, als):
    new = np.empty(df.shape[0], dtype=object)
    for i in range(len(new)):
        try: new[i] = als[df.iloc[i,0]]
        except KeyError: new[i] = df.iloc[i,0]
    return pd.concat([df,pd.Series(new, name='alias')], axis=1)
        
def move_to_bot(df, cond):
    idx = df.index[cond]
    return pd.concat([df.drop(idx), df.loc[idx]], ignore_index=True)