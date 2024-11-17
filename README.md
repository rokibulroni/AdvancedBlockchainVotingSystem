
# Advanced Blockchain-Based Voting System

This is a secure and decentralized voting system built on blockchain. It includes features such as user authentication, vote validation, and mining.

## Features
- **Blockchain**: A robust implementation for decentralized voting.
- **Authentication**: Voter authentication using JWT.
- **Vote Validation**: Ensures a voter can vote only once per election.
- **REST API**: Use HTTP endpoints for interaction.

## Requirements
- Python 3.7 or later
- Flask: `pip install flask`
- PyJWT: `pip install pyjwt`

## How to Run
1. Clone the repository.
2. Install the dependencies using `pip install -r requirements.txt`.
3. Run the application: `python app.py`.

## Endpoints
1. **Register Voter**: `POST /register`
   - Request body: `{ "voter_id": "1234" }`
2. **Cast a Vote**: `POST /vote`
   - Request body: `{ "token": "<JWT_TOKEN>", "candidate": "Alice" }`
3. **Mine a Block**: `GET /mine`
4. **Get Blockchain**: `GET /chain`

## Example Usage
1. Register a voter:
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"voter_id":"1234"}' http://localhost:5000/register
   ```
2. Cast a vote:
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"token":"<TOKEN>", "candidate":"Alice"}' http://localhost:5000/vote
   ```
3. Mine a block:
   ```bash
   curl http://localhost:5000/mine
   ```
4. Retrieve the blockchain:
   ```bash
   curl http://localhost:5000/chain
   ```

## License
MIT License
