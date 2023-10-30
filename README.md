# MessageValidating

This is a client and server that validates the integrity of text messages
using a protocol based on secret keys. In this scenario, a client has downloaded a file from a
3rd party, untrusted source that contains several text messages from the server, for example,
emails. The client also has a file of associated “signatures”, or hashes, of the messages, also
from the untrusted source. The signatures prove that the server originated the messages,
however, the client must verify these signatures.
The client will validate that the messages came from the server by assuming a
secure channel, and then contact the server and have it provide the signatures. If the signatures
match, the server must have originated the message.

The client and server communicate via TCP with a port defined as a command line argument.
The protocol works by sending ASCII characters — not UTF-8 or unicode strings.
The client connects to the server and issues a “HELLO” on a single line.
The server responds with a “260 OK” string if it receives the “HELLO” message.
Then the client sends a Command. There are only two commands: “DATA” or “QUIT”.
Each time that the client wants to send a message to the server it will send the DATA command
first. That means the client sends the DATA command separately and Msg 1 after that. Then for
sending the next message it will send another DATA command.
The server checks if it received the DATA command, then it will compute the hash using the key
and the message.
The server then sends the computed hash value and a “270 SIG” string to the client.
The client will compare the computed hash value with the signature value which is provided,
and it will send the PASS or FAIL to the server.
Then the server sends the “260 OK” string once again when it receives the PASS and FAIL
result from the client.
Server checks if it receives the QUIT command, so it will close the connection.
