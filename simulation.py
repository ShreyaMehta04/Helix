import json
import hashlib
import uuid
import datetime

# ------------------------------
# Helper Functions
# ------------------------------

def generate_did(entity_name):
    """Simulate a Decentralized Identifier (DID)"""
    return f"did:example:{uuid.uuid4().hex[:8]}:{entity_name.lower().replace(' ', '')}"

def hash_credential(data):
    """Create a hash of the credential data to simulate ZKP"""
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

# ------------------------------
# Actors
# ------------------------------

class Issuer:
    def _init_(self, name):
        self.name = name
        self.did = generate_did(name)

    def issue_credential(self, holder_did, credential_data):
        credential = {
            "issuer": self.did,
            "holder": holder_did,
            "type": "VerifiableCredential",
            "data": credential_data,
            "issued_at": str(datetime.datetime.utcnow()),
        }
        credential["proof"] = hash_credential(credential)
        return credential

class Holder:
    def _init_(self, name):
        self.name = name
        self.did = generate_did(name)
        self.credentials = []

    def receive_credential(self, credential):
        self.credentials.append(credential)

    def present_proof(self, verifier, credential_index=0):
        credential = self.credentials[credential_index]
        proof = {
            "holder_did": self.did,
            "credential_hash": credential["proof"],
            "selective_disclosure": credential["data"]  # Simulated partial reveal
        }
        return proof

class Verifier:
    def _init_(self, name):
        self.name = name
        self.did = generate_did(name)

    def verify_proof(self, proof, known_credential_hash):
        return proof["credential_hash"] == known_credential_hash

# ------------------------------
# Simulation Flow
# ------------------------------

# Setup
issuer = Issuer("University of ABC")
holder = Holder("Alice Johnson")
verifier = Verifier("Company XYZ")

# Step 1: Issuer issues a credential to the holder
credential_data = {
    "name": "Alice Johnson",
    "degree": "Bachelor of Science",
    "year": "2024"
}
credential = issuer.issue_credential(holder.did, credential_data)
holder.receive_credential(credential)

# Step 2: Holder presents proof to verifier
proof = holder.present_proof(verifier)

# Step 3: Verifier verifies the proof
is_valid = verifier.verify_proof(proof, credential["proof"])

# Output
print("=== Credential Issued ===")
print(json.dumps(credential, indent=2))

print("\n=== Proof Presented ===")
print(json.dumps(proof, indent=2))

print("\n✅ Verification Result:", "VALID" if is_valid else "INVALID")