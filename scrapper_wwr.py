# https://weworkremotely.com/

import requests
from bs4 import BeautifulSoup


def extract_job(html):
    try:
        title = html.find("span", {"class": "title"}).string
        company = html.find("span", {"class": "company"}).string
        location = html.find("span", {"class": "region company"}).string
        apply_link = html.select_one("li > a")["href"]
        return {
            "title": title,
            "company": company,
            "location": location,
            "apply_link": f"https://weworkremotely.com{apply_link}",
            "from": "Weworkremotely",
        }
    except:
        pass


def extract_jobs(url):
    jobs = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("li", {"class": "feature"})
    print(f"Scrapping WWR...")
    for result in results:
        job = extract_job(result)
        jobs.append(job)
    return jobs


def get_wwr_jobs(word):
    url = f"https://weworkremotely.com/remote-jobs/search?term={word}"
    jobs = extract_jobs(url)
    return jobs
