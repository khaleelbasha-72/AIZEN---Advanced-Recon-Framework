import requests
import argparse
import time
import whois
import dns.resolver
import socket
import ssl
import builtwith
import json
import os
import re

from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

session = requests.Session()
session.headers.update({"User-Agent": "AIZEN-Recon"})


# ---------------- BANNER ----------------

def banner(domain):

    print(r"""
 █████╗ ██╗███████╗███████╗███╗   ██╗
██╔══██╗██║╚══███╔╝██╔════╝████╗  ██║
███████║██║  ███╔╝ █████╗  ██╔██╗ ██║
██╔══██║██║ ███╔╝  ██╔══╝  ██║╚██╗██║
██║  ██║██║███████╗███████╗██║ ╚████║
╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝
""")

    print("AIZEN Advanced Recon Framework by Khaleel Basha")

    print("+==========================================================+")
    print(f"| Target: {domain}".ljust(59) + "|")
    print("+==========================================================+")


def section(title):

    print("\n+==========================================================+")
    print("| " + title.center(56) + " |")
    print("+==========================================================+")


# ---------------- INFRASTRUCTURE ----------------

def resolve_ips(domain):

    try:
        return [str(r) for r in dns.resolver.resolve(domain,"A")]
    except:
        return []


# ---------------- GEOLOCATION ----------------

def get_location(ip):

    try:

        data = requests.get(f"http://ip-api.com/json/{ip}").json()

        return {
            "Country":data.get("country"),
            "Region":data.get("regionName"),
            "City":data.get("city"),
            "ISP":data.get("isp")
        }

    except:
        return {}


# ---------------- SUBDOMAINS ----------------

def crtsh_lookup(domain):

    subs=set()

    try:

        r=session.get(f"https://crt.sh/?q=%25.{domain}&output=json")

        for entry in r.json():

            for name in entry["name_value"].split("\n"):

                if domain in name:
                    subs.add(name.strip())

    except:
        pass

    return list(subs)


# ---------------- WHOIS ----------------

def whois_lookup(domain):

    try:

        w=whois.whois(domain)

        creation=w.creation_date

        if isinstance(creation,list):
            creation=creation[0]

        age=round((datetime.now()-creation).days/365,2)

        return {"Registrar":w.registrar,"Domain Age":age}

    except:
        return {}


# ---------------- DNS ----------------

def dns_enum(domain):

    records={}

    for r in ["A","MX","NS","TXT"]:

        try:
            records[r]=[str(x) for x in dns.resolver.resolve(domain,r)]
        except:
            pass

    return records


# ---------------- SSL ----------------

def ssl_info(domain):

    try:

        ctx=ssl.create_default_context()

        with socket.create_connection((domain,443)) as sock:

            with ctx.wrap_socket(sock,server_hostname=domain) as ssock:

                cert=ssock.getpeercert()

                return {"Expiry":cert.get("notAfter")}

    except:
        return {}


# ---------------- HEADERS ----------------

def headers(domain):

    try:

        r=requests.get(f"https://{domain}")

        return {
            "HSTS":r.headers.get("Strict-Transport-Security"),
            "CSP":r.headers.get("Content-Security-Policy")
        }

    except:
        return {}


# ---------------- EMAILS ----------------

def emails(domain):

    found=set()

    try:

        r=requests.get(f"https://{domain}")

        soup=BeautifulSoup(r.text,"html.parser")

        for link in soup.find_all("a"):

            if "mailto:" in link.get("href",""):
                found.add(link.get("href").replace("mailto:",""))

    except:
        pass

    return list(found)


# ---------------- TECHNOLOGY ----------------

def technologies(domain):

    try:
        return builtwith.parse(f"https://{domain}")
    except:
        return {}


# ---------------- DIRECTORIES ----------------

def directories(domain):

    words=["admin","login","dashboard","uploads","backup"]

    found=[]

    for w in words:

        url=f"https://{domain}/{w}"

        try:

            r=requests.get(url)

            if r.status_code<400:
                found.append(url)

        except:
            pass

    return found


# ---------------- PORT SCAN ----------------

def ports(domain):

    p=[21,22,80,443,8080]

    open_ports=[]

    for port in p:

        try:

            s=socket.socket()
            s.settimeout(1)

            if s.connect_ex((domain,port))==0:
                open_ports.append(port)

            s.close()

        except:
            pass

    return open_ports


# ---------------- JS ENDPOINTS ----------------

def js_endpoints(domain):

    endpoints=set()

    try:

        r=requests.get(f"https://{domain}")

        soup=BeautifulSoup(r.text,"html.parser")

        scripts=[s.get("src") for s in soup.find_all("script") if s.get("src")]

        for s in scripts:

            if not s.startswith("http"):
                s=f"https://{domain}/{s}"

            js=requests.get(s).text

            matches=re.findall(r"/api/[A-Za-z0-9/_-]+",js)

            for m in matches:
                endpoints.add(m)

    except:
        pass

    return list(endpoints)


# ---------------- WAYBACK ----------------

def wayback(domain):

    snaps=[]

    try:

        url=f"http://web.archive.org/cdx/search/cdx?url={domain}&output=json&limit=10"

        r=session.get(url)

        data=r.json()

        for row in data[1:]:

            ts=row[1]

            date=datetime.strptime(ts,"%Y%m%d%H%M%S")

            snaps.append({
                "date":str(date),
                "url":f"https://web.archive.org/web/{ts}/{domain}"
            })

    except:
        pass

    return snaps


# ---------------- ARCHIVED URLS ----------------

def archived_urls(domain):

    urls=[]

    try:

        api=f"http://web.archive.org/cdx/search/cdx?url={domain}/*&output=json"

        r=session.get(api)

        data=r.json()

        for row in data[1:20]:
            urls.append(row[2])

    except:
        pass

    return urls


# ---------------- HTML REPORT ----------------

def html_report(domain,data):

    html=f"""
<html>
<head>
<title>AIZEN Report</title>
<style>
body{{background:#0f172a;color:white;font-family:Arial}}
.card{{background:#1e293b;padding:20px;margin:20px;border-radius:10px}}
</style>
</head>
<body>

<h1>AIZEN Security Report</h1>
<h2>Target: {domain}</h2>
"""

    for k,v in data.items():

        html+=f"<div class='card'><h3>{k}</h3><pre>{v}</pre></div>"

    html+="</body></html>"

    return html


# ---------------- SAVE REPORT ----------------

def save(domain,data):

    os.makedirs("reports",exist_ok=True)

    t=int(time.time())

    json_file=f"reports/scan_{t}.json"
    html_file=f"reports/scan_{t}.html"

    with open(json_file,"w") as f:
        json.dump(data,f,indent=4)

    with open(html_file,"w") as f:
        f.write(html_report(domain,data))

    print("\nReports saved:")
    print("JSON:",json_file)
    print("HTML:",html_file)


# ---------------- MAIN ----------------

def main():

    parser=argparse.ArgumentParser()

    parser.add_argument("--domain",required=True)

    args=parser.parse_args()

    domain=args.domain

    banner(domain)

    start=time.time()

    try:

        subs=crtsh_lookup(domain)

        with ThreadPoolExecutor(max_workers=10) as executor:

            futures={

                "IPs":executor.submit(resolve_ips,domain),
                "WHOIS":executor.submit(whois_lookup,domain),
                "DNS":executor.submit(dns_enum,domain),
                "SSL":executor.submit(ssl_info,domain),
                "Headers":executor.submit(headers,domain),
                "Emails":executor.submit(emails,domain),
                "Technology":executor.submit(technologies,domain),
                "Directories":executor.submit(directories,domain),
                "Ports":executor.submit(ports,domain),
                "JS Endpoints":executor.submit(js_endpoints,domain),
                "Wayback":executor.submit(wayback,domain),
                "Archived URLs":executor.submit(archived_urls,domain)

            }

            results={k:v.result() for k,v in futures.items()}

    except KeyboardInterrupt:

        print("\nScan stopped safely")
        return


    ips=results["IPs"]

    location=get_location(ips[0]) if ips else {}

    section("INFRASTRUCTURE")

    for ip in ips:
        print("IP:",ip)

    section("SERVER LOCATION")

    for k,v in location.items():
        print(f"{k:<10}: {v}")

    section("SUBDOMAINS")

    for s in subs:
        print("-",s)

    for k,v in results.items():

        section(k)

        if isinstance(v,list):

            for i in v:
                print("-",i)

        elif isinstance(v,dict):

            for x,y in v.items():
                print(f"{x:<15}: {y}")

    data=results
    data["Subdomains"]=subs
    data["Location"]=location

    save(domain,data)

    print("\nExecution Time:",round(time.time()-start,2),"seconds")


if __name__=="__main__":
    main()
