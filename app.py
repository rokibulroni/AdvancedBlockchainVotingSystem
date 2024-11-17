
import hashlib
import json
from time import time
from flask import Flask, jsonify, request, abort
import jwt
import datetime

SECRET_KEY = "your_secret_key"

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_votes = []
        self.voters = {}  # Simulate a database for voters
        self.create_block(previous_hash='1', proof=100)

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'votes': self.current_votes,
            'proof': proof,
            'previous_hash': previous_hash,
        }
        self.current_votes = []
        self.chain.append(block)
        return block

    def get_last_block(self):
        return self.chain[-1]

    def add_vote(self, voter_id, candidate):
        self.current_votes.append({'voter_id': voter_id, 'candidate': candidate})

    def proof_of_work(self, last_proof):
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    def valid_proof(self, last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def hash(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def register_voter(self, voter_id):
        if voter_id in self.voters:
            return False
        self.voters[voter_id] = False  # False means the voter hasn't voted yet
        return True

    def validate_vote(self, voter_id):
        return voter_id in self.voters and not self.voters[voter_id]

    def mark_voted(self, voter_id):
        if voter_id in self.voters:
            self.voters[voter_id] = True

blockchain = Blockchain()
app = Flask(__name__)

# Authentication and JWT
def authenticate_user(voter_id):
    token = jwt.encode({'voter_id': voter_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, SECRET_KEY, algorithm='HS256')
    return token

def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except:
        return None

@app.route('/register', methods=['POST'])
def register_voter():
    data = request.get_json()
    voter_id = data.get('voter_id')
    if not voter_id:
        return jsonify({'message': 'Voter ID is required'}), 400

    if blockchain.register_voter(voter_id):
        token = authenticate_user(voter_id)
        return jsonify({'message': 'Voter registered successfully', 'token': token}), 201
    else:
        return jsonify({'message': 'Voter already registered'}), 400

@app.route('/vote', methods=['POST'])
def cast_vote():
    data = request.get_json()
    token = data.get('token')
    candidate = data.get('candidate')

    if not token or not candidate:
        return jsonify({'message': 'Token and candidate are required'}), 400

    decoded = decode_token(token)
    if not decoded:
        return jsonify({'message': 'Invalid or expired token'}), 401

    voter_id = decoded['voter_id']
    if blockchain.validate_vote(voter_id):
        blockchain.add_vote(voter_id, candidate)
        blockchain.mark_voted(voter_id)
        return jsonify({'message': 'Vote successfully added'}), 201
    else:
        return jsonify({'message': 'Voter has already voted or is not registered'}), 403

@app.route('/mine', methods=['GET'])
def mine_block():
    last_block = blockchain.get_last_block()
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    previous_hash = blockchain.hash(last_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': 'New block mined',
        'index': block['index'],
        'votes': block['votes'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
