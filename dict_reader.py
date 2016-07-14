#hypy Evan Racah and Thorsten Kurth
import numpy as np
import math



def choose_params(param_range_dic):
    '''Chooses params
    Takes dictionary param names and ranges and returns dictionary with param names and single values
    Args:
        param_range_dic (dict): dictionary of param names and ranges
            key (string): the name of the parameter as it is called in user;s train fxn
            value (list or dict) : list or dict specifying distribution of possible values
                    list: sequence of values (uniform dist assumed)
                    dictionary: specifies either high, low, step or
                                parameters for a probability distribution'''
    param_dic = {}
    for k,v in param_range_dic.iteritems():
        if type(v) is list:
            param_dic[k] = np.random.choice(v)
        elif type(v) is dict:
            param_dic[k] = parse_dic(v)
            
    return param_dic
            
        



def parse_dic(dic):
    #TODO: add doc string
    if 'low' in dic and 'high' in dic:
        return choose_val_from_sequence(dic)
    else:
        return choose_val_from_prob_dist(dic)



def choose_val_from_sequence(dic):
    #TODO: add doc string
    low = dic['low']
    high = dic['high']
    step_type = 'discrete' if 'step_type' not in dic else dic['step_type']
    
    if step_type == 'discrete':
        step_size = 1 if 'step_size' not in dic else dic['step_size']
        seq = np.arange(low,high, step_size)
        val = np.random.choice(seq)
    
    elif 'log' in step_type:
        val = parse_log_fxn(dic)
   
    
    elif step_type == 'continuous':
        pass
        
        
        
        
    return val



def parse_log_fxn(dic):
    #TODO: add doc string
    #extract the base from the string log<base>
    base = int(dic['step_type'].split('log')[1])

    step_size = 1 #by default
    low = dic['low']
    high = dic['high']
    
    # take the log to get the power
    #todo: make sure these are powers of the base
    low = math.log(low, base)
    high = math.log(high, base)
    
    #create sequence of exponents, then uniformly choose from them
    seq = np.arange(low, high, step_size)
    exponent = np.random.choice(seq)
    
    #convert exponent back to power
    exponent = base**exponent
    
    
    return exponent



def choose_val_from_prob_dist(dic):
    '''Takes in description of prob dist and takes a sample from the dist
      Args:
            dic (dict): Contains these keys:
                       params (dict): contains param, value pairs for the keyword arguments in the fxn function
                       fxn (function): a python function that takes params 
                           keyword arguments and returns a value or values '''
    
    params = dic['params']
    func = dic['fxn']
    return func(**params)
    



if __name__ == "__main__":
    sample_dictionary = {'k': [1,5,7,9], #list example
                        'low_high_int': {'low': 1, 'high':10, 'step_type': 'discrete', 'step_size': 2, 'sample': 'uniform'},
     
                        #make sample uniform default,  discrete default, step_size of one default
                        #'low_high_float' : {'low': 1.0, 'high':10.0, 'step_type': 'continuous', 'sample': 'uniform'},
    
                        'nonuniform_sample' : { 'params': {'loc': 0.0, 'scale': 1.0}, 'fxn': np.random.normal},
                        'non_standard_step' : {'low': 0.001, 'high': 1.0, 'step_type': 'log10' },
                        'string_setting': ['relu', 'leakyrelu', 'elu', 'tanh'],
                        'layers_example' : {'low': 64, 'high':4096, 'step_type': 'log2'},
                        #'generator_example' : {'fxn': np.random.binomial, 'params': {'n': 5, 'p': 0.3, 'size': 1} },
    
    
                        }
    print choose_params(sample_dictionary)









