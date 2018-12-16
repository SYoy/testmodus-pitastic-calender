import pandas
import numpy

def read_from_config(file='config.csv'):
    data = pandas.read_csv(file, names=['date','num_left','special'])
    date = data.date.tolist()
    nums = data.num_left.tolist()
    special = data.special.tolist()

    return date,nums,special
    
def write_to_config(toAddList):
    pd = pandas.read_csv('config.csv', names=['date','num_left','special'])
    pd.loc[len(pd)] = toAddList
    pd.to_csv('config.csv', header=False)
    #print(pd)
    
    return None

def write_to_librarian(Ok,Used):
    old = pandas.read_csv('librarian.csv', names=['Database_Indices','Used_Data','Always_Usable'])
    ok_col = pandas.DataFrame({'Ok':Ok})
    used_col = pandas.DataFrame({'Used':Used})
    always_col = old['Always_Usable']
    pd = pandas.concat([ok_col,used_col,always_col], ignore_index=True,axis=1)
    pd.to_csv('librarian.csv', header=False)
    
    return None

def read_from_librarian(file='librarian.csv'):
    data = pandas.read_csv(file, names=['Database_Indices','Used_Data','Always_Usable'])
    good = data.Database_Indices.tolist()
    used = data.Used_Data.tolist()
    always = data.Always_Usable.tolist()
    good = [x for x in good if not numpy.isnan(x)]
    used = [x for x in used if not numpy.isnan(x)]
    always = [x for x in always if not numpy.isnan(x)]

    return good,used,always

def init_librarian(Ok,Used,Always):
    ok_col = pandas.DataFrame({'Ok':Ok})
    used_col = pandas.DataFrame({'Used':Used})
    always_col = pandas.DataFrame({'Always':Always})
    pd = pandas.concat([ok_col,used_col,always_col], ignore_index=True,axis=1)
    pd.to_csv('librarian.csv', header=False)
    
    return None
