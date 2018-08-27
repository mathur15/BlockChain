#General blockchain
#Crypto is for adding transaction based on the blockchain technology

#Module 1-Create Blockchain
#use different POST requests to edit transactions
#proof of work is the problem that miners solve
#number which is hard to find but easy to verify by other miners

import datetime   #timestamp
import hashlib    #hash the block
import json    #make json objects
from flask import Flask,jsonify -->  #return the messages from postman


#Building the Blockchain

class Blockchain:
	def __init__(self):
		self.chain = [] #list of blocks
		self.create_block(proof=1,previous_hash='0') #Genesis block
	def create_block(self,proof,previous_hash):
		block={'index':len(self.chain)+1,
		'timestamp':str(datetime.datetime.now()),
		'proof': proof,
		'previous_hash':previous_hash}

		self.chain.append(block)

		return block

		#index,timestamp,proof,previous_hash

	def get_previous_block(self):
		return self.chain[-1]

	def proof_of_work(self,previous_proof):
		new_proof=1 #increment the proof at each iteration
		check_proof=False#turn to true when done
		while check_proof is False:
			#define the problem miners have to solve using the SHA256 with 4 leading 0's
			#generate hash every iteration
			hash_operation=hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest() #non symmetrical
			#add a b before the start of the hash
			#check if the first four characters are 0's
			if hash_operation[0:4] == '0000':#miner wins
				check_proof=True
			else
				new_proof+=1
		return new_proof


	#generate the SHA256 hash for a block
	def hash(self,block):
		encoded_block=json.dumps(block,sort_keys=True).encode() #format for the SHA256
		#convert the json to string
		return hashlib.sha256(encdoded_block).hexdigest()

    #verify if everything is right in the blockchain
	  #-check if each block has right proof of work
	  #-prev hash is the has of the previous block
	def is_chain_valid(self,chain):
		#loop through blocks
		previous_block=chain[0]
		block_index=1
		while block_index < len(chain):
			block=chain[block_index]
			if block['previous_hash'] != self.hash(previous_block):
				return False
			previous_proof= previous_block['proof'] 
			proof=block['proof']
			hash_operation=hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest() #non symmetrical
			if hash_operation[:4] !='0000':
				return False
			previous_block=block
			block_index+=1
		return True

#Mining the blockchain











	



		



#Mining the Blockchain



