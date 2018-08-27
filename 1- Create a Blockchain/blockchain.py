#General blockchain
#Crypto is for adding transaction based on the blockchain technology

#Module 1-Create Blockchain
#use different POST requests to edit transactions

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
	



		



#Mining the Blockchain



