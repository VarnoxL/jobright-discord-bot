from bot import parse

MD = """| Company | Job Title | Location | Work Model | Date Posted |
| ----- | --------- |  --------- | ---- | ------- |
| **[IBM](http://www.ibm.com)** | **[SWE Intern](https://jobright.ai/jobs/info/abc123?x=1)** | NY | On Site | Oct 23 |
| ↳ | **[Dev Intern](https://jobright.ai/jobs/info/def456?x=1)** | NY | Hybrid | Oct 23 |
"""
jobs = parse(MD)
assert [j["id"] for j in jobs] == ["abc123", "def456"]
assert jobs[1]["company"] == "IBM" and jobs[1]["title"] == "Dev Intern"
print("ok")
