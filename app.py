from flask import Flask, render_template, request, send_file
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
import os

app = Flask(__name__)

key_file = 'key.pem'

def generate_or_load_key():
    if not os.path.exists(key_file):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        with open(key_file, 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

        return private_key
    else:
        try:
            with open(key_file, 'rb') as f:
                return serialization.load_pem_private_key(
                    f.read(),
                    password=None,
                    backend=default_backend()
                )
        except Exception as e:
            print("Error loading private key:", e)
            print("Generating new key pair...")
            os.remove(key_file)
            return generate_or_load_key()

private_key = generate_or_load_key()
public_key = private_key.public_key()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sign', methods=['POST'])
def sign():
    if request.method == 'POST':
        file = request.files['file']
        data = file.read()
        signature = private_key.sign(
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        with open('signed_file.txt', 'wb') as f:
            f.write(data)
            f.write(signature)

        return send_file('signed_file.txt', as_attachment=True)

@app.route('/verify', methods=['POST'])
def verify():
    if request.method == 'POST':
        file = request.files['file']
        data = file.read()
        signature = data[-256:]
        data = data[:-256]

        try:
            public_key.verify(
                signature,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return "Signature verified successfully!"
        except Exception as e:
            return "Signature verification failed: " + str(e)

if __name__ == '__main__':
    app.run(debug=True)
