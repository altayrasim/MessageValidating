import sys
import socket
import hashlib

def read(connection):
    line = ""
    while True :
        char = connection.recv(1).decode('ascii')
        if char == "\n":
            break
        line += char
    return line

def main():

    listen_port = int(sys.argv[1])
    key_file = sys.argv[2]

    # Read in all the keys from the key-file
    keys = []
    with open(key_file, 'r') as key_file:
        for line in key_file:
            keys.append(line.replace('\n', ''))

    # Open a TCP socket on the port
    address = ('0.0.0.0', listen_port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(address)
    server_socket.listen(1)

    while True:
        connection, addr = server_socket.accept()

        # Read a line from the connected socket
        request = read(connection)
        print(request)

        if request != "HELLO":
            print("Error: Client did not send 'HELLO'")
            connection.close()
            continue

        connection.send("260 OK\n".encode('ascii'))

        keyCount = 0
        # Process DATA or QUIT commands
        while True:
            command = read(connection)
            print(command)
            if not command:
                break
            if command == "DATA":
                sha256_hash = hashlib.sha256()
                decoded_message = ""
                
                while True:
                    line = read(connection)
                    if line == ".":
                        break
                    decoded_message = line.replace("\\\\", "\\").replace("\\.", ".")                  

                sha256_hash.update(decoded_message.encode('ascii'))
                sha256_hash.update(keys[keyCount].encode('ascii'))
                signature = sha256_hash.hexdigest()
                keyCount += 1

                connection.send("270 SIG\n".encode('ascii'))
                connection.send((signature + "\n").encode('ascii'))

                response = read(connection)
                print(response)
                if response != "PASS" and response != "FAIL":
                    print("Error: Client response is not 'PASS' or 'FAIL'")
                    connection.close()
                    break

                connection.send("260 OK\n".encode('ascii'))

            elif command == "QUIT":
                connection.close()
                sys.exit(0)

            else:
                print("Error: Invalid command")
                connection.close()
                break

if __name__ == "__main__":
    main()
