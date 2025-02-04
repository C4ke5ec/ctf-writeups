__author__ = 'cdumitru'

import sys
from Crypto.Cipher import ARC4
import numpy
import string
import itertools
from multiprocessing import Pool
from time import time
import cProfile


#ALPHABET = string.digits
ALPHABET = string.ascii_lowercase
#ALPHABET = string.ascii_uppercase
#ALPHABET = string.letters + string.digits
#ALPHABET = string.letters + string.digits + string.punctuation
#ALPHABET = string.printable

KEY_LENGTH = 4
FILE_NAME = "decode5_raw.txt"
CPU_COUNT= 1


def gen():
    """
    Iterates through the alphabet one letter at a time
    """
    for i in ALPHABET:
        yield tuple([i])


def check(key, data):
    """
    Decrypts the data with the given key and checks the entropy
    """

    decr = ARC4.new(key).decrypt(data)

    #compute for the decrypted data block

    #interpret decrypted data as an int array
    int_array = numpy.frombuffer(decr, dtype=numpy.uint8)
    count = numpy.bincount(int_array)
    #compute probability for each int value
    prob = count/float(numpy.sum(count))
    #thow away zero values
    prob = prob [numpy.nonzero(prob)]
    #Shannon entropy
    entropy = -sum(prob * numpy.log2(prob))

    #if this doesn't look like a random stream then jackpot
    if entropy < 7.9:
        print('Key: {0}, Entropy: {1}'.format(key, entropy))



def worker(base):
    #read 64KB from the file
    data = open(FILE_NAME, 'rb').read(2**16)

    #generate all the strings of KEY_LENGTH length and check them

    #We know prior that the key starts with a. Remove the next two lines for generic behavior
    if string.ascii_lowercase in ALPHABET:
        base = tuple(['a']) + base

    for i in itertools.product(ALPHABET, repeat=KEY_LENGTH-len(base)):
        check(''.join(base + i), data)




def parallel():
    """
    Starts a number of threads that search through the key space
    """
    p = Pool(CPU_COUNT)
    p.map(worker, gen(), chunksize=2)
    p.close()
    p.join()

def serial():
    worker(tuple())


if __name__ == "__main__":
    serial()