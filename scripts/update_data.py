#!/usr/bin/env python3
import subprocess, json, re
from datetime import datetime
from openpyxl import load_workbook

SHEET_ID = "1ECqrsi3HjcQxEf_FVVQHDJppwUga_-pHRjRpRLNyOrQ"
EXPORT_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=xlsx"
XLSX_FILE  = "/tmp/mcl_data.xlsx"
OUTPUT_FILE = "data.json"

SHEET_NAME_MAP = {'店舗別':'店舗別','新規':'新規','追加':'追加','物販':'物販','プラン比率':'プラン比率'}

def normalize(name):
    for k,v in SHEET_NAME_MAP.items():
        if k in name: return v
    return None

def extract_value(v):
    if not v or not isinstance(v,str): return v
    m = re.search(r'"""COMPUTED_VALUE"""\),(.+)\)',v)
    if m:
        try: return json.loads(m.group(1))
        except: pass
    return v

def excel_date(serial):
    if not isinstance(serial,(int,float)) or not (40000<serial<50000): return None
    try:
        from datetime import timedelta
        return (datetime(1899,12,30)+timedelta(days=serial)).strftime("%Y/%m/%d")
    except: return None

def parse():
    wb = load_workbook(XLSX_FILE)
    data = {}
    for raw in wb.sheetnames:
        name = normalize(raw)
        if not name: continue
        ws = wb[raw]
        headers = [c.value for c in ws[1]]
        rows = []
        for row in ws.iter_rows(min_row=2):
            r = {}
            for i,cell in enumerate(row):
                if i>=len(headers): break
                v = cell.value
                if isinstance(v,str) and "COMPUTED_VALUE" in v: v = extract_value(v)
                d = excel_date(v)
                if d: v = d
                r[headers[i]] = v
            if any(r.values()): rows.append(r)
        if rows: data[name] = rows
    return data

def month_key(sheet,row):
    date_str = None
    if sheet=="プラン比率": date_str = row.get("申込日")
    elif "発生日" in row:  date_str = row.get("発生日")
    elif "来店日" in row:  date_str = row.get("来店日")
    if date_str and isinstance(date_str,str) and len(date_str)>=7:
        return date_str[:7]
    return datetime.now().strftime("%Y-%m")

def main():
    print(f"[{datetime.now().isoformat()}] Updating...")
    r = subprocess.run(["curl","-L","-o",XLSX_FILE,EXPORT_URL],capture_output=True)
    if r.returncode!=0: print("Download failed"); return False
    data = parse()
    print("Sheets:", list(data.keys()))
    out = {}
    for sheet,rows in data.items():
        for row in rows:
            mk = month_key(sheet,row)
            if mk not in out: out[mk]={}
            if sheet not in out[mk]: out[mk][sheet]=[]
            out[mk][sheet].append(row)
    with open(OUTPUT_FILE,'w',encoding='utf-8') as f:
        json.dump({"ALL_DATA":out},f,ensure_ascii=False)
    for m,sheets in out.items():
        for s,rows in sheets.items():
            print(f"  {m}/{s}: {len(rows)}行")
    print("✓ Done")
    return True

if __name__=="__main__":
    exit(0 if main() else 1)
