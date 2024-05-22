import argparse
import os
import re
import requests 
import html
import subprocess
import sys

path = './exploit-db'


def exploit_func(id):
    filename = os.path.join(path, f"{id}.txt")
    
    try:
        if os.path.exists(filename):
            print(f"Exit, opening {filename}")
            with open(filename) as f:
                exploit = f.read()
        else:
            url = 'https://exploit-db.com/exploits/{id}'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            res = requests.get(url, headers=headers)
            exploit = res.text[res.text.find('<code') : res.text.find('</code>')]
            exploit = html.unescape(exploit[exploit.find('">') + 2 :])
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(exploit)
    except Exception as e:
        print("Error:", e)
        return
    
    try:
        if sys.platform.startswith('win'):  
            subprocess.run(['notepad.exe', filename], check=True)
        elif sys.platform.startswith('linux'):  
            subprocess.run(['xdg-open', filename], check=True)
        else:
            print("Unsupported platform.")    
    except subprocess.CalledProcessError as e:
        print("Error opening exploit file:", e)

def page_func(page_num):
    files_in_page = sorted(os.listdir(path), key=lambda x: int(x.split('.')[0]))
    exploits_in_page = [int(filename.split('.')[0]) for filename in files_in_page]
    start_i = page_num *5
    end_i = min((page_num + 1) * 5, len(exploits_in_page))
    if exploits_in_page:
        print(f"Exploit in page {page_num}")
        for expl_id in exploits_in_page[start_i:end_i]:
            print(expl_id)


def search_func(keyword):
    keywords = keyword.split()
    matches = set()
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        with open(os.path.join(path, filename), 'r', encoding='utf-8') as f:
            exploit = f.read().lower()
            for i in range(len(keywords)):
                pattern = r'\b' + keywords[i]  + r'\b'
                if re.search(pattern, exploit, re.IGNORECASE):
                    print(pattern)
                    matches.add(filepath)
    if matches:
        for expl in matches:
            print(expl)
    else:
        print("keyword not found.")

def main():
    parser = argparse.ArgumentParser(description="Python Exam")
    parser.add_argument("--exploit", help="Exploit by ID")
    parser.add_argument("--page", type=int, help="get page")
    parser.add_argument("--search", help="Search keyword")
    args = parser.parse_args()

    if args.exploit:       
        res = re.match(r'^(https://www.exploit-db\.com/exploits/)?(\d+)$', args.exploit) 
        print(res)
        if res is not None:
            exploit_id = re.search(r'\d+', args.exploit).group()  # Extract ID from input
            exploit_func(exploit_id)
        return
    elif args.page is not None: 
        page_func(args.page)
        return
    elif args.search:
        search_func(args.search)
        return
    else:

        parser.print_help()

if __name__ == '__main__':
    main()
