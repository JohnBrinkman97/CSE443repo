# code shell adapted from https://en.bitcoin.it/wiki/Block_hashing_algorithm
#  by Steve Cole for cse433s Spring 2019

# NAME: John Brinkman

# Fill in the code sections marked # YOUR CODE HERE . You may use any of the
#  utility functions contained in this file to help you.

import hashlib
import time

### UTILITY FUNCTIONS ###

def switchEndian(hexString):
    '''
    Takes in a string representing hex-encoded bytes (2 chars per byte)
    and returns a copy of the string with the byte ordering reversed.
    Example: converts 'a1b2c3d4' to 'd4c3b2a1' .

    @param hexString The hex-string-encoded number to be reversed
    @return A bytewise-reversed copy of hexString
    '''
    hexVal = hexString.decode('hex')
    rev = hexVal[::-1].encode('hex_codec')
    return rev

def int2LittleEndian(n):
    '''
    Converts a 4-byte integer value to a hex-encoded string (2 chars per byte)
      in Little Endian order.
    Pads with zeroes if less than 8 chars.
    Example: converts 26 to '1a000000'

    @param n Integer to be converted
    @return Little Endian hex string version of integer
    '''
    return switchEndian('{:08x}'.format(n)) 

def qq2hexStr(t):
    '''
    Takes 32-byte numerical value ("quad quad") and returns it encoded as 
      a hex-encoded string with 2 chars per byte.
    Example: takes in 33 and returns '00000..21' (64 chars total).
    Useful for printing threshold as a string.
    '''
    return '{:064x}'.format(t)

def extractThreshold(bits):
    '''
    Extracts a numerical threshold from the 'bits' field of a Bitcoin block.
    Note: 'bits' field is assumed to be a string in Little Endian order 
      (as it's shown in the Blockchain viewer for Bitcoin).

    @param bits 'bits' field of a Bitcoin block
    @return Numerical threshold encoded in the 'bits' field
    '''
    # convert hex string and reverse
    bitsNum = bits.decode('hex')[::-1].encode('hex_codec')  
    bitsNum = int(bitsNum, 16) 

    # extract threshold from 4-byte 'bits' field
    # exponent: MSB
    # mantissa: 3 remaining bytes 
    # threshold = mantissa * 2**(8*(exponent-3))
    e = bitsNum >> 24
    m = bitsNum & 0xFFFFFF
    t = m * (1 << (8 * (e - 3)))

    return t


### CORE FUNCTIONS ###

def hashBlock(version, prevHash, merkleRoot, ts, bits, nonce):
    '''
    Computes the hash value for a Bitcoin block with the given parameters.
    See https://en.bitcoin.it/wiki/Block_hashing_algorithm for details
      on the Bitcoin hash algorithm.
    Note that parameters must be in Little Endian format.

    @param version Bitcoin version
    @param prevHash Hash of previous block 
    @param merkleRoot Root of Merkle tree for the block 
    @param ts Timestamp
    @param bits 'bits' field of block; encodes threshold below which hash value must be
    @param nonce 4-byte value that causes hash to be below threshold extracted from bits
    @return String representing Big Endian hex encoding of hash value
    '''
    # Hint: Don't forget the return value.
    # YOUR CODE HERE
    header_hex = version+prevHash+merkleRoot+ts+bits+nonce
    
    header_bin = header_hex.decode('hex')
    hash = hashlib.sha256(hashlib.sha256(header_bin).digest()).digest()
    hash.encode('hex_codec')
    #print(hash[::-1].encode('hex_codec'))
    return hash[::-1].encode('hex_codec')

def mineBlock(version, prevHash, merkleRoot, ts, bits):
    '''
    Computes a 4-byte nonce value that will yield a valid Bitcoin block given 
      the other header values passed as parameters.
    See https://en.bitcoin.it/wiki/Block_hashing_algorithm for details
      on the Bitcoin hash algorithm.
    Note that parameters must be in Little Endian format.
    
    @param version: Bitcoin version
    @param prevHash: Hash of previous block 
    @param merkleRoot: root of Merkle tree for the block 
    @param ts: timestamp
    @param bits: Bits field of block; encodes threshold below which hash value must be
    
    @return nonce value
    '''
    # extract threshold from bits
    # YOUR CODE HERE
    threshold = extractThreshold(bits)
    # mining loop 
    # Hints to make problem tractable: 
    #   1. The solution nonce is between 0x60000000 and 0x70000000.
    #   2. To iterate through a range of indices, use the xrange() 
    #      function rather than the range() function to avoid running
    #      out of memory.
    # YOUR CODE HERE
    # for ... 
    for i in xrange(0x60000000,0x70000000):
        # convert nonce to Little Endian hex-encoded string
        # YOUR CODE HERE
        littleEndianNonce = int2LittleEndian(i)
        # get hash value of block using this nonce
        # YOUR CODE HERE
        hashVal = hashBlock(version,prevHash,merkleRoot,ts,bits,littleEndianNonce)
        # convert hash value to numeric val
        # YOUR CODE HERE (use following template, plug in correct variable name--
        #  hashStr is hash value from previous step)
        # hashNum = int(hashStr, 16)
        hashNum = int(hashVal,16)
        # test for success; print or return nonce, hash, and threshold upon success
        # NB: You can print the threshold with statement: 
        #   'print qq2hexStr(threshold)'
        # Hint: don't forget the return value.
        # YOUR CODE HERE
        if hashNum < threshold:
            print("Int nonce: " + str(i))
            print("Little Endian nonce: " + str(int2LittleEndian(i)))
            print("Hash value: " + str(hashVal))
            print("Hash Number: " + str(hashNum))
            print qq2hexStr(threshold)
            return 

if __name__ == "__main__":
    # main function: set up block parameters and call hashBlock or mineBlock
    # YOUR CODE HERE
    start = time.time()
    version = '01000000'
    # previousHash = '1dbd981fe6985776b644b173a4d0385ddc1aa2a829688d1e0000000000000000'
    # merkleHashRoot = 'b371c14921b20c2895ed76545c116e0ad70167c5c4952ca201f5d544a26efb53'
    # timeStamp = 'b4f6d74d'
    # bits = 'f2b9441a'
    # nonce = '071a0c81'
    #print(hashBlock(version,previousHash,merkleHashRoot,timeStamp,bits,nonce))

    previousHash = 'd44b8a28a4bc90c5e94acb3ffff8f710d42d085d39c9f349a42c000000000000'
    merkleHashRoot = '1673404d0ff0a7a605811d5b84e7fb63b84ce0f0f28b91bf8d94304ec1f0f518'
    timeStamp = '264bd44d'
    bits = 'f2b9441a'
    mineBlock(version,previousHash,merkleHashRoot,timeStamp,bits)
    end = time.time()
    print(end-start)