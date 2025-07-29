import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5560")

queries = [
    "221 NE 122nd Avenue, Portland, OR 97230",  # Test a valid address
    "Seattle, WA",                              # Test by city, state
    "asdjklqwe",                                # Invalid test / gibberish
    ""                                          # Test a blank string
]

for query in queries:
    print(f"\nQuery: '{query}'")
    socket.send_string(query)
    reply = socket.recv_json()
    print("Response:")
    print(json.dumps(reply, indent=2))
