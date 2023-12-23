import socket
import json
import time
import multiprocessing  # For IPC

queue = multiprocessing.Queue()


# Nama file database
database_file = "laporan.txt"

def load_database():
    try:
        with open(database_file, "r") as file:
            database_data = json.load(file)
        return database_data
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"File {database_file} tidak ditemukan atau tidak berisi JSON valid. Database akan kosong.")
        return {}

# Database berisi NIK pelapor yang valid
database = load_database()

def save_database():
    with open(database_file, "w") as file:
        json.dump(database, file)

def validate_report(data_json):
    nik_pelapor = data_json.get("NIK Pelapor", "")

    # Muat ulang database dari file sebelum memproses laporan
    global database
    database = load_database()

    if nik_pelapor not in database:
        return {"response": "Laporan tidak valid"}
    else:
        # Proses laporan valid, buat respon dengan informasi penjemputan
        waktu = time.strftime("%Y-%m-%d %H:%M:%S")
        jumlah_orang = 2  # Misalnya, jumlah orang yang akan melakukan penjemputan

        respon = {
            "response": "Laporan valid",
            "Waktu_Penjemputan": waktu,
            "Nama_pelapor": database[nik_pelapor]["Nama Pelapor"],
            "Jumlah_orang": jumlah_orang,
        }
        return respon

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8080)  # Sesuaikan dengan alamat dan port server

    server_socket.bind(server_address)
    server_socket.listen(1)

    print("Server listening on", server_address)

    while True:
        print("Waiting for a connection...")
        client_socket, client_address = server_socket.accept()
        print("Accepted connection from", client_address)

        try:
            data = client_socket.recv(1024)
            if data:
                report_data = json.loads(data.decode('utf-8'))
                # response = validate_report(report_data)
                # client_socket.sendall(json.dumps(response).encode('utf-8'))
                queue.put(report_data)  # Send data to database manager
                response = queue.get()  # Receive response from database manager
                client_socket.sendall(json.dumps(response).encode('utf-8'))

        finally:
            client_socket.close()


if __name__ == "__main__":
    start_server()