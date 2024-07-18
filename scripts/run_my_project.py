import src.main
import timeit

from scripts.setupGUI import SetupGUI
import logging


if __name__ == '__main__':
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