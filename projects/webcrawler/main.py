import os
import re
import requests
import colorama
from pathlib import Path
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table

int_ext_url_table = Table(title="Internal / External URLs")

int_ext_url_table.add_column("Link", style="cyan", no_wrap=True)
int_ext_url_table.add_column("Source", style="magenta")
int_ext_url_table.add_column("Type", justify="right", style="green")

# init the colorama module
colorama.init()

GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW

report_folder = "data"

# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()

total_urls_visited = 0


def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def is_excluded_link(url):
    """
    Checks if the URL is an excluded type (email, javascript, etc.)
    You can customize this function to add more exclusions.
    """
    excluded_patterns = [r"^mailto:", r"^javascript:", r"^tel:", r"^viber:"]
    for pattern in excluded_patterns:
        if re.match(pattern, url, re.IGNORECASE):
            return True
    return False


def get_all_website_links(url):
    urls = set()
    response = None

    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        print(f"{GRAY}[!] Connection refused: {url}{RESET}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")

        if href == "" or href is None:
            continue

        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)

        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

        if not is_valid(href) or is_excluded_link(href):
            continue

        if href in internal_urls:
            # already in the set
            continue

        if domain_name not in href:
            # external link
            if href not in external_urls:
                print(f"{GRAY}[!] External link: {href}{RESET}")
                int_ext_url_table.add_row(href, url, "[yellow]External")
                external_urls.add(href)
            continue

        print(f"{GREEN}[*] Internal link: {href}{RESET}")

        urls.add(href)

        internal_urls.add(href)
        int_ext_url_table.add_row(href, url, "[green]Internal")
    return urls


def crawl(url, max_urls=30):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """
    global total_urls_visited
    total_urls_visited += 1
    print(f"{YELLOW}[*] Crawling: {url}{RESET}")
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Link Extractor Tool with Python")
    parser.add_argument("url", help="The URL to extract links from.")
    parser.add_argument(
        "-m",
        "--max-urls",
        help="Number of max URLs to crawl, default is 30.",
        default=30,
        type=int,
    )

    args = parser.parse_args()
    url = args.url
    max_urls = args.max_urls

    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc

    Path(report_folder).mkdir(parents=True, exist_ok=True)

    crawl(url, max_urls=max_urls)

    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total External links:", len(external_urls))
    print("[+] Total URLs:", len(external_urls) + len(internal_urls))
    print("[+] Total crawled URLs:", max_urls)

    # save the internal links to a file
    with open(
        os.path.join(report_folder, f"{domain_name}_internal_links.txt"),
        "w",
        encoding="utf-8",
    ) as f:
        for internal_link in internal_urls:
            print(internal_link.strip(), file=f)

    # save the external links to a file
    with open(
        os.path.join(report_folder, f"{domain_name}_external_links.txt"),
        "w",
        encoding="utf-8",
    ) as f:
        for external_link in external_urls:
            print(external_link.strip(), file=f)

    console = Console()
    console.print(int_ext_url_table)
