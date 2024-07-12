import src.main
import timeit

from scripts.setupGUI import SetupGUI


if __name__ == '__main__':
    g = SetupGUI()
    g.run()
    while True:
        start = timeit.default_timer()
        src.main.main()
        stop = timeit.default_timer()
        print('Runtime: ', stop - start)