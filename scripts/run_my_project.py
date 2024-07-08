import src.main
import subprocess
import time
import timeit

from scripts.setupGUI import SetupGUI


if __name__ == '__main__':
    g = SetupGUI()
    g.run()
    while True:
        start = timeit.default_timer()
        src.main.main()
        stop = timeit.default_timer()
        print('Time: ', stop - start)
        time.sleep(5)