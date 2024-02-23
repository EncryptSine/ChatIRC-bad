import tkinter as tk
import socket
import threading

connected = False

def connect():

  pseudo = entry.get()

  login_window.destroy()

  open_chat_window(pseudo)

def open_chat_window(pseudo):

  chat_window = tk.Tk()
  chat_window.title("Chat - " + pseudo)
  chat_window.geometry("400x600")

  messages = tk.Text(chat_window)
  messages.pack()
  entry = tk.Entry(chat_window)
  entry.pack()

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    sock.connect(("0.0.0.0", 53134))
  except Exception as e:
    print(f"Erreur de connexion: {e}")
    return

  sock.sendall(pseudo.encode("utf-8"))

  global connected
  connected = True
  
  def receive_message():
    while connected:
        try:
            data = sock.recv(1024)
            if not data:
                break
            messages.insert("end", data.decode("utf-8") + "\n")
            messages.see("end")
        except Exception as e:
            print(f"Erreur de réception: {e}")
            break
  receive_thread = threading.Thread(target=receive_message)
  receive_thread.start()
  def send_message(event=None):
    message = entry.get()
    message = pseudo + ": " + message
    try:
        sock.sendall(message.encode("utf-8"))
        entry.delete(0, "end")
    except Exception as e:
        print(f"Erreur d'envoi: {e}")

  entry.bind("<Return>", send_message)
  
  button = tk.Button(chat_window, text="Envoyer", command=send_message)
  button.pack()
  def on_close():
    global connected
    connected = False
    sock.close()
    chat_window.destroy()
  chat_window.protocol("WM_DELETE_WINDOW", on_close)
  chat_window.mainloop()

login_window = tk.Tk()
login_window.title("Connexion")
login_window.geometry("200x100")

label = tk.Label(login_window, text="Pseudo :")
label.pack()
entry = tk.Entry(login_window)
entry.pack()

button = tk.Button(login_window, text="Se connecter", command=connect)
button.pack()

login_window.mainloop()