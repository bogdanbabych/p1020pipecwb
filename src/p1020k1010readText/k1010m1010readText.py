'''
Created on 18 Dec 2017

@author: bogdan
'''
import sys, os, re
import pathlib



class clFile2Str(object):
    '''
    this class converts a file into a string for a more systematic processing 
    printing warning that no file was found 
    '''
    def __init__(self, SFileIn=sys.argv[1]):
        self.SContent = ''
        try:
            self.SContent = pathlib.Path(SFileIn).read_text()
        except:
            print("WARNING: file not found!!!")
        
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
    STmxIn = pathlib.Path(sys.argv[1]).read_text()
    OReadTMX = clReadTMX(STmxIn)
    pass
    