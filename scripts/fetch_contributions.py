#!/usr/bin/env python3
"""Fetch public GitHub contribution HTML and save normalized JSON. No token required."""
from __future__ import annotations
import json, os, re
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path
import requests
from bs4 import BeautifulSoup

USERNAME=os.getenv("GITHUB_USERNAME","Zaid7829")
OUT=Path("data/contributions.json")
URL=f"https://github.com/users/{USERNAME}/contributions"

def level(count:int)->int:
    if count<=0: return 0
    if count<=2: return 1
    if count<=5: return 2
    if count<=10: return 3
    if count<=20: return 4
    return 5

def parse_count(text:str)->int:
    m=re.search(r"(\d[\d,]*)\s+contribution",text,re.I)
    return int(m.group(1).replace(",","")) if m else 0

def main():
    r=requests.get(URL,headers={"User-Agent":"Zaid7829-profile-art/1.0"},timeout=20)
    r.raise_for_status()
    soup=BeautifulSoup(r.text,"html.parser")
    found={}
    for cell in soup.select("[data-date]"):
        raw=cell.get("data-date")
        if not raw: continue
        try: d=date.fromisoformat(raw)
        except ValueError: continue
        text=cell.get("aria-label","") or cell.get_text(" ",strip=True)
        count=int(cell.get("data-count") or parse_count(text))
        found[d.isoformat()]=count
    if not found:
        raise RuntimeError("No contribution cells found. GitHub may have changed its HTML layout.")

    latest=max(found)
    latest_date=date.fromisoformat(latest)
    start=latest_date-timedelta(days=364)
    start-=timedelta(days=(start.weekday()+1)%7)
    end=start+timedelta(days=370)
    days=[]
    d=start
    while d<=end:
        c=found.get(d.isoformat(),0)
        days.append({"date":d.isoformat(),"count":c,"level":level(c)})
        d+=timedelta(days=1)

    chronological=sorted(days,key=lambda x:x["date"])
    latest_real=min(date.today(),end)
    current=0
    for x in reversed([x for x in chronological if date.fromisoformat(x["date"])<=latest_real]):
        if x["count"]>0: current+=1
        else: break
    longest=0; run=0
    for x in chronological:
        run=run+1 if x["count"]>0 else 0
        longest=max(longest,run)
    best=max(chronological,key=lambda x:x["count"])
    monthly=defaultdict(int)
    for x in chronological: monthly[x["date"][:7]]+=x["count"]
    total=sum(x["count"] for x in chronological)
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps({"username":USERNAME,"generated_at":__import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),"days":days,"stats":{"total":total,"current_streak":current,"longest_streak":longest,"best_day":{"date":best["date"],"count":best["count"]},"monthly":dict(monthly)}},indent=2),encoding="utf-8")
    print(f"Fetched {total:,} contributions for {USERNAME} -> {OUT}")

if __name__=="__main__": main()
