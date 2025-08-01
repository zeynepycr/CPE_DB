import requests
import gzip
import xml.etree.ElementTree as ET
import json

url = "https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.gz"
input_gz = "official-cpe-dictionary_v2.3.xml.gz"
output_json = "cpe_db.json"

def download_file(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download file: {response.status_code}")

download_file(url, input_gz)

entries = []

try:
    with gzip.open(input_gz, 'rt', encoding='utf-8') as f:
        tree = ET.parse(f)
        root = tree.getroot()
        for item in root.findall(".//{http://cpe.mitre.org/dictionary/2.0}cpe-item"):
            cpe_name = item.attrib.get('name')
            title_elem = item.find("{http://cpe.mitre.org/dictionary/2.0}title")
            title = title_elem.text if title_elem is not None else ""
            vendor = ""
            product = ""
            if cpe_name:
                parts = cpe_name.split(':')
                if len(parts) > 2:
                    vendor = parts[2]
                if len(parts) > 3:
                    product = parts[3]
            entries.append({
                "CpeName": cpe_name,
                "Title": title,
                "Vendor": vendor,
                "Product": product
            })
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    print(f"Converted {input_gz} to {output_json} successfully.")
except Exception as e:
    print(f"Error: {e}")