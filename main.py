import sys

if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) < 2:
        print("error")
        sys.exit(5)
