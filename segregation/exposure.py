"""
Exposure Segregation Metrics
"""

__author__ = "Renan X. Cortes <renanc@ucr.edu> and Sergio J. Rey <sergio.rey@ucr.edu>"

import numpy as np
import pandas as pd

__all__ = ['Exposure']


def _exposure(data, group_pop_var, total_pop_var):
    """
    Calculation of Exposure index

    Parameters
    ----------

    data          : a pandas DataFrame
    
    group_pop_var : string
                    The name of variable in data that contains the population size of the group of interest (X)
                    
    total_pop_var : string
                    The name of variable in data that contains the total population of the unit

    Attributes
    ----------

    statistic : float
                Exposure Index
                
    core_data : a pandas DataFrame
                A pandas DataFrame that contains the columns used to perform the estimate. 

    Notes
    -----
    The group of interest is labelled as group X, whilst Y is the complementary group. Groups X and Y are mutually excludent.
    
    Based on Massey, Douglas S., and Nancy A. Denton. "The dimensions of residential segregation." Social forces 67.2 (1988): 281-315.

    """
    if((type(group_pop_var) is not str) or (type(total_pop_var) is not str)):
        raise TypeError('group_pop_var and total_pop_var must be strings')
    
    if ((group_pop_var not in data.columns) or (total_pop_var not in data.columns)):    
        raise ValueError('group_pop_var and total_pop_var must be variables of data')

    data = data.rename(columns={group_pop_var: 'group_pop_var', 
                                total_pop_var: 'total_pop_var'})
    
    x = np.array(data.group_pop_var)
    t = np.array(data.total_pop_var)
    
    if any(t < x):    
        raise ValueError('Group of interest population must equal or lower than the total population of the units.')
   
    yi = t - x
    
    X = x.sum()
    xPy = np.nansum((x / X) * (yi / t))
    
    core_data = data[['group_pop_var', 'total_pop_var']]
    
    return xPy, core_data


class Exposure:
    """
    Classic Exposure Index

    Parameters
    ----------

    data          : a pandas DataFrame
    
    group_pop_var : string
                    The name of variable in data that contains the population size of the group of interest (X)
                    
    total_pop_var : string
                    The name of variable in data that contains the total population of the unit

    Attributes
    ----------

    statistic : float
                Exposure Index

    core_data : a pandas DataFrame
                A pandas DataFrame that contains the columns used to perform the estimate. 
                
    Examples
    --------
    In this example, we will calculate the Exposure Index (xPy) for the Riverside County using the census tract data of 2010.
    The group of interest (X) is non-hispanic black people which is the variable nhblk10 in the dataset and the Y group is the other part of the population.
    
    Firstly, we need to read the data:
    
    >>> This example uses all census data that the user must provide your own copy of the external database.
    >>> A step-by-step procedure for downloading the data can be found here: https://github.com/spatialucr/osnap/tree/master/osnap/data.
    >>> After the user download the LTDB_Std_All_fullcount.zip and extract the files, the filepath might be something like presented below.
    >>> filepath = '~/data/std_2010_fullcount.csv'
    >>> census_2010 = pd.read_csv(filepath, encoding = "ISO-8859-1", sep = ",")
    
    Then, we filter only for the desired county (in this case, Riverside County):
    
    >>> df = census_2010.loc[census_2010.county == "Riverside County"][['pop10','nhblk10']]
    
    The value is estimated below.
    
    >>> exposure_index = Exposure(df, 'nhblk10', 'pop10')
    >>> exposure_index.statistic
    0.886785172226587
    
    The interpretation of this number is that if you randomly pick a X member of a specific area, there is 88.68% of probability that this member shares a unit with a Y member.
    
    Notes
    -----
    The group of interest is labelled as group X, whilst Y is the complementary group. Groups X and Y are mutually excludent.
    
    Based on Massey, Douglas S., and Nancy A. Denton. "The dimensions of residential segregation." Social forces 67.2 (1988): 281-315.

    """

    def __init__(self, data, group_pop_var, total_pop_var):
        
        aux = _exposure(data, group_pop_var, total_pop_var)

        self.statistic = aux[0]
        self.core_data = aux[1]
        self._function = _exposure

