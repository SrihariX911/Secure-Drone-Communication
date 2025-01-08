**Secure Drone Communication**

Welcome to the Secure Drone Communication project! This repository showcases a robust implementation of a secure communication system for drones using advanced cryptographic techniques. The project leverages the NTRU cryptosystem, which is known for its efficiency and resistance to quantum attacks.

**Features**

NTRU-based Cryptography: Implements the NTRU public-key cryptosystem for secure data exchange.
Dynamic Messaging: Supports encryption and decryption of user-provided messages.
Polynomial Operations: Includes polynomial arithmetic for key generation and encryption.
Scalability: Suitable for secure communication in Internet of Drones (IoD) networks.
Python-based: Fully implemented in Python for easy integration and extensibility.


**How It Works**

**Key Generation:**

Bob generates a public-private key pair using small and large primes.
The public key is shared with Alice for message encryption.

**Message Encryption:**

Alice encrypts her message using Bob's public key and a random polynomial.
The encrypted message is sent to Bob.

**Message Decryption:**

Bob decrypts the received message using his private key.

**Polynomial Arithmetic:**

Utilizes advanced polynomial operations for secure encoding and decoding.


**Setup Instructions**

Prerequisites
Python 3.8+
numpy library for polynomial operations
Optional: Install any virtual environment tool like venv or conda.

Installation

Clone the repository:

git clone https://github.com/SrihariX911/Secure-Drone-Communication.git

cd Secure-Drone-Communication

Install dependencies:

pip install numpy

Run the program:

python main.py

**Usage**

Start the program and follow the prompts.
Provide the degree, small prime, and large prime values for key generation.
Input a message (string or a list of numbers) for encryption.
Observe the encrypted message and its successful decryption.
