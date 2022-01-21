#Create a cryptocurrency
"""
Created on Thu Dec 23 21:53:58 2021

@author: diaby
"""

#Module 2 - create cryptocurrency -- diabycoin

#Importing the librairie

import json
import datetime
import hashlib
import requests #Request decentralize

from urllib.parse import urlparse

#Party 1 -  Build the blockchain
class Blockchain:
    
    def __init__(self):
        self.chain = [] # list of chain
        self.transactions = [] # list of transaction
        self.create_block(proof = 1, previous_hash ='0') # Genesis block
        self.nodes = set()
    
    # Create new block
    def create_block(self, proof, previous_hash):
        block = {
                  'index': len(self.chain)+1, 
                  'timestamp':str(datetime.datetime.now()),
                  'proof': proof,
                  'previous_hash':previous_hash,
                  'transactions' : self.transactions
                }
        self.transactions = []
        self.chain.append(block)
        return block
    
    #Get previous block
    def get_previous_block(self):
        return self.chain[-1]
    
    # proof of work
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 + previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    #hash function
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    #Verify the chain is valid
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 + previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    
    # Add tansaction in blockchain
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append(
                    {
                        'sender' : sender,
                        'receiver' : receiver,
                        'amount' : amount
                    }
                )
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    
    #Add node method for decentralization
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
    
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
            if longest_chain:
                self.chain = longest_chain
                return True
            return False
