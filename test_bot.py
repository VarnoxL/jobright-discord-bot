from bot import parse

MD = """| Company | Job Title | Location | Work Model | Date Posted |
| ----- | --------- |  --------- | ---- | ------- |
| **[IBM](http://www.ibm.com)** | **[SWE Intern](https://jobright.ai/jobs/info/abc123?x=1)** | NY | On Site | Oct 23 |
| **[Roblox](https://roblox.com)** | **[[2027] SWE](https://jobright.ai/jobs/info/ghi789?x=1)** | CA | Hybrid | Oct 22 |
| ↳ | **[Dev Intern](https://jobright.ai/jobs/info/def456?x=1)** | NY | Hybrid | Oct 23 |
"""
jobs = parse(MD)
assert [j["id"] for j in jobs] == ["abc123", "ghi789", "def456"]
assert jobs[1]["title"] == "[2027] SWE"
assert jobs[2]["company"] == "Roblox" and jobs[2]["title"] == "Dev Intern"
print("ok")
