import os
import subprocess
import time
import argparse

LANGUAGES = {
    'en': {
        'list_prompt': "List of Python files in the current directory:",
        'cycle_start': "Starting {file} for {on_time} seconds...",
        'cycle_stop': "{file} stopped. Sleeping for {off_time} seconds...",
        'cycle_interrupted': "Cycle interrupted.",
        'switch_to': "Switching to {after_file}...",
        'run_once': "Running {file}...",
        'list_processes': "Running Python processes:",
        'process_error': "Error listing processes: {error}",
        'kill_success': "Successfully killed processes with name {name}.",
        'kill_failure': "No processes found with name {name}.",
        'kill_error': "Error killing process: {error}",
        'lang_prompt': "Choose language (en/ru): "
    },
    'ru': {
        'list_prompt': "Список Python файлов в текущей директории:",
        'cycle_start': "Запуск {file} на {on_time} секунд...",
        'cycle_stop': "{file} остановлен. Ожидание {off_time} секунд...",
        'cycle_interrupted': "Цикл прерван.",
        'switch_to': "Переключение на {after_file}...",
        'run_once': "Запуск {file}...",
        'list_processes': "Запущенные Python процессы:",
        'process_error': "Ошибка при получении списка процессов: {error}",
        'kill_success': "Успешно завершены процессы с именем {name}.",
        'kill_failure': "Процессы с именем {name} не найдены.",
        'kill_error': "Ошибка завершения процесса: {error}",
        'lang_prompt': "Выберите язык (en/ru): "
    }
}

def get_language():
    lang = input(LANGUAGES['en']['lang_prompt'] + LANGUAGES['ru']['lang_prompt']).strip()
    return LANGUAGES.get(lang, LANGUAGES['en'])

def list_python_files(language):
    print(language['list_prompt'])
    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.py')]
    for i, file in enumerate(files, start=1):
        print(f"{i}. {file}")
    return files

def run_with_cycle(file, on_time, off_time, language):
    try:
        while True:
            print(language['cycle_start'].format(file=file, on_time=on_time))
            process = subprocess.Popen(['python', file])
            time.sleep(on_time)
            process.terminate()
            print(language['cycle_stop'].format(file=file, off_time=off_time))
            time.sleep(off_time)
    except KeyboardInterrupt:
        print(language['cycle_interrupted'])

def cycle_with_switch(file1, on_time, off_time, after_file, language):
    try:
        while True:
            print(language['cycle_start'].format(file=file1, on_time=on_time))
            process = subprocess.Popen(['python', file1])
            time.sleep(on_time)
            process.terminate()
            print(language['cycle_stop'].format(file=file1, off_time=off_time))
            time.sleep(off_time)
            print(language['switch_to'].format(after_file=after_file))
            subprocess.run(['python', after_file])
            break
    except KeyboardInterrupt:
        print(language['cycle_interrupted'])

def run_once(file, language):
    print(language['run_once'].format(file=file))
    subprocess.run(['python', file])

def list_running_processes(language):
    try:
        result = subprocess.run(['ps', '-fA'], stdout=subprocess.PIPE, text=True)
        processes = [line for line in result.stdout.splitlines() if 'python' in line]
        print(language['list_processes'])
        for process in processes:
            print(process)
    except Exception as e:
        print(language['process_error'].format(error=e))

def kill_process_by_name(name, language):
    try:
        result = subprocess.run(['pkill', '-f', name], text=True)
        if result.returncode == 0:
            print(language['kill_success'].format(name=name))
        else:
            print(language['kill_failure'].format(name=name))
    except Exception as e:
        print(language['kill_error'].format(error=e))

def run_complex_cycle(tasks, language):
    try:
        while True:
            for task in tasks:
                file, on_time, off_time = task['file'], task['on_time'], task['off_time']
                print(language['cycle_start'].format(file=file, on_time=on_time))
                process = subprocess.Popen(['python', file])
                time.sleep(on_time)
                process.terminate()
                print(language['cycle_stop'].format(file=file, off_time=off_time))
                time.sleep(off_time)
    except KeyboardInterrupt:
        print(language['cycle_interrupted'])

def parse_complex_cycle_arg(arg):
    tasks = []
    for entry in arg:
        file, on_time, off_time = entry.split(':')
        tasks.append({
            'file': file,
            'on_time': int(on_time) * 3600, 
            'off_time': int(off_time) * 3600  
        })
    return tasks

def main():
    language = get_language()
    parser = argparse.ArgumentParser(description="Python file manager CLI.")
    parser.add_argument('--list', action='store_true', help="List Python files in the current directory.")
    parser.add_argument('--cycle', nargs=3, metavar=('FILE', 'ON_TIME', 'OFF_TIME'),
                        help="Run a Python file in a cycle of ON_TIME and OFF_TIME seconds.")
    parser.add_argument('--aftercycle', nargs=4, metavar=('FILE1', 'ON_TIME', 'OFF_TIME', 'FILE2'),
                        help="Run FILE1 in a cycle and then switch to FILE2.")
    parser.add_argument('--runonce', metavar='FILE', help="Run a Python file once.")
    parser.add_argument('--listprocs', action='store_true', help="List all running Python processes.")
    parser.add_argument('--kill', metavar='NAME', help="Kill a Python process by name.")
    parser.add_argument('--complexcycle', nargs='+', metavar='FILE:ON_TIME:OFF_TIME',
                        help="Run multiple Python files in complex cycles.")

    args = parser.parse_args()

    if args.list:
        list_python_files(language)

    if args.cycle:
        file, on_time, off_time = args.cycle
        run_with_cycle(file, int(on_time), int(off_time), language)

    if args.aftercycle:
        file1, on_time, off_time, file2 = args.aftercycle
        cycle_with_switch(file1, int(on_time), int(off_time), file2, language)

    if args.runonce:
        run_once(args.runonce, language)

    if args.listprocs:
        list_running_processes(language)

    if args.kill:
        kill_process_by_name(args.kill, language)

    if args.complexcycle:
        tasks = parse_complex_cycle_arg(args.complexcycle)
        run_complex_cycle(tasks, language)

if __name__ == "__main__":
    main()
