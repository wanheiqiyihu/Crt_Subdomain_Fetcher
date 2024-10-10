import requests
import argparse
import os
import concurrent.futures


def fetch_subdomains(domain, result_file):
    url = f"https://crt.sh/?q={domain}&exclude=expired&group=none&output=json"
    try:
        print(f"正在处理：{domain}")
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        json_data = response.json()


        subdomains = set()
        for entry in json_data:
            for name in entry["name_value"].splitlines():
                if name != domain:
                    subdomains.add(name)

        # 将子域名添加到文件末尾
        with open(result_file, mode='a', encoding='utf-8') as file:
            for subdomain in subdomains:
                file.write(f"{subdomain}\n")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {domain}: {e}")


def separate_subdomains(filename, wildcard_file='wildcard_subdomains.txt',
                        non_wildcard_file='non_wildcard_subdomains.txt'):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, filename)

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 保存所有子域名
    with open(wildcard_file, mode='w', encoding='utf-8') as wildcard_f, \
            open(non_wildcard_file, mode='w', encoding='utf-8') as non_wildcard_f:

        for line in sorted(set(line.strip() for line in lines)):
            if '*' in line:
                wildcard_f.write(f"{line}\n")
            else:
                non_wildcard_f.write(f"{line}\n")

    print(f"包含通配符的子域名已写入 {os.path.join(current_dir, wildcard_file)}")
    print(f"不包含通配符的子域名已写入 {os.path.join(current_dir, non_wildcard_file)}")






def remove_duplicates(filename):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, filename)

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    unique_lines = sorted(set(line.strip() for line in lines))

    with open(file_path, mode='w', encoding='utf-8') as file:
        for line in unique_lines:
            file.write(f"{line}\n")

    print(f"去重后的数据已写入 {file_path}")

    # 调用函数分离子域名
    separate_subdomains(filename)


def main():
    parser = argparse.ArgumentParser(description='Fetch and save subdomains data from crt.sh for given domains.')
    parser.add_argument('-t', type=str, help='Single domain target')
    parser.add_argument('-f', type=str, help='File containing list of domains, one per line')
    parser.add_argument('-threads', type=int, default=5, help='Number of threads to use (default: 5)')

    args = parser.parse_args()

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
            print(f"文件未找到: {args.f}")
            return

    result_file = "out.txt"

    if os.path.exists(result_file):
        os.remove(result_file)

    total_domains = len(domains)
    completed_domains = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_domain = {executor.submit(fetch_subdomains, domain, result_file): domain for domain in domains}
        for future in concurrent.futures.as_completed(future_to_domain):
            domain = future_to_domain[future]
            try:
                future.result()
            except Exception as exc:
                print(f"{domain} 生成异常: {exc}")

            completed_domains += 1
            percent_complete = (completed_domains / total_domains) * 100
            print(f"进度: {percent_complete:.2f}%", end='\r')

    remove_duplicates(result_file)


if __name__ == "__main__":
    main()
