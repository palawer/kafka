from tasks.send_task import send_task
from config    import collector_topic
from db import Domain
from db import DomainCheck
from db import delete_tables
from db import create_tables
import time

n_pulls = 3
sleep_between_pulls = 20

if __name__== "__main__":
    domains = {
        "helsinkitimes" : "https://www.helsinkitimes.fi/",
        "berlin"        : "https://www.berlin.de/en/news/",
        "9news"         : "https://www.9news.com.au/sydney",
        "fail!"         : "fail://fail.com",
    }
    domain_checks = {
        "helsinkitimes" : ["covid(\\d+) ","govern(\\w+)"],
    }
    delete_tables()
    create_tables()
    domain_ids = []
    for name,url in domains.items():
        d = Domain(
            domain = name,
            url    = url
        )
        d.save()
        domain_ids.append(d.id)
        for idx,regexp in enumerate(domain_checks.get(name,[])):
            DomainCheck(
                domain_id   = d.id,
                name        = f"{name}-{idx}",
                regexp      = regexp,
            ).save()
    
    for x in range(n_pulls):
        for d_id in domain_ids:
            print(f"sending collector task for {d_id}")
            send_task(
                topic       = collector_topic,
                domain_id   = d_id
            )
        time.sleep(sleep_between_pulls)
