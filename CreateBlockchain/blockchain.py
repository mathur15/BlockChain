# A very simple Flask Hello World app for you to get started with...

from flask import Flask,jsonify,request
import datetime   #timestamp
import hashlib    #hash the block
import json    #make json objects
#from flask_cors import CORS

#Building the Blockchain

class Blockchain:
    def __init__(self):
        self.chain = [] #list of blocks
        self.create_block(proof=1,previous_hash='0',content='First Block') #Genesis block
    def create_block(self,proof,previous_hash,content):
        block={'index':len(self.chain)+1,
        'timestamp':str(datetime.datetime.now()),
        'proof': proof,
        'previous_hash':previous_hash,
        'content':content}

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
            #this is just a criteria of sorts of generate a proof of work
            #add a b before the start of the hash
            #check if the first four characters are 0's
            if hash_operation[0:4] == '0000':#miner wins
                check_proof=True
            else:
                new_proof+=1
        return new_proof


    #generate the SHA256 hash for a block
    def hash(self,block):
        encoded_block=json.dumps(block,sort_keys=True).encode() #format for the SHA256
        #convert the json to string
        return hashlib.sha256(encoded_block).hexdigest()

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
            #this was how the proof of works were made
            if hash_operation[:4] !='0000':
                return False
            previous_block=block
            block_index+=1
        return True
def process_request_string(string):
    string_value = string.split("=")
    string = string_value[1].replace("%20",' ')
    string = string_value[1].replace("+",' ')
    return string

app = Flask(__name__)
#CORS(app,resources={r"/*":{"origins":"*"}})
blockchain=Blockchain()
@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/mine_block',methods=['GET','POST'])
def mine_block():
    #Purpose to mine
    #Solve POW based on previous block
    #1- Get previous proof
  if request.method == 'GET':
    previous_block=blockchain.get_previous_block()
    previous_proof=previous_block['proof']
    proof=blockchain.proof_of_work(previous_proof)
    #2-add to blockchain
    previous_hash=blockchain.hash(previous_block)
    content = 'Test message'
    block=blockchain.create_block(proof,previous_hash,content)
    response={'message':'Congratulations you just mined a block!',
    'index':block['index'],
    'timestamp':block['timestamp'],
    'proof':block['proof'],
    'previous_hash':block['previous_hash']
    }
    return jsonify(response),200
  if request.method == 'POST':
    queryString = request.query_string
    queryString = str(queryString,'utf-8')
    queryComponents = queryString.split('&')
    event_string = process_request_string(queryComponents[0])
    quantity_string = process_request_string(queryComponents[1])
    status = process_request_string(queryComponents[2])
    content = {}
    for i in queryComponents:
       string_components = i.split('=')
       if string_components[0] == 'event':
               content['event'] = event_string
       if string_components[0] == 'quantity':
               content['quantity'] = quantity_string
       if string_components[0] == 'Status':
               content['status'] = status
    previous_block=blockchain.get_previous_block()
    previous_proof=previous_block['proof']
    proof=blockchain.proof_of_work(previous_proof)
    #2-add to blockchain
    previous_hash=blockchain.hash(previous_block)
    block=blockchain.create_block(proof,previous_hash,content)
    #print(block)
    return request.query_string

@app.route("/get_chain",methods=['GET'])
def get_chain():
    response={'chain':blockchain.chain,
              'length':len(blockchain.chain)}

    return jsonify(response),200

@app.route("/get_last",methods=['POST'])
def get_last():
    last_block = blockchain.get_previous_block()
    response={'chain':last_block,
              'length':len(blockchain.chain)}

    return jsonify(response),200

#check if blockchain is valid

@app.route('/is_valid_blockchain',methods=['GET'])
def is_valid_blockchain():
    is_valid=blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response={'message':'All Good.'}
    else:
        response={'message': 'We have a problem'}
    return jsonify(response),200
@app.route('/get_length',methods=['POST'])
def get_chain_length():
    response={
        'length':len(blockchain.chain)}
    return jsonify(response),200
app.run(host='0.0.0.0',port=5000)
