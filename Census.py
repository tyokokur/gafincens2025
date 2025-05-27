import numpy as np, pandas as pd
import matplotlib.pyplot as plt, matplotlib as mpl

class Census:
    """
    docstring for Census class
    """
    def __init__(self, filepath='', header=1, datarange=(17,None), from_file=True, 
                 orig_df=pd.DataFrame({'empty':[0]}), orig_datarange=(None,None)):
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
        
        
        
        