import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

%matplotlib inline
%config InlineBackend.figure_format = 'retina'

def plotWaterfall(inputlist, figsize = (10,6), last_as_net = False, colors = ['blue','red'], return_df=False):
    
    # calculate constants
    XINDEX = range(len(inputlist)+1)
    ADJ = [float(x[1]) for x in inputlist]
    NET = sum(ADJ)
    ADJ.append(NET)
    YBUFFER = 0.25
    XBUFFER = -.15
    POS_COLOR, NEG_COLOR = colors
    
    #trim input for zeros, remove from input
    inputlist = [(x[0],float(x[1])) for x in inputlist if x[1]!=0]
        
    # make a dataframe, store the data
    df = pd.DataFrame(inputlist)
    df.columns = ['labels','values']
    df['labels'] = df['labels']
    
    # get a running total
    df['runsum'] = df.iloc[:,1].cumsum()
    
    # shift the rows, previous row is start for 
    # new row
    df['from'] = df.iloc[:,2].shift(1)
    
    # after shift fill the last column with zero
    df.fillna(0,inplace=True)
    
    # make an additional column, the max of either from or runsum
    df['min'] = df.apply(lambda x: min(x['runsum'],x['from']), axis=1)

    df['max'] = df.apply(lambda x: max(x['runsum'],x['from']), axis=1)
    df['plus_max'] = df.apply(lambda x : x['max'] if x['values'] > 0 else 0, axis=1)
    df['minus_max'] = df.apply(lambda x : x['max'] if x['values'] < 0 else 0, axis =1)
    
    # add the net row
    net_row = pd.DataFrame([{'labels':'net', 
                             'values':0,
                             'runsum':NET,
                             'from': 0., 
                             'min':0.,
                             'max':NET, 'plus_max':NET,'minus_max': 0.}])

    df = df.append(net_row)
    df.reset_index(inplace=True)

    df.plot.line(x='labels',y='runsum',legend=False, style=':')
    df['plus_max'].plot(kind='bar', stacked=True, color=POS_COLOR)
    df['minus_max'].plot(kind='bar', stacked=True, color=NEG_COLOR)

    
    my_plot = df['min'].plot(kind='bar', stacked=True, color='white', figsize= figsize)
    my_plot.set_xticklabels(df['labels'],rotation=0)
    
    # labels
    Y_MAX = df['max']
    CUMSUM = df['runsum']
        
    # plot main totals
    for xindex, cumsum, adj, y_max in zip(XINDEX, CUMSUM, ADJ, Y_MAX):
        # plot main totals
        my_plot.annotate('%.1f' % cumsum , 
                         xy=(0,0), 
                         xytext=(xindex + XBUFFER,y_max+YBUFFER), 
                         #fontsize=12, 
                         fontweight='bold')
    
    
    CUMSUM_DIFF = df['runsum'].diff().values[1:]/2.

    Y_ADJ = CUMSUM_DIFF + df['runsum'].values.astype(float)[:-1]
    
    
    #plot deltas
    for xindex, adj, y_adj in zip(XINDEX[:-1], ADJ[1:],Y_ADJ):
        # plot main totals
        if adj >= 0.0:
            color = 'green'
        else:
            color = 'red'
            
        my_plot.annotate('%.1f' % adj , 
                         xy=(0,0), 
                         xytext=(xindex+XBUFFER+.5,y_adj+YBUFFER), 
                         #fontsize=12, 
                         fontweight='bold',
                         color = color
                        )
    if return_df == True:
        return df

# ### run a sample:

# random_input = [
#     ('start',10),
#     ('adj1',-1),
#     ('adj2',+15),
#     ('adj3',0),
#     ('adj3',-3)
# ]

# dd = plotWaterfall(random_input, colors = ['black','red'])