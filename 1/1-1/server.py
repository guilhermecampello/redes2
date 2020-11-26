import socket
import selectors

sel = selectors.DefaultSelector()
def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)
    conn.sendall(b'dir')

def read(conn, mask):
    data = conn.recv(1024)  # Should be ready
    if data:
      print(repr(data))
    else:
      print('closing', conn)
      sel.unregister(conn)
      conn.close()

HOST = ''
PORT = 50007
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)
while True:
  events = sel.select()
  for key, mask in events:
    callback = key.data
    callback(key.fileobj, mask)
