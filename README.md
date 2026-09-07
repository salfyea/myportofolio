# My Portofolio

Selamat datang di repositori portofolio pribadi saya!

Repositori ini digunakan untuk mengerjakan seluruh rangkaian tugas dan tutorial mata kuliah **Pemrograman Berbasis Platform (PBP), Gasal 2026/2027** ^-^

<p align="center">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&amp;logo=html5&amp;logoColor=white" alt="HTML5">
  <img src="https://img.shields.io/badge/CSS-663399?style=for-the-badge&amp;logo=css&amp;logoColor=white" alt="CSS">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&amp;logo=python&amp;logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&amp;logo=django&amp;logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&amp;logo=git&amp;logoColor=white" alt="Git">
  <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&amp;logo=github&amp;logoColor=white" alt="GitHub">
</p>

[Identitas](#identitas-diri) · [Tentang Proyek](#tentang-proyek) · [Menjalankan Proyek](#menjalankan-proyek) · [Refleksi Tugas 1](#tugas-1) · [Penggunaan AI](#penggunaan-ai)

---

## Identitas Diri

| Keterangan | Identitas |
| --- | --- |
| Nama | Salwa Alifia Putri |
| NPM | 2506620280 |
| Kelas | PBP A |
| Program Studi | S1 Sistem Informasi |
| Institusi | Universitas Indonesia |

## Tentang Proyek

Website ini menyajikan profil, pengalaman, proyek, dan keahlian saya dalam satu halaman. Proyek dikembangkan bertahap sepanjang semester dengan melanjutkan kode dari tutorial dan tugas sebelumnya

Pada tahap Tugas 1, konten halaman masih ditulis langsung dalam **HTML5** dan tampilannya diatur menggunakan **CSS3**. Django digunakan untuk menyajikan halaman melalui view dan routing sederhana sesuai tutorial. Konten portofolio belum dikelola melalui model database, dan halaman ini tidak menggunakan JavaScript atau framework frontend

### Teknologi dan Fungsinya

| Teknologi | Penggunaan dalam proyek |
| --- | --- |
| HTML5 | Struktur konten dan elemen semantik halaman |
| CSS3 | Warna, tipografi, Grid, Flexbox, media query, dan efek hover |
| Python dan Django | Menjalankan proyek serta menghubungkan URL dengan template |
| Git dan GitHub | Mencatat perubahan kode dan menyimpan repositori untuk pengumpulan |

## Berkas Utama

Struktur berikut mengikuti penempatan berkas pada Tutorial 01:

| Lokasi | Fungsi |
| --- | --- |
| `manage.py` | Menjalankan perintah pengelolaan proyek Django |
| `portofolio/settings.py` | Konfigurasi proyek, template, dan static files |
| `portofolio/urls.py` | Pemetaan URL halaman |
| `portofolio/views.py` | View yang menyajikan template portofolio |
| `templates/index.html` | Struktur dan konten website |
| `static/css/style.css` | Seluruh styling halaman |
| `static/img/SalwaAlifiaPutri.jpeg` | Foto profil yang dirujuk dalam HTML |
| `requirements.txt` | Dependensi Python proyek |
| `README.md` | Dokumentasi dan refleksi mingguan |

## Menjalankan Proyek

Gunakan repositori proyek dari Tutorial 01. Untuk salinan baru, clone repositori melalui alamat pada tombol **Code** di GitHub, lalu buka terminal pada folder yang berisi `manage.py`.

### 1. Siapkan Virtual Environment

Jika folder `env` belum tersedia, jalankan:

```bash
python -m venv env
```

### 2. Aktifkan Virtual Environment

**Windows PowerShell:**

```powershell
.\env\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```bat
env\Scripts\activate.bat
```

**macOS / Linux:**

```bash
source env/bin/activate
```

### 3. Pasang Dependensi

```bash
python -m pip install -r requirements.txt
```

Siapkan konfigurasi environment lokal sesuai Tutorial 0 dan pengaturan pada `settings.py`. Gunakan versi dependensi yang tercantum dalam proyek.

### 4. Periksa dan Jalankan Proyek

```bash
python manage.py check
python manage.py runserver
```

### 5. Buka Website

Akses [http://localhost:8000/](http://localhost:8000/) melalui browser.

Pastikan CSS dan foto profil termuat. Halaman dijalankan melalui server Django, bukan dengan membuka `index.html` langsung dari file manager.

Untuk memperbarui Tugas 1 pada proyek yang sudah berjalan, gunakan versi terbaru `templates/index.html` dan `static/css/style.css`. Setup awal tidak perlu diulang jika environment dan dependensi sudah tersedia.

## Perkembangan Mingguan

| Tahap | Lingkup Pengembangan |
| --- | --- |
| Tutorial 1 | Halaman About Me serta penghubungan view, URL, template, dan static files sesuai tutorial |
| Tugas 1 | Penambahan Experience, Featured Projects, dan Skills; pengembangan styling kartu; serta perbaikan layout mobile agar elemen tidak bertumpuk dan konten lebih mudah dibaca. |

## Refleksi Mingguan

### Tugas 1

1. **Penggunaan elemen semantik HTML5**

   Saya menggunakan elemen semantik HTML5 untuk membagi halaman berdasarkan fungsi kontennya. Elemen `<header>` memuat identitas dan navigasi, `<nav>` mengelompokkan tautan menuju bagian halaman, dan `<main>` menandai konten utama. Bagian Profile, Experience, Featured Projects, dan Skills menggunakan `<section>` karena masing-masing mempunyai tema yang jelas. Setiap bagian juga memiliki heading agar hierarki informasi lebih mudah diikuti.

   Untuk setiap item pengalaman, proyek, dan kelompok keahlian, saya menggunakan `<article>`. Setiap kartu memuat judul dan penjelasan yang tetap dapat dipahami sebagai satu unit informasi. Sementara itu, `<footer>` digunakan untuk informasi penutup. Saya tidak menggunakan `<aside>` karena belum ada konten tambahan yang bersifat pelengkap di luar alur utama portofolio. Elemen `<div>` tetap digunakan untuk pengelompokan layout, seperti container dan grid, yang tidak selalu membutuhkan makna semantik tersendiri.

   Pembagian tersebut membantu saya membaca dan mengembangkan kode tanpa harus menafsirkan fungsi setiap `<div>` dari nama class saja. Struktur yang jelas juga membantu teknologi bantu mengenali bagian navigasi dan konten utama. Namun, elemen semantik tidak otomatis membuat tampilan menjadi rapi atau seluruh halaman menjadi aksesibel. CSS, urutan heading, teks alternatif foto, dan indikator fokus tautan tetap diperlukan. Karena itu, struktur HTML digunakan untuk menjelaskan makna konten, sedangkan CSS digunakan untuk mengatur tampilannya.

2. **Tantangan dan pertimbangan dalam membuat layout responsif**

   Tantangan utama pada kode awal adalah layout profil yang tetap menggunakan dua kolom dan kartu yang tetap menggunakan tiga kolom tanpa media query. Susunan tersebut memberi ruang untuk membaca di desktop, tetapi dapat membuat teks terlalu sempit ketika layar mengecil. Navigasi, pasangan NPM dan program studi, serta dekorasi foto yang bergeser dari batas gambar juga perlu diperhatikan agar tidak menimbulkan elemen yang melebar keluar layar.

   Pada versi revisi, kartu menggunakan tiga kolom di desktop, dua kolom pada lebar layar maksimal 900px, dan satu kolom pada lebar maksimal 600px. Untuk profil di mobile, urutannya menjadi nama, foto, kemudian bio dan informasi kontak. Nama diprioritaskan agar identitas langsung terlihat, sedangkan foto dibatasi ukurannya supaya tidak mendominasi layar. Urutan ini juga mengikuti urutan elemen dalam HTML. Navigasi dan metadata diberi kemampuan membungkus baris, sementara `minmax(0, ...)`, `min-width: 0`, dan `overflow-wrap` membantu mengendalikan konten di dalam grid.

   Dasar evaluasi saya adalah keterbacaan dan prioritas informasi, bukan sekadar mengecilkan semua ukuran secara proporsional. Teks utama perlu tetap nyaman dibaca, tautan perlu mudah dipilih, dan pengguna tidak seharusnya harus menggulir horizontal untuk membaca kartu. Breakpoint tersebut merupakan keputusan desain yang perlu dibuktikan melalui pemeriksaan browser, bukan jaminan bahwa semua ukuran layar sudah sesuai. Evaluasi visual perlu dilakukan pada lebar seperti 375px, 768px, dan 1440px, serta saat teks diperbesar. Pada saat draf dokumentasi ini disusun, pemeriksaan yang tersedia baru mencakup struktur kode; hasil pengujian browser belum dicatat.

3. **Batasan static web dan rencana pengembangan dinamis**

   Batasan utama pada struktur saat ini adalah semua informasi portofolio ditulis langsung dalam HTML. Ketika ada pengalaman, proyek, atau keahlian baru, saya perlu mengubah markup secara manual. Pendekatan ini masih cukup untuk konten yang sedikit, tetapi pengelolaannya menjadi kurang praktis ketika jumlah item bertambah. Pengulangan struktur kartu juga berpotensi menimbulkan ketidakkonsistenan apabila setiap perubahan dilakukan satu per satu.

   Prioritas pengembangan berikutnya adalah pengelolaan data proyek melalui model Django dan antarmuka admin. Data seperti judul, deskripsi, kategori, dan tautan proyek dapat disimpan sebagai field, kemudian diambil oleh view dan ditampilkan melalui perulangan pada template. Dengan demikian, perubahan isi tidak selalu membutuhkan perubahan struktur HTML. CSS kartu yang sudah digunakan kembali pada Tugas 1 dapat dipertahankan ketika sumber datanya menjadi dinamis.

   Fitur tersebut saya prioritaskan karena langsung menjawab kebutuhan pemeliharaan portofolio. Pengembangannya juga memerlukan validasi data, pembatasan akses pengelola, dan penanganan kondisi ketika belum ada proyek. Static web sendiri tetap dapat memiliki interaksi berbasis CSS, seperti hover dan navigasi anchor. Keterbatasan yang saya maksud terutama terletak pada pengelolaan data dan pemrosesan di server. Fitur model dan admin tersebut masih merupakan rencana untuk iterasi berikutnya, belum implementasi pada Tugas 1.

## AI Disclosure

### Peran AI dalam Proses Pembelajaran

Saya menggunakan ChatGPT sebagai pendamping untuk mempelajari syntax HTML/CSS dan memahami cara melakukan debugging pada website portofolio. Bantuan yang diberikan mencakup penjelasan hubungan antara class HTML dan selector CSS, penggunaan Grid dan Flexbox, serta fungsi media query dalam menyesuaikan layout

ChatGPT juga membantu mengidentifikasi masalah dan memberikan contoh revisi kode. Contohnya adalah class `.section-title` yang sudah didefinisikan dalam CSS tetapi belum diterapkan pada heading HTML, serta layout kartu yang belum memiliki pengaturan khusus untuk layar kecil

Dari penjelasan tersebut, saya memahami bahwa debugging perlu dilakukan dengan menelusuri hubungan antara struktur HTML, aturan CSS, dan perilaku yang diharapkan. Menambahkan aturan CSS saja belum cukup apabila selector-nya tidak cocok dengan elemen yang ingin diatur

### Pemahaman yang Dikembangkan

Beberapa konsep yang dibahas selama proses pengerjaan adalah:

- **Hubungan HTML dan CSS:** class pada HTML harus sesuai dengan selector agar styling diterapkan pada elemen yang benar
- **Penggunaan kembali styling:** class `.card` dapat menampung aturan bersama, sedangkan class tambahan mengatur variasi tampilan setiap jenis kartu
- **Responsivitas:** penyesuaian desktop ke mobile perlu mempertimbangkan jumlah kolom, urutan informasi, ukuran foto, dan keterbacaan teks
- **Pemisahan tanggung jawab:** HTML menjelaskan struktur dan makna konten, sedangkan CSS mengatur penyajiannya
- **Aksesibilitas:** indikator fokus keyboard dan pengaturan pengurangan animasi membantu mengakomodasi kebutuhan pengguna yang berbeda

### Evaluasi Kritis terhadap AI

Saran AI dapat menjadi titik awal untuk memahami masalah, tetapi tidak otomatis membuktikan bahwa solusi sudah benar pada proyek yang dijalankan. Sebagai contoh, penambahan media query dapat terlihat tepat ketika dibaca, tetapi tampilannya tetap perlu diperiksa melalui browser. Panjang teks, ukuran gambar, dan lebar layar dapat menghasilkan kondisi yang belum terlihat dari pemeriksaan kode saja. Demikian pula, koreksi HTML/CSS tidak membuktikan bahwa konfigurasi Django dan pemuatan static files sudah berjalan dengan benar. Karena itu, saya membedakan antara penjelasan konsep, usulan perubahan, dan hasil pengujian. Pemahaman konsep perlu diperkuat melalui dokumentasi, sedangkan keberhasilan implementasi perlu dibuktikan dengan menjalankan dan memeriksa website

### Verifikasi dan Perbaikan Manual

- **Masalah yang saya temukan:** Pada tampilan mobile, beberapa elemen saling bertumpuk. Kartu juga terlihat terlalu sempit dan memanjang ke bawah sehingga isinya kurang nyaman dibaca (T-T)
- **Perubahan yang saya lakukan sendiri:** Saya menyesuaikan pengaturan tampilan kartu pada CSS agar susunannya lebih sesuai dengan lebar layar mobile
- **Alasan perubahan:** Penyesuaian dilakukan untuk memperbaiki proporsi kartu, mencegah elemen saling bertumpuk, dan meningkatkan keterbacaan konten pada layar kecil
- **Hasil pemeriksaan:** Setelah diperiksa melalui browser pada tampilan mobile, kartu terlihat lebih proporsional, konten lebih mudah dibaca, dan susunan halaman lebih rapi. Penulisan kode juga sudah dirapikan agar lebih mudah dipahami

### Catatan Penggunaan

Bantuan ChatGPT mencakup penjelasan konsep, identifikasi masalah, contoh revisi HTML/CSS, serta penyusunan awal dokumentasi

## Pemeriksaan Sebelum Pengumpulan

Daftar berikut merupakan verifikasi progress saya. Tanda centang diisi setelah pemeriksaan finalisasi dilakukan

- [✅] Nama, NPM, bio, pengalaman, dan tautan kontak sesuai data pribadi.
- [✅] Foto tersedia dan tampil.
- [✅] `python manage.py check` selesai tanpa masalah konfigurasi.
- [✅] `python manage.py runserver` berhasil dan halaman dapat diakses.
- [✅] CSS termuat serta tampilan diperiksa pada desktop, tablet, dan mobile.
- [✅] Tidak ada scroll horizontal yang tidak diperlukan; seluruh navigasi berfungsi.
- [✅] Fokus keyboard terlihat dan teks tetap terbaca ketika diperbesar.
- [✅] Jawaban reflektif sudah disesuaikan dengan pemahaman serta pengalaman pribadi.
- [✅] AI disclosure, log prompting, dan catatan pengujian sesuai proses yang sebenarnya.
- [✅] Commit terbaru sudah di-push dan tautan commit publik dapat dibuka melalui mode Incognito.

## Referensi
- [Django — menjalankan development server](https://docs.djangoproject.com/en/5.2/intro/tutorial01/#the-development-server). Gunakan dokumentasi versi yang sesuai dengan dependensi proyek.
- [Shields.io — Static Badge](https://shields.io/badges/static-badge), untuk badge teknologi pada README.
