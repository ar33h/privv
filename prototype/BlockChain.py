# Privv - Truly Private Messaging (Python Prototype) | PBL II 

import datetime
import hashlib

# Coloured Terminal Text
from colorama import init
init()
from colorama import Fore, Back, Style

class Block:

    # Each block has 7 attributes 

    #1 Block Number
    blockNo = 0

    #2 Data stored in this block
    data = None 

    #3 Pointer to next block
    next = None

    #4 The hash of this block (serves as a unique ID)
    hash = None
    
    #5 Number only used once  
    nonce = 0

    #6 Store the hash ID of previous block in the chain
    previous_hash = 0x0

    #7 Timestamp 
    timestamp = datetime.datetime.now()


    # Initialize a block by storing some data
    def __init__(self, data):
        self.data = data

    
    # If someone changes the hash of a block every block that comes after it is changed
    # This helps make a blockchain immutable

    #Method to compute 'hash' of a block
    def hash(self):

        # SHA-256 hashing algorithm 
        h = hashlib.sha256()

        # This algorithm takes 5 attributes
        h.update(
        str(self.nonce).encode('utf-8') +
        str(self.data).encode('utf-8') +
        str(self.previous_hash).encode('utf-8') +
        str(self.timestamp).encode('utf-8') +
        str(self.blockNo).encode('utf-8')
        )

        # Returns a hexadecimal string
        return h.hexdigest()


    def __str__(self):

        # Print out the value of a block
        return "Block Hash: " + str(self.hash()) + "\nPreviousHash: " + str(self.previous_hash) + "\nBlockNo: " + str(self.blockNo) + "\nBlock Data: " + str(self.data) + "\nHashes: " + str(self.nonce) + "\n--------------"
        
        
class Blockchain:
    
    # Mining difficulty 
    diff = 10

    # Maximum we can store in a 32-bit number
    maxNonce = 2**32

    # Target hash for mining
    target = 2 ** (256-diff)

    # Genesis block - first block in blockchain
    block = Block("Genesis")

    # Sets it as the head
    head = block

    # Add block to Blockchain
    def add(self, block):

        block.previous_hash = self.block.hash()

        block.blockNo = self.block.blockNo + 1

        self.block.next = block
        self.block = self.block.next


    # Determines whether or not we can add a given block
    def mine(self, block):
        
        for n in range(self.maxNonce):
           
            if int(block.hash(), 16) <= self.target:
                self.add(block)
                print("Add Block")
                print(block)
                break

            else:
                block.nonce += 1
    


# If someone edits a block 
def editBlock(blockchain,genesisBlock,index):

    i=0
    for x in range(index):
        blockchain.head = blockchain.head.next
        i += 1

    print(" - Editing Block No. "+str(i))
    blockchain.head.data = "Edited"

    # Check if block have edited
    blockchain.head = genesisBlock
    temp = genesisBlock

    # Print out each block in the blockchain
    while blockchain.head.next != None:

        if(blockchain.head.hash() != blockchain.head.next.previous_hash):
            print("...Block No. " +  str(blockchain.head.blockNo) + " has been edited...")
            print("=========Show Edited==========")
            print(str(temp))
            print(str(blockchain.head))
            print(str(blockchain.head.next))
            print("=========End Edited=========")
            
        temp = blockchain.head
        blockchain.head = blockchain.head.next
