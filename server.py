import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("192.168.1.14", 53134))
sock.listen()
clients = []

def handle_client(client):
  while True:
    try:
      data = client.recv(1024)
      if not data:
        break
      for c in clients:
        c.sendall(data)
    except Exception as e:
      print(f"Erreur de réception ou d'envoi: {e}")
      break
  clients.remove(client)
  client.close()

def handle_connection(conn, addr):
  pseudo = conn.recv(1024).decode("utf-8")
  print(f"Nouveau client connecté: {pseudo} ({addr[0]}:{addr[1]})")
  clients.append(conn)
  client_thread = threading.Thread(target=handle_client, args=(conn,))
  client_thread.start()

while True:
  conn, addr = sock.accept()

  connection_thread = threading.Thread(target=handle_connection, args=(conn, addr))
  connection_thread.start()