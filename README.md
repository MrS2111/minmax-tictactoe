# minmax-tictactoe

1. Peter Kurniawan - 1122013
2. Steven - 1122021
3. Devid Laritsan Manurung - 1122045
4. Calvin Estanto Zendrato - 1123040

## How to Run
1. install module requirements.txt (pip install -r requirements.txt)
2. make sure the path of programs
3. python app.py


### Penjelasan Tentang Algoritma
Minimax adalah sebuah algoritma yang sering digunakan dalam kecerdasan buatan, terutama dalam permainan dua pemain (seperti catur atau tic-tac-toe), untuk menentukan langkah terbaik yang harus diambil oleh pemain. Algoritma ini berfungsi dengan cara mengasumsikan bahwa kedua pemain berusaha untuk memaksimalkan keuntungan mereka sendiri dan meminimalkan keuntungan lawannya.

Penjelasan Minimax:
Tujuan: Minimax berusaha untuk memaksimalkan nilai bagi pemain yang sedang bergerak, sembari meminimalkan nilai yang didapatkan oleh pemain lawan. Pemain bertindak dengan cara memilih langkah yang dapat memberikan hasil terbaik bagi dirinya, mengingat bahwa lawan juga akan berusaha melakukan hal yang sama.

Proses:

Pemain Maksimal (Max): Pemain pertama (biasanya diasumsikan sebagai pemain yang berusaha memaksimalkan keuntungan).
Pemain Minimal (Min): Pemain kedua (biasanya berusaha untuk meminimalkan keuntungan pemain pertama).
Algoritma ini bekerja dengan memodelkan semua kemungkinan langkah yang bisa diambil oleh kedua pemain dalam sebuah pohon keputusan, dan setiap simpul pohon tersebut diberi nilai berdasarkan kondisi permainan di dalamnya (misalnya, menang, kalah, atau seri). Pemain maksimal akan memilih langkah yang memberikan nilai tertinggi, sementara pemain minimal akan memilih langkah yang memberikan nilai terendah.
