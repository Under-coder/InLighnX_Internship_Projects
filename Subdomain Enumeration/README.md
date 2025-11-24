**Subdomain Finder**
---------------------

This program checks a list of possible subdomains for a given domain and identifies which ones exist.
It loads subdomains from a text file (subdomains.txt), tests each one using HTTP requests, and saves all successfully discovered subdomains to discovered_subdomains.txt.
Threading is used to speed up the scanning process.



**How it works**

- Reads subdomains from a file
- Tries accessing "http://subdomain.domain" for each entry
- If the URL responds with status code 200, it is marked as discovered
- Results are stored in an output file
