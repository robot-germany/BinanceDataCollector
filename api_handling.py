import requests
import concurrent.futures
import threading


thread_local = threading.local()


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(site):
    session = get_session()
    try:
        with session.get(site[0]) as response:
            return [response.json(), site[1]]
    except requests.exceptions.RequestException as e:
        print(f"Connection error for site {site[0]}: {e}")
        return None


def download_all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=80) as executor:
        results = executor.map(download_site, sites)
        try:
            successful_results = filter[None, results]
        except TypeError:
            raise RuntimeError("Connection Error!")
        return successful_results
