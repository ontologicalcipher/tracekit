import socket

try:
    import dns.resolver
except ImportError:
    dns = None


def resolve(domain):
    domain = domain.strip()

    result = {
        "domain": domain,
        "ip_addresses": [],
        "mx_records": [],
        "ns_records": [],
    }

    # A/IPv4 records
    try:
        result["ip_addresses"] = sorted({
            item[4][0]
            for item in socket.getaddrinfo(domain, 443, socket.AF_INET)
        })
    except socket.gaierror:
        pass

    # DNS records
    if dns is not None:
        for record_type, key in [
            ("MX", "mx_records"),
            ("NS", "ns_records"),
        ]:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                result[key] = sorted(
                    str(answer).rstrip(".") for answer in answers
                )
            except Exception:
                pass

    return result


def print_result(result):
    print()
    print(f"Domain: {result['domain']}")

    print("\n[IP ADDRESSES]")
    for ip in result["ip_addresses"]:
        print(f"  {ip}")

    print("\n[MX RECORDS]")
    for record in result["mx_records"]:
        print(f"  {record}")

    print("\n[NS RECORDS]")
    for record in result["ns_records"]:
        print(f"  {record}")
