import requests
import argparse
import os
import concurrent.futures


def fetch_subdomains(domain):
    url = f"https://crt.sh/?q={domain}&exclude=expired&group=none&output=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
        print(f"正在处理：{domain}")
        # 处理每个 entry.name_value，首先分行，再将不等于 domain 的子域名加入结果
        subdomains = set()
        for entry in json_data:
            for name in entry["name_value"].splitlines():
                if name != domain:
                    subdomains.add(name)
        return list(subdomains)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {domain}: {e}")
        return []


def save_to_txt(data, filename="out.txt"):
    unique_data = sorted(set(data))
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, filename)

    with open(file_path, mode='w', encoding='utf-8') as file:
        for item in unique_data:
            file.write(f"{item}\n")
    print(f"Data has been written to {file_path}")


def main():
    parser = argparse.ArgumentParser(description='Fetch and save subdomains data from crt.sh for given domains.')
    parser.add_argument('-t', type=str, help='Single domain target')
    parser.add_argument('-f', type=str, help='File containing list of domains, one per line')
    parser.add_argument('-threads', type=int, default=10, help='Number of threads to use (default: 10)')

    args = parser.parse_args()

    # 仅当 -t 和 -f 参数都未提供时才显示帮助信息
    if args.t is None and args.f is None:
        parser.print_help()
        return

    domains = set()

    if args.t:
        domains.add(args.t)

    if args.f:
        try:
            with open(args.f, 'r') as file:
                file_domains = {line.strip() for line in file if line.strip()}
                domains.update(file_domains)
        except FileNotFoundError:
            print(f"File not found: {args.f}")
            return

    all_subdomains = set()
    total_domains = len(domains)
    completed_domains = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_domain = {executor.submit(fetch_subdomains, domain): domain for domain in domains}
        for future in concurrent.futures.as_completed(future_to_domain):
            domain = future_to_domain[future]
            try:
                subdomains = future.result()
                if subdomains:
                    all_subdomains.update(set(subdomains) - {domain})
            except Exception as exc:
                print(f"{domain} generated an exception: {exc}")

            # 更新已完成任务数并输出百分比
            completed_domains += 1
            percent_complete = (completed_domains / total_domains) * 100
            print(f"进度: {percent_complete:.2f}%", end='\r')

    save_to_txt(all_subdomains)


if __name__ == "__main__":
    main()
