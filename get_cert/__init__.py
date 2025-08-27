import json
import ssl
import socket
from datetime import datetime
import azure.functions as func

def get_ssl_info(domain):
    ctx = ssl.create_default_context()
    with socket.create_connection((domain, 443), timeout=5) as sock:
        with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
            cert = ssock.getpeercert()
            valid_from = datetime.strptime(cert['notBefore'], "%b %d %H:%M:%S %Y %Z")
            valid_to = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
            days_remaining = (valid_to - datetime.utcnow()).days
            return {
                "domain": domain,
                "cn": dict(x[0] for x in cert['subject'])['commonName'],
                "valid_from": valid_from.strftime("%Y-%m-%d %H:%M:%S"),
                "valid_to": valid_to.strftime("%Y-%m-%d %H:%M:%S"),
                "days_remaining": days_remaining
            }

def main(req: func.HttpRequest) -> func.HttpResponse:
    domain_param = req.params.get('domain')
    if not domain_param:
        return func.HttpResponse(
            json.dumps({"error": "Missing domain parameter"}),
            mimetype="application/json",
            status_code=400
        )

    domains = [d.strip() for d in domain_param.split(",") if d.strip()]
    results = []

    for domain in domains:
        try:
            results.append(get_ssl_info(domain))
        except Exception as e:
            results.append({
                "domain": domain,
                "cn": None,
                "valid_from": None,
                "valid_to": None,
                "days_remaining": None,
                "error": str(e)
            })

    return func.HttpResponse(
        json.dumps(results, indent=2),
        mimetype="application/json",
        status_code=200
    )
