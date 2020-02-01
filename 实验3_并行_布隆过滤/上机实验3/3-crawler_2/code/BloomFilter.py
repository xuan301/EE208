from Bitarray import Bitarray
from GeneralHashFunctions import *

class BloomFilter(set):
    def __init__(self,size,hash_num):
        super(BloomFilter,self).__init__()
        self.bitarray = Bitarray(size)
        self.size = size
        self.hash_num = hash_num

    def __len__(self):
        return self.size

    def __iter__(self):
        return iter(self.bitarray)

    def add(self,item):
        for