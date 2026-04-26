"""Tra cứu kho lưu trữ chứng chỉ công khai để lọc ra các tên miền phụ chứa thông tin quan trọng."""
import requests

def find_subdomains(domain):
    url = f"https://crt.sh/?q={domain}&output=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        subdomains = set([entry['name_value'] for entry in data])
        for sub in sorted(subdomains):
            if "the-flag-is" in sub:
                print(f"Tìm thấy Flag tiềm năng: {sub}")
    else:
        print("Không thể kết nối tới crt.sh")

find_subdomains("cryptohack.org")
