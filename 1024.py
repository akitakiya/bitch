import socket

def main():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 1024))
    s.listen(1500)
    while 1:
        conn, addr = s.accept()
        print(addr)
        headers = ''
        while 1:
            buf = conn.recv(2048).decode('utf-8')
            headers += buf
            if len(buf) < 2048:
                break

        headers = headers.replace('127.0.0.1:1024', 't66y.com')\
                         .replace('keep-alive', 'close')\
                         .replace('gzip','')
        print(headers)
        s1 = socket.socket()
        s1.connect(('t66y.com', 80))
        s1.sendall(headers.encode())

        resp = b''
        while 1:
            try:
                buf = s1.recv(1024*8)
            except socket.timeout as e:
                print(e)
                break

            resp += buf
            if not buf or\
               buf.startswith(b'WebSocket') and buf.endswith(b'\r\n\r\n'):
                break

        resp = resp.replace(b'Content-Encoding: gzip\r\n', b'')\
                   .replace(b't66y.com', b'bjgong.tk:1024')
        print('send to', addr)
        conn.sendall(resp)
        conn.close()


main()
