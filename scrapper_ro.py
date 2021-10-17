# https://remoteok.io/

import requests
from bs4 import BeautifulSoup


def extract_jobs(url):
    jobs = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, "html.parser")
    try:
        container = soup.find("table", {"id": "jobsboard"})
        results = container.find_all("tr", {"class": "job"})
        print(f"Scrapping remote...")

        for result in results:
            try:
                title = result.find("h2", {"itemprop": "title"}).string
                company = result.find("h3", {"itemprop": "name"}).string
                location = result.find("div", {"class": "location"}).string.strip()
                apply_link = result.select_one("td.source > a")["href"]
                job = {
                    "title": title,
                    "company": company,
                    "location": location,
                    "apply_link": f"https://remoteok.io{apply_link}",
                    "from": "Remote",
                }
                jobs.append(job)
            except:
                continue
        return jobs
    except:
        pass


def get_ro_jobs(word):
    url = f"https://remoteok.io/remote-dev+{word}-jobs"
    jobs = extract_jobs(url)
    return jobs
