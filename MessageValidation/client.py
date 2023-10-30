import sys
import socket

def main():
    server_name = sys.argv[1]
    server_port = int(sys.argv[2])
    message_filename = sys.argv[3]
    signature_filename = sys.argv[4]

    # Read messages from the message file
    messages = []
    with open(message_filename, 'r') as message_file:
        while True:
            length = message_file.readline().strip()
            if not length:
                break
            message = message_file.read(int(length)).strip()
            messages.append(message)

    # Read signatures from the signature file
    signatures = []
    with open(signature_filename, 'r') as signature_file:
        for line in signature_file:
            signatures.append(line.strip())

    # Open a TCP socket to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_name, server_port))

    # Send a "HELLO" message to the server
    client_socket.sendall("HELLO\n".encode('ascii'))

    
    response = client_socket.recv(1024).decode('ascii').strip()
    print(response)

    if response != "260 OK":
        print("Error: Server response is not '260 OK'")
        client_socket.close()
        return

    message_counter = 0

    for message in messages:

        # Send the "DATA" command
        client_socket.sendall("DATA\n".encode('ascii'))

        # Send the message
        client_socket.sendall((message + "\n.\n").encode('ascii'))
        
        response = client_socket.recv(1024).decode('ascii').strip()
        print(response)
        if response != "270 SIG":
            print(f"Error: Server response is not '270 SIG' for message {message_counter}")
            client_socket.close()
            return
        
        # Receive the signature from the server
        server_signature = client_socket.recv(1024).decode('ascii').strip()
        print(server_signature)

        if server_signature == signatures[message_counter]:
            client_socket.sendall("PASS\n".encode('ascii'))
        else:
            client_socket.sendall("FAIL\n".encode('ascii'))

        response = client_socket.recv(1024).decode('ascii').strip()
        print(response)

        if response != "260 OK":
            print("Error: Server response is not '260 OK' after message validation")
            client_socket.close()
            return

        message_counter += 1

    # Send a "QUIT" message to the server
    client_socket.sendall("QUIT\n".encode('ascii'))

    # Close the TCP socket
    client_socket.close()

if __name__ == "__main__":
    main()
