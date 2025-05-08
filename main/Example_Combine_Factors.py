import ManageData    as md  #loads and saves data
import TransformData as td  #Cleans and transforms data
import FactorTester  as ft  #Test factors for suitability in models
import numpy         as np
import pandas as pd
from itertools import combinations
import itertools


def get_first_n_keys_as_list(dictionary, n):
  """
  Returns the first n keys of a dictionary as a list.

  Args:
    dictionary (dict): The input dictionary.
    n (int): The number of keys to retrieve.

  Returns:
    list: A list containing the first n keys of the dictionary.
  """
  return list(itertools.islice(dictionary, n))


def LoadData(CapRange):
    #CapRange can be All, High, Mid, or Low
    SaveFile                = 'Data' + CapRange + 'Cap' #Save loaded data in this file
    Filename                = SaveFile + '.xlsm' #load data in this file
    R1                      = md.removeloadeddata(SaveFile+'.pkl') #deletes any previously saved
    D                       = md.initialize()               #Creats a Python dictionary to store data
    D                       = md.loaddataFormat1(D,Filename)#Load data from spreadsheet
    Success                 = md.saveproject(D,SaveFile+'.pkl')    #Saves the loaded data to a pickel file
    D                       = md.loadproject(SaveFile+'.pkl')
    return D


def single_factor_alpha_test(cap_range):
    D = LoadData(cap_range)
    TD = {}
    FA = {}
    N = np.int_(5)
    TD['ForwardReturns_AP'] = D['ForwardReturns_AP'].copy()
    factor_ranking = {}
    R = {}
    factor_names = []
    Number_of_points = 100
    for key in D.keys():
        if key == 'Price_Book_AP':
            TD[key] = -D['Price_Book_AP'].copy()
            TD[key] = td.CleanData(TD[key], N)
            TransformList = ['ZSBT', 'ZSCSBS']
            TD[key] = td.Transform(TD[key], TransformList, D)
            FA[key] = ft.AnalyzeFactor(key, TD[key], TD['ForwardReturns_AP'], N)
            factor_names.append(key)
        elif key.endswith('_AP') and key != 'ForwardReturns_AP':
            TD[key] = D[key].copy()
            TD[key] = td.CleanData(TD[key], N)
            TransformList = ['ZSBT', 'ZSCSBS']
            TD[key] = td.Transform(TD[key], TransformList, D)
            # FA[key] = ft.AnalyzeFactor(key, TD[key], TD['ForwardReturns_AP'], N)
            try:
                FA[key] = ft.AnalyzeFactor(key, TD[key], TD['ForwardReturns_AP'], N)
            except IndexError:
                print(f"Warning: IndexError in AnalyzeFactor for {key}. Skipping this factor.")
                continue
            factor_names.append(key)

    for key, value in FA.items():
        if key in factor_names:
            factor_ranking[key] = FA[key]['ICitp']
    # sorted_dict_by_values = dict(sorted(my_dict.items(), key=lambda item: item[1]))
    factor_ranking = dict(sorted(factor_ranking.items(), key=lambda item: item[1], reverse=True))
    ranked_factor_list = get_first_n_keys_as_list(factor_ranking, 5)
    
    # Top 4
    top_4_ranked_factor_list = get_first_n_keys_as_list(factor_ranking, 4)
    # Top 5
    top_5_ranked_factor_list = get_first_n_keys_as_list(factor_ranking, 5)
    factor_pairs = list(combinations(ranked_factor_list, 2))
    for factor_1, factor_2 in factor_pairs:
        S2 = ft.Optimize_IRitp_2(TD[factor_1], TD[factor_2], TD['ForwardReturns_AP'], Number_of_points)
        R['S2'] = S2
    
    factor_triplets = list(combinations(ranked_factor_list, 3))
    for factor_1, factor_2, factor_3 in factor_triplets:
        S3 = ft.Optimize_IRitp_3(TD[factor_1], TD[factor_2], TD[factor_3], TD['ForwardReturns_AP'], Number_of_points)
        R['S3'] = S3
        
    factor_quads = list(combinations(top_4_ranked_factor_list, 4))    
    for factor_1, factor_2, factor_3, factor_4 in factor_quads:
        S4 = ft.Optimize_IRitp_4(TD[factor_1], TD[factor_2], TD[factor_3], TD[factor_4], TD['ForwardReturns_AP'], Number_of_points)
        R['S4'] = S4
    
    factor_quints = list(combinations(top_5_ranked_factor_list, 5))
    for factor_1, factor_2, factor_3, factor_4, factor_5 in factor_quints:
        S5 = ft.Optimize_IRitp_5(TD[factor_1], TD[factor_2], TD[factor_3], TD[factor_4], TD[factor_5], TD['ForwardReturns_AP'], Number_of_points)
        R['S5'] = S5
    
    # return (ranked_factor_list, factor_ranking, R)
    
    print(f"The Factors with the Highest IC Value are : {ranked_factor_list} for the {cap_range} dataset")
    print(f"The Highest IC Inter-temporal value (2 factor model) = {np.max(R['S2']['ICitp'])}")
    print(f"The Highest IC Inter-temporal value (3 factor model) = {np.max(R['S3']['ICitp'])}")
    print(f"The Highest IC Inter-temporal value (4 factor model) = {np.max(R['S4']['ICitp'])}")
    print(f"The Highest IC Inter-temporal value (5 factor model) = {np.max(R['S5']['ICitp'])}")
    return (cap_range, ranked_factor_list, np.max(R['S2']['ICitp']), np.max(R['S3']['ICitp']), np.max(R['S4']['ICitp']), np.max(R['S5']['ICitp']))
    


def new_column_name(current_name):
    new_column_name = f"{current_name}_AP"
    return new_column_name


def get_factors(excel_file):
    excel_file_data = pd.read_excel(excel_file,"data")
    factor_names = excel_file_data['Variable'].unique()
    factor_names = np.delete(factor_names, -1)
    return factor_names

            
def Run_Lab(D,SaveFile):
    # D could by Dall, Dhigh, Dmid, or Dlow
    #SaveFile could be RunNumber_5
    TD                      = {}  #Dictionary for transformed data
    FA                      = {}  #Dictionary for factors
    N                       = np.int_(5)  #Used to control data cleaning, see notes
    #Next 4 lines were added so forward returns will be used
    # print(type(D))
    Returns_AP              =  D['Returns_AP'].copy()
    # print(D['Returns_AP'])
    
    
    Returns_AP              =  D['Returns_AP'].copy()
    TD['ForwardReturns_AP'] =  D['ForwardReturns_AP'].copy()
    
    
    TD['Price_Book_AP']    	= -D['Price_Book_AP'].copy()        #Change the sign of price to book because high is bad, low is good
    TD['Price_Book_AP']    	= td.CleanData(TD['Price_Book_AP'],N) #Moderate outliers so model building is better
    TransformList           = ['ZSBT','ZSCSBS']                 #z-score by time, decile crosssection by sector
    TD['Price_Book_AP']    	= td.Transform(TD['Price_Book_AP'],TransformList,D)
    X = TD['Price_Book_AP']
    
    NumTile                 = np.int_(5)
    FA['Price_Book_AP']     = ft.AnalyzeFactor('Price_Book',TD['Price_Book_AP'],TD['ForwardReturns_AP'],NumTile)

    N                       = np.int_(5)
    TD['STMomentum_AP']    	= D['STMomentum_AP'].copy()
    TD['STMomentum_AP']    	= td.CleanData(TD['STMomentum_AP'],N)   #Moderate outliers so model building is better
    TransformList           = ['ZSBT','ZSCSBS']                     #z-score by time, decile crosssection by sector
    TD['STMomentum_AP']    	= td.Transform(TD['STMomentum_AP'],TransformList,D)
    NumTile                 = np.int_(5)                        	#Number of quantiles to use in AnalyzeFactor
    FA['STMomentum_AP']    	= ft.AnalyzeFactor('STMomentum',TD['STMomentum_AP'],TD['ForwardReturns_AP'],NumTile)
    

    N                           = np.int_(5)
    TD['SurpriseMomentum_AP']   = D['SurpriseMomentum_AP'].copy()
    TD['SurpriseMomentum_AP']   = td.CleanData(TD['SurpriseMomentum_AP'] ,N)  	#Moderate outliers so model building is better
    TransformList           = ['ZSBT','ZSCSBS']                     #z-score by time, decile crosssection by sector
    NumTile                 = 5                       				#Number of quantiles to use in AnalyzeFactor
    TD['SurpriseMomentum_AP']   = td.Transform(TD['SurpriseMomentum_AP'] ,TransformList,D)
    FA['SurpriseMomentum_AP']   = ft.AnalyzeFactor('SurpriseMomentum_AP',TD['SurpriseMomentum_AP'] ,TD['ForwardReturns_AP'],NumTile)

    N                       = 5
    TD['Month12ChangeF12MEarningsEstimate_AP']  = D['Month12ChangeF12MEarningsEstimate_AP'].copy()
    TD['Month12ChangeF12MEarningsEstimate_AP']  = td.CleanData(TD['Month12ChangeF12MEarningsEstimate_AP'],N)  #Moderate outliers so model building is better
    TransformList           = ['ZSBT','ZSCSBS']                     #z-score by time, decile crosssection by sector
    NumTile                 = np.int_(5)                            #Number of quantiles to use in AnalyzeFactor
    TD['Month12ChangeF12MEarningsEstimate_AP']  = td.Transform(TD['Month12ChangeF12MEarningsEstimate_AP'],TransformList,D)
    FA['Month12ChangeF12MEarningsEstimate_AP']  = ft.AnalyzeFactor('Month12ChangeF12MEarningsEstimate_AP',TD['Month12ChangeF12MEarningsEstimate_AP'] ,TD['ForwardReturns_AP'],NumTile)
    
    VMalpha_AP          = 1.0*FA['Price_Book_AP']['SignalTile_AP'] + 1.0*FA['STMomentum_AP']['SignalTile_AP']        
    TD['VMalpha_AP']    = VMalpha_AP.copy()
    TransformList       = ['ZSCSBS']
    TD['VMalpha_AP']    = td.Transform(TD['VMalpha_AP'],TransformList,D)
    NumTile             = 5                        #Number of quantiles to use in AnalyzeFactor
    FA['VMalpha_AP']    = ft.AnalyzeFactor('VMalpha',TD['VMalpha_AP'],TD['ForwardReturns_AP'],NumTile)
    NumPointsS2         = 100 #Number of grid points to search, 100 is usually enough
    S2                  = ft.Optimize_IRitp_2(TD['Price_Book_AP'],TD['STMomentum_AP'] ,TD['ForwardReturns_AP'], NumPointsS2)
    NumPointsS3         = 100 #Number of grid points to search, 100 is usually enough
    S3                  = ft.Optimize_IRitp_3(TD['Price_Book_AP'],TD['SurpriseMomentum_AP'],TD['Month12ChangeF12MEarningsEstimate_AP'],TD['ForwardReturns_AP'],NumPointsS3)
#
    r = md.savefile('TD' + SaveFile +'.pkl',TD) 
    r = md.savefile('FA' + SaveFile +'.pkl',FA)
    r = md.savefile('S2' + SaveFile + '.pkl',S2)
    r = md.savefile('S3' + SaveFile + '.pkl',S3)
    
    R               = {}
    R['SaveFile']   = SaveFile
    R['TD']         = TD
    R['FA']         = FA
    R['S2']         = S2
    R['S3']         = S3
    return R



# data = LoadData('All')
# lab_run = Run_Lab(data,'RunNumber_5')
# print(lab_run['FA']['Price_Book_AP']['ICitp'])
# single_test = single_factor_alpha_test("All")

categories = ["All", "High", "Mid", "Low"]
results = []
for dataset in categories:
    res = single_factor_alpha_test(dataset)
    results.append(res)
print(results)


        
    
    


    
    



