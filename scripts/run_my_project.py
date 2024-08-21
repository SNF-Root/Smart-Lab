import src.main
import timeit
import time

from scripts.setupGUI import SetupGUI
import logging
import os
import sys


if __name__ == '__main__':
    # Create necessary files and directories
    # Are not overrided by pulling updates
    file_paths = [os.path.join('src', 'register.txt'), os.path.join('src', 'rclone.txt'), os.path.join('ansible', 'hosts.yml')]

    for file_path in file_paths:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                pass  # Create an empty file

    # Run the setup GUI to configure the project
    g = SetupGUI()
    g.run()

    # Set up logging errors with logging and sys
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = handle_exception
    
    logging.basicConfig(filename='error.log', filemode="a", level=logging.ERROR,
                        format='%(asctime)s %(levelname)s %(message)s')
    # Have a cooldown to avoid spamming errors
    last_error = None
    last_logged_time = 0
    cooldown_period = 60  # seconds

    # Run the whole program in a loop
    while True:
        try:
            start = timeit.default_timer()
            src.main.main()
            stop = timeit.default_timer()
            print('Whole Loop Runtime: ', stop - start)
        except Exception as e:
            current_time = time.time()
            error_message = str(e)
            
            if error_message != last_error or (current_time - last_logged_time) > cooldown_period:
                logging.error(f"Exception occured: {e}", exc_info=True)
                last_error = error_message
                last_logged_time = current_time
    