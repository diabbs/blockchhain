#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 11:47:11 2021

@author: diaby
"""
from flask import Flask, jsonify, request
from uuid import uuid4

from diabycoin import Blockchain
#Creating a web app
app = Flask(__name__)
 
#creating an address for the node on Port 5000
node_address = str(uuid4()).replace('-','')      


#Creating a Blockchain
blockchain = Blockchain()

#Mining new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender = node_address, receiver = 'DIABY', amount = 10)
    block = blockchain.create_block(proof, previous_hash)
    response = {
                'message' : 'Congratulation, you mine the block',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash'],
                'transactions': block['transactions']
                }
    return jsonify(response), 200

#Getting the fully Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {
                'chain' : blockchain.chain, 
                'length' : len(blockchain.chain)
               }
    return jsonify(response), 200

#Check the block is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
     is_valid = blockchain.is_chain_valid(blockchain.chain)
     if is_valid:
         response = {'message' : 'All good. The blockchain is valid.'}
     else:
         response = {'message' : 'We have the problème, the blockchain is not valid.'}
     return jsonify(response), 200
 
# Add a new transacion to the blockchain
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all (key in json for key in transaction_keys):
        return 'Some elements of the transaction are missed', 400
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
    response = {'message' : f'This transacton will be added to block{index}'}
    return jsonify(response), 201

 
#Parti 3 : Decentralizing our blockchain

#Connecting new nodes
@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {
                'message' : 'All the nodes are connected, the Diabycoin Blockchain now contains the follow nodes :',
                'total_nodes' : list(blockchain.nodes)
               }
    return jsonify(response), 201

#Replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
     is_chain_replaced = blockchain.replace_chain()
     if is_chain_replaced:
         response = {
                     'message' : 'The nodes had different chains so the chain was replaced by the longest one.',
                     'new_chain' : blockchain.chain
                    }
     else:
         response = {
                     'message' : 'All good, the chain is the largest one.',
                     'actual_chain' : blockchain.chain
                    }
     return jsonify(response), 200
     


#Running the app
app.run(host='127.0.0.1',port=5001,debug=True)
