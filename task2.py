import json
import time
from datasketch import HyperLogLog

LOG_FILE = "lms-stage-access.log"

def extract_ips_from_log(filename):
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            try:
                data = json.loads(line)
                ip = data.get("remote_addr")
                if ip:
                    yield ip
            except json.JSONDecodeError:
                continue

def exact_unique_count(ip_list):
    return len(set(ip_list))

def hll_unique_count(ip_list, precision=14):
    hll = HyperLogLog(p=precision)
    for ip in ip_list:
        hll.update(ip.encode("utf-8"))
    return int(hll.count())

def main():
    ip_list = list(extract_ips_from_log(LOG_FILE))

    start = time.time()
    exact = exact_unique_count(ip_list)
    exact_time = time.time() - start

    start = time.time()
    hll = hll_unique_count(ip_list)
    hll_time = time.time() - start

    print("Результати порівняння:")
    print(f"{'':30}{'Точний підрахунок':>20}{'HyperLogLog':>15}")
    print(f"{'Унікальні елементи':30}{exact:>20}{hll:>15}")
    print(f"{'Час виконання (сек.)':30}{exact_time:>20.4f}{hll_time:>15.4f}")

if __name__ == "__main__":
    main()
