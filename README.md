# Generalized Suffix Tree based Indexing Module

### Requirement
- Python 3.5+
- Apache, MySQL
- Library Python : anytree, pymysql, time, pickle, dan re

### How to use
1. Unduh atau clone repository ini.
2. Jalankan Apache dan MySQL pada XAMPP Anda
3. Import database yang tersedia yaitu page_information.sql pada localhost
4. Install python dan library yang diperlukan. Untuk library dapat diinstall melalui cmd: ```pip install <nama library>```
5. Pastikan nama dan koneksi database sesuai pada fungsi getResult() dan getTitle()
6. Jalankan script gst.py
7. Masukkan kalimat atau kata yang ingin dicari
8. Lihat hasil pada terminal atau console
9. Jika ingin membuat tree dari awal maka hapus file yang bernama gst lalu uncomment 3 line teratas pada fungsi main pada script gst.py
10. Jalankan script gst.py

