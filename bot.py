import json, os, re, sys, urllib.request

RAW = "https://raw.githubusercontent.com/jobright-ai/{}/master/README.md"
FEEDS = [  # (jobright repo, webhook env var, seen file)
    ("2026-Software-Engineer-Internship", "DISCORD_WEBHOOK", "seen.json"),
    ("2026-Software-Engineer-New-Grad", "DISCORD_WEBHOOK_NEWGRAD", "seen_newgrad.json"),
]
LINK = re.compile(r"\[(.+)\]\(([^)]+)\)")  # greedy: titles can contain [brackets]
JOB_ID = re.compile(r"/jobs/info/(\w+)")


def parse(md):
    jobs, company = [], ""
    for line in md.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 5 or not (m := JOB_ID.search(cells[1])):
            continue
        if cells[0] != "↳":  # ↳ = same company as previous row
            company = (LINK.search(cells[0]) or [None, cells[0].strip("*")])[1]
        title, url = LINK.search(cells[1]).groups()
        jobs.append(dict(id=m[1], company=company, title=title, url=url,
                         location=cells[2], model=cells[3], date=cells[4]))
    return jobs


def post(webhook, jobs):
    for i in range(0, len(jobs), 10):  # Discord max 10 embeds/message
        embeds = [{"title": f"{j['company']} – {j['title']}"[:256], "url": j["url"],
                   "description": f"📍 {j['location']} · {j['model']} · {j['date']}"} for j in jobs[i:i + 10]]
        req = urllib.request.Request(webhook, json.dumps({"embeds": embeds}).encode(),
                                     {"Content-Type": "application/json", "User-Agent": "jobright-bot"})
        urllib.request.urlopen(req).close()


def run(repo, hook_env, seen_file):
    jobs = parse(urllib.request.urlopen(RAW.format(repo)).read().decode())
    if not jobs:
        sys.exit(f"{repo}: parsed 0 jobs — README format changed?")
    first_run = not os.path.exists(seen_file)
    seen = set() if first_run else set(json.load(open(seen_file)))
    new = [j for j in jobs if j["id"] not in seen]
    if new and not first_run:
        post(os.environ[hook_env], new[::-1])  # oldest first
    json.dump(sorted(seen | {j["id"] for j in jobs}), open(seen_file, "w"), indent=0)
    print(f"{repo}: {len(jobs)} jobs, {len(new)} new, first_run={first_run}")


if __name__ == "__main__":
    for feed in FEEDS:
        run(*feed)
