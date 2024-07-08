import src.main
import subprocess
import time
import timeit

if __name__ == '__main__':
    print("it works!")
    subprocess.run("python3 setupGUI.py", shell=True)
    while True:
        start = timeit.default_timer()
        src.main.main()
        stop = timeit.default_timer()
        print('Time: ', stop - start)
        time.sleep(5)