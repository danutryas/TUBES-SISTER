import socket
import json

def send_report(data):
    # Membuat socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Menentukan alamat server
    server_address = ("localhost", 8080)

    try:
        # Menghubungkan ke server
        client_socket.connect(server_address)

        # Mengirim data ke server
        message = json.dumps(data)
        client_socket.sendall(message.encode('utf-8'))

        # Menerima respons dari server
        response = client_socket.recv(1024)
        print(response.decode('utf-8'))

    finally:
        # Menutup koneksi
        client_socket.close()

def main():
    # Meminta input dari pengguna
    nik_pelapor = input("Masukkan NIK Pelapor: ")
    nama_pelapor = input("Masukkan Nama Pelapor: ")
    nama_terduga = input("Masukkan Nama Terduga Covid: ")
    alamat_terduga = input("Masukkan Alamat Terduga Covid: ")
    gejala = input("Masukkan Gejala: ")

    # Membuat data laporan berdasarkan input pengguna
    report_data = {
        "NIK Pelapor": nik_pelapor,
        "Nama Pelapor": nama_pelapor,
        "Nama Terduga Covid": nama_terduga,
        "Alamat Terduga Covid": alamat_terduga,
        "Gejala": gejala,
    }

    # Mengirim laporan ke server
    send_report(report_data)

if __name__ == "__main__":
    main()