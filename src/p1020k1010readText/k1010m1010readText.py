'''
Created on 18 Dec 2017

@author: bogdan
'''
import sys, os, re
import pathlib



class clFile2Str(object):
    '''
    this class converts a file into a string for a more systematic processing 
    '''
    def __init__(self, SFileIn=sys.argv[1]):
        self.SContent = ''
        try:
            self.SContent = pathlib.Path(SFileIn).read_text()
        except:
            pass
        
    def getData(self):
        return self.SContent
    
    def printData(self):
        print(self.SContent)
        return


class clReadTMX(object):
    '''
    readsTMX file / string and outputs one-line per-sentence output 
    '''


    def __init__(self, STmxIn):
        '''
        Constructor
        '''
        
        print(STmxIn)
        

if __name__ == '__main__':
    OFile2Str = clFile2Str(sys.argv[1])
    STmxIn = OFile2Str.getData()
    OReadTMX = clReadTMX(STmxIn)
    pass
    