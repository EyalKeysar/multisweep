


def send(socket, data: bytes):
    try:
        length = len(data)
        length = str(length).zfill(6) + '|'
        payload = length.encode() + data
        socket.send(payload)
    except socket.timeout:
        pass

def recv(socket, size) -> bytes:
    try:
        length = socket.recv(7).decode()
        length = int(length[:-1])
        data = socket.recv(length)
        return data
    except socket.timeout:
        return b''
