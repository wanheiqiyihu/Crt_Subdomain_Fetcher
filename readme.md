# Crt_Subdomain_Fetcher

这是一个通过使用[`crt.sh`](https://crt.sh/)获取给定域名的子域名的Python脚本。

## 依赖项

在运行此脚本之前，请确保您的系统上安装了以下软件包：

- Python 3.x
- requests

您可以使用`pip`安装所需的Python库：

```bash
pip install requests
```

## 使用方法

```bash
python Crt_Subdomain_Fetcher.py [-t DOMAIN] [-f FILE] [-threads NUMBER]
```

### 参数说明

- `-t DOMAIN`: 指定单个目标域名。
- `-f FILE`: 包含域名列表的文件，每行一个域名。
- `-threads NUMBER`: 选择使用的线程数（默认为5）。

### 示例

1. **查询单个域名的子域名**：

   ```bash
   python Crt_Subdomain_Fetcher.py -t example.com
   ```

2. **从文件中读取域名进行查询**：

   ```bash
   python Crt_Subdomain_Fetcher.py -f domain_list.txt
   ```

3. **使用自定义线程数进行查询**：

   ```bash
   python Crt_Subdomain_Fetcher.py -f domain_list.txt -threads 20
   ```

## 输出

脚本会生成一个包含所有子域名的文件，默认为`out.txt`。该文件将保存在脚本执行目录中。

## 注意事项

- 确保您输入的文件路径正确，否则程序会抛出“File not found”错误。
- 在调用API时请遵循相关法律法规，确保对方服务器的稳定性和您的合法使用。

## 贡献

如果您希望贡献此项目，请提交Issue或Pull Request。

---

# Crt_Subdomain_Fetcher

This is a Python script to fetch subdomains for given domains using [`crt.sh`](https://crt.sh/).

## Dependencies

Before running this script, ensure the following packages are installed on your system:

- Python 3.x
- requests

You can install the required Python library using `pip`:

```bash
pip install requests
```

## Usage

```bash
python Crt_Subdomain_Fetcher.py [-t DOMAIN] [-f FILE] [-threads NUMBER]
```

### Argument Description

- `-t DOMAIN`: Specify a single target domain.
- `-f FILE`: Specify a file containing a list of domains, one per line.
- `-threads NUMBER`: Choose the number of threads to use (default is 5).

### Examples

1. **Fetch subdomains for a single domain**:

   ```bash
   python Crt_Subdomain_Fetcher.py -t example.com
   ```

2. **Fetch subdomains from a list of domains in a file**:

   ```bash
   python Crt_Subdomain_Fetcher.py -f domain_list.txt
   ```

3. **Use a custom number of threads**:

   ```bash
   python Crt_Subdomain_Fetcher.py -f domain_list.txt -threads 20
   ```

## Output

The script will generate a file containing all subdomains, named `out.txt` by default. This file will be saved in the directory where the script is executed.

## Notes

- Ensure the file path you provide is correct, or the program will throw a "File not found" error.
- When using the API, comply with legal regulations and ensure the stability of the server and your lawful use.

## Contributions

If you wish to contribute to this project, please submit an Issue or a Pull Request.
