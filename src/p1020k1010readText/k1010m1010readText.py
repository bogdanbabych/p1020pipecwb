'''
Created on 18 Dec 2017

@author: bogdan
'''
import sys, os, re
import pathlib


class clReadTMX(object):
    '''
    readsTMX file / string and outputs one-line per-sentence output 
    '''


    def __init__(self, STmxIn):
        '''
        Constructor
        '''
        
        print("output\n", STmxIn)
        

if __name__ == '__main__':
    STmxIn = pathlib.Path(sys.argv[1]).read_text()
    OReadTMX = clReadTMX(STmxIn)
    pass
    