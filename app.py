import streamlit as st
import json
import hashlib
import uuid
import datetime

# --------------------------
# Helper Functions
# --------------------------

def generate_did(entity_name):
    return f"did:example:{uuid.uuid4().hex[:8]}:{entity_name.lower().replace(' ', '')}"

def hash_credential(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

# --------------------------
# Classes for DID actors
# --------------------------

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

    def present_proof(self, index=0):
        credential = self.credentials[index]
        return {
            "holder_did": self.did,
            "credential_hash": credential["proof"],
            "selective_disclosure": credential["data"]
        }

class Verifier:
    def _init_(self, name):
        self.name = name
        self.did = generate_did(name)

    def verify_proof(self, proof, known_hash):
        return proof["credential_hash"] == known_hash

# --------------------------
# Streamlit App UI
# --------------------------

st.set_page_config(page_title="DID Credential Simulation", layout="wide")

st.title("🔐 Decentralized Identity (DID) Simulation")
st.markdown("Simulate how credentials are issued, held, and verified in a decentralized identity system.")

st.divider()

# Input Fields
issuer_name = st.text_input("🔵 Issuer Name", "University of ABC")
holder_name = st.text_input("🟢 Holder Name", "Alice Johnson")
verifier_name = st.text_input("🟣 Verifier Name", "Company XYZ")

st.subheader("📄 Credential Details")
col1, col2, col3 = st.columns(3)
with col1:
    name = st.text_input("Name", "Alice Johnson")
with col2:
    degree = st.text_input("Degree", "Bachelor of Science")
with col3:
    year = st.text_input("Year", "2024")

# Process Flow
if st.button("🚀 Simulate Credential Flow"):
    issuer = Issuer(issuer_name)
    holder = Holder(holder_name)
    verifier = Verifier(verifier_name)

    # Step 1: Issuer issues credential
    credential_data = {
        "name": name,
        "degree": degree,
        "year": year
    }
    issued_cred = issuer.issue_credential(holder.did, credential_data)

    # Step 2: Holder receives and stores it
    holder.receive_credential(issued_cred)

    # Step 3: Holder presents proof
    proof = holder.present_proof()

    # Step 4: Verifier validates
    is_valid = verifier.verify_proof(proof, issued_cred["proof"])

    # Display Results
    st.success("✅ Credential Successfully Issued")
    with st.expander("🔹 Issued Credential (JSON)"):
        st.json(issued_cred)

    st.success("✅ Proof Presented by Holder")
    with st.expander("🔸 Proof Presented (JSON)"):
        st.json(proof)

    st.success("✅ Verifier Verification Result")
    st.markdown(f"### ✅ Proof is *{'VALID' if is_valid else 'INVALID'}*")

    st.info(f"Issuer DID: {issuer.did}")
    st.info(f"Holder DID: {holder.did}")
    st.info(f"Verifier DID: {verifier.did}")

st.caption("Simulation powered by Streamlit · Built for educational purposes.")