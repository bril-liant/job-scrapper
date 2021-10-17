import requests
from bs4 import BeautifulSoup


def get_last_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, "html.parser")
    try:
        pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
        last_page = pages[-2].get_text(strip=True)
        return int(last_page)
    except:
        pass


def extract_job(html):

    title = html.find("h2", {"class": "fc-black-800"}).find("a")["title"]
    company = html.find("h3", {"class": "fc-black-700"}).find("span").string
    if company is not None:
        company = company.string.strip()
    else:
        company = None
    location = (
        html.find("h3", {"class": "fc-black-700"})
        .find("span", {"class": "fc-black-500"})
        .string
    )
    if location is not None:
        location = location.string.strip()
    else:
        location = None
    job_id = html["data-jobid"]
    return {
        "title": title,
        "company": company,
        "location": location,
        "apply_link": f"https://stackoverflow.com/jobs/{job_id}",
        "from": "Stackoverflow",
    }


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping SO: Page {page}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_so_jobs(word):
    url = f"https://stackoverflow.com/jobs?r=true&q={word}"
    last_page = get_last_page(url)
    if last_page:
        jobs = extract_jobs(last_page, url)
        return jobs
    else:
        pass
