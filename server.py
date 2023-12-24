import socket
import json
import threading
import datetime


# Database file
database_file = "laporan.txt"

def load_database():
    try:
        with open(database_file, "r") as file:
            database_data = json.load(file)
        return database_data
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"File {database_file} tidak ditemukan atau tidak berisi JSON valid. Database akan kosong.")
        return {}

database = load_database()

def validate_report(data_json):
    nik_pelapor = data_json.get("NIK Pelapor", "")

    global database
    database = load_database()
    if nik_pelapor not in database:
        return {"status": "tidak valid", "pesan": "NIK pelapor tidak terdaftar"}
    else:
        waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
        jumlah_orang = 2
        return {"status": "valid", "Waktu": waktu, "Nama_pelapor": data_json["Nama Pelapor"], "Jumlah_orang": jumlah_orang}



def handle_client(client_socket):
    try:
        data = client_socket.recv(1024)
        if data:
            report_data = json.loads(data.decode('utf-8'))
            response = validate_report(report_data)
            client_socket.sendall(json.dumps(response).encode('utf-8'))

    finally:
        client_socket.close()



def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 8080))
    server_socket.listen(1)
    print("Server listening on", server_socket.getsockname())

    while True:
        print("Waiting for a connection...")
        client_socket, client_address = server_socket.accept()
        print("Accepted connection from", client_address)
        # Create a thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()



if __name__ == "__main__":
    main()