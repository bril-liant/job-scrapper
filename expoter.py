import csv


def save_to_file(jobs, word):
    file = open(f"{word}_jobs.csv", mode="w", encoding="utf-8-sig", newline="")
    writer = csv.writer(file)
    writer.writerow(["title", "company", "location", "link", "from"])
    for job in jobs:
        writer.writerow(list(job.values()))
    return
