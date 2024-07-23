import src.main
import timeit

from scripts.setupGUI import SetupGUI
import logging
import os


if __name__ == '__main__':
    file_paths = ['src/register.txt', 'src/rclone.txt', 'ansible/hosts.yml']

for file_path in file_paths:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            pass  # Create an empty file

    g = SetupGUI()
    g.run()
    logging.basicConfig(filename='error.log', level=logging.ERROR,
                        format='%(asctime)s %(levelname)s %(message)s')
    try:
        while True:
            start = timeit.default_timer()
            src.main.main()
            stop = timeit.default_timer()
            print('Whole Loop Runtime: ', stop - start)
    except Exception as e:
        logging.error(f"Exception occured: {e}", exc_info=True)