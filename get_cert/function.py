import ssl
import socket
import sys
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

def get_cert_info(hostname, port=443):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            der_cert = ssock.getpeercert(binary_form=True)
    
    cert = x509.load_der_x509_certificate(der_cert, default_backend())
    
    with open("cert.pem", "wb") as f:
        f.write(cert.public_bytes(encoding=serialization.Encoding.PEM))
    
    subject = cert.subject.rfc4514_string()
    not_before = cert.not_valid_before.strftime("%H:%M %d-%m-%Y")
    not_after = cert.not_valid_after.strftime("%H:%M %d-%m-%Y")

    return {
        "subject": subject,
        "not_before": not_before,
        "not_after": not_after
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 function.py <domain>")
        sys.exit(1)

    hostname = sys.argv[1]
    info = get_cert_info(hostname)
    print(f"Domain: {hostname}")
    print(f"Subject: {info['subject']}")
    print(f"Valid From: {info['not_before']}")
    print(f"Valid To: {info['not_after']}")
