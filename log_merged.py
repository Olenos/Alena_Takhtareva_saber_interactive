import json
import argparse
import os

from datetime import datetime
from pathlib import Path
import time


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Tool to merge two JSON log files.')

    parser.add_argument(
        'log_a',
        metavar='<LOG_FILE_A>',
        type=str,
        help='Path to the first JSON log file')

    parser.add_argument(
        'log_b',
        metavar='<LOG_FILE_B>',
        type=str,
        help='Path to the second JSON log file')

    parser.add_argument(
        '-o',
        '--output',
        help='Path to the merged JSON log file',
        dest='output_file')

    return parser.parse_args()


def _merge_logs(log_a_path: Path, log_b_path: Path) -> list:
    log_a = _open_log(log_a_path)
    log_b = _open_log(log_b_path)

    print('Merging logs...')
    merged_logs = log_a + log_b
    return merged_logs


def _open_log(log_path: Path) -> list:
    print(f'Opening log file: {log_path}...')
    with open(log_path, 'r') as file:
        logs = file.readlines()
    return logs


def _sort_logs(logs: list) -> list:
    print('Sorting logs...')
    json_list_logs = [json.loads(line) for line in logs]

    sorted_list_logs = sorted(json_list_logs, key=lambda x: datetime.strptime(x['timestamp'], '%Y-%m-%d %H:%M:%S'))

    return sorted_list_logs


def _convert_timestamp(logs: list, target_type: type) -> list:
    print('Converting timestamps...')
    for log in logs:
        log['timestamp'] = target_type(log['timestamp'])
    return logs


def _write_logs(logs: list, output_file: str) -> None:
    print('Writing merged logs...')

    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)

    with open(output_file, 'w') as file:
        for log in logs:
            json.dump(log, file, separators=(',', ':'))
            file.write('\n')
    print(f'Merged logs written to: {output_file}')


def main() -> None:
    args = _parse_args()

    log_a_path = Path(args.log_a)
    log_b_path = Path(args.log_b)
    output_file = args.output_file

    merged_logs = _merge_logs(log_a_path, log_b_path)
    sorted_logs = _sort_logs(merged_logs)
    converted_logs = _convert_timestamp(sorted_logs, str)

    _write_logs(converted_logs, output_file)


if __name__ == '__main__':
    print('Log merging tool started.')

    start_time = time.time()

    main()

    end_time = time.time()
    execution_time = end_time - start_time

    print(f'Log merging completed in {execution_time:.2f} seconds.')
