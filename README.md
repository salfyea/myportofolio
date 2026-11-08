# My Portofolio

Selamat datang di repositori portofolio pribadi saya!

Repositori ini digunakan untuk mengerjakan seluruh rangkaian tugas dan tutorial mata kuliah **Pemrograman Berbasis Platform (PBP), Gasal 2026/2027** ^-^

<p align="center">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&amp;logo=html5&amp;logoColor=white" alt="HTML5">
  <img src="https://img.shields.io/badge/CSS-663399?style=for-the-badge&amp;logo=css&amp;logoColor=white" alt="CSS">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&amp;logo=javascript&amp;logoColor=black" alt="JavaScript">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&amp;logo=python&amp;logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&amp;logo=django&amp;logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&amp;logo=git&amp;logoColor=white" alt="Git">
  <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&amp;logo=github&amp;logoColor=white" alt="GitHub">
</p>

<p align="center">
  <a href="https://github.com/salfyea/myportofolio/actions/workflows/ci.yml"><img src="https://github.com/salfyea/myportofolio/actions/workflows/ci.yml/badge.svg" alt="Status CI"></a>
</p>

[Identitas](#identitas-diri) · [Tentang Proyek](#tentang-proyek) · [Perkembangan](#perkembangan-proyek) · [Menjalankan Proyek](#menjalankan-proyek) · [Refleksi Mingguan](#refleksi-mingguan) · [Penggunaan AI](#penggunaan-ai)

---

## Identitas Diri

| Keterangan | Identitas |
| --- | --- |
| Nama | Salwa Alifia Putri |
| NPM | 2506620280 |
| Kelas | PBP A |
| Program Studi | S1 Sistem Informasi |
| Institusi | Universitas Indonesia |

---

## Tentang Proyek

Website ini merupakan portofolio pribadi yang menampilkan profil, pengalaman, proyek, dan keahlian saya dalam satu aplikasi web.

Proyek ini dikerjakan secara **bertahap sepanjang semester** dengan melanjutkan hasil dari tutorial dan tugas sebelumnya. Karena itu, README ini juga diperlakukan sebagai dokumentasi yang terus berkembang: setiap tugas baru akan menambahkan fitur, refleksi, catatan implementasi, serta pembaruan setup tanpa menghilangkan riwayat perkembangan sebelumnya.

Pada tahap awal, portofolio masih bersifat statis. Seiring bertambahnya materi Django, project berkembang menjadi aplikasi yang menggunakan **Model-View-Template (MVT)**, database, form, CRUD, JSON API, fitur interaktif, **sistem autentikasi dan otorisasi berbasis peran**, serta **AJAX dengan JavaScript** untuk memuat dan menambah data tanpa me-reload halaman.

### Arah Perkembangan Proyek

```text
Static Portfolio
      ↓
Django MVT
      ↓
Database-backed Content
      ↓
Dynamic Projects & Skills
      ↓
ModelForm + CRUD
      ↓
JSON Delivery
      ↓
Interactive Frontend
      ↓
Authentication, Session & Cookie
      ↓
Role-based Authorization
      ↓
AJAX, Toast & Perlindungan XSS
      ↓
Fitur tambahan & pengembangan berikutnya
```

### Teknologi dan Fungsinya

| Teknologi | Penggunaan dalam proyek |
| --- | --- |
| **HTML5** | Struktur konten dan elemen semantik halaman |
| **CSS3** | Warna, tipografi, Grid, Flexbox, media query, dan efek hover |
| **JavaScript** | Interaksi frontend: AJAX dengan Fetch API, debouncing pencarian, modal dengan Popover API, dan notifikasi toast |
| **Python** | Bahasa pemrograman backend |
| **Django** | Routing, view, model, ORM, form, template, session, autentikasi, otorisasi, dan respons JSON |
| **Django Auth & Groups** | Sistem akun bawaan Django serta pembagian peran pengguna |
| **Git** | Mencatat perubahan kode dan membantu pengembangan bertahap |
| **GitHub** | Menyimpan repositori, Pull Request, dan dokumentasi proyek |
| **Google Gemini API** | Mendukung fitur AI Chat Widget melalui backend |

---

## Perkembangan Proyek

Bagian ini akan terus diperbarui sampai akhir rangkaian tugas.

| Tahap | Lingkup Pengembangan |
| --- | --- |
| **Tutorial 1** | Halaman About Me serta penghubungan view, URL, template, dan static files sesuai tutorial. |
| **Tutorial 2** | Implementasi konsep MVT Django melalui model `Experience`, migration database, queryset pada view, template dinamis, routing URL, base template, serta unit testing. |
| **Tugas 1** | Penambahan Experience, Featured Projects, dan Skills, pengembangan styling kartu, serta perbaikan layout mobile agar elemen tidak bertumpuk dan konten lebih mudah dibaca. |
| **Tugas 2** | Pengembangan Featured Projects berbasis database menggunakan model `Project`, migration, fixture, queryset, halaman Projects terpisah, navigasi, template dinamis dengan empty state, serta pengujian fitur. |
| **Tutorial 3** | Pembuatan skeleton `base.html` sebagai root template, penerapan `ModelForm` untuk `Project`, serta implementasi create, update, delete, dan JSON delivery untuk `Project`. |
| **Tugas 3** | Refactor template agar extend dari `base.html`, pembuatan model `Skill` yang menggantikan data Skills hardcoded, `ModelForm`, create, update, delete, JSON delivery, dan penampilan data hasil deserialisasi JSON secara langsung pada halaman kelola Skills. |
| **Tutorial 4** | Implementasi autentikasi bawaan Django (register, login, logout), penanda status login pada navbar, cookie `last_login` beserta penghapusannya saat logout, pembatasan create dan delete `Project` untuk pemilik portofolio, fitur star pada `Project` menggunakan `ManyToManyField`, serta pengamanan endpoint JSON dengan natural key. |
| **Tugas 4** | Penerapan pola autentikasi dan otorisasi pada bagian `Skill`: penambahan peran **Editor** melalui Django Group, pembatasan hak akses sisi server untuk empat peran, penyembunyian kontrol aksi pada template sesuai peran, fitur star pada `Skill`, serta penggantian proteksi kode rahasia dengan sistem otorisasi Django. |
| **Tutorial 5** | Penerapan JavaScript dan AJAX pada halaman Projects: komponen notifikasi toast, pemuatan data proyek lewat Fetch API dengan JSON yang dirakit manual (termasuk jumlah dan status star), state loading, kosong, dan error, pencarian dengan debouncing, modal form tambah proyek, pengiriman form lewat AJAX dengan token CSRF, serta perlindungan XSS di sisi tampilan dan server. |
| **Tugas 5** | Penerapan seluruh pola Tutorial 5 pada bagian `Skill`: tabel skill dimuat lewat AJAX beserta jumlah dan status star, pencarian berdasarkan nama dengan debouncing, tambah skill lewat modal dan `fetch` dengan respons 201, 400, dan 403, toast untuk keberhasilan maupun kegagalan, pembersihan input dengan `strip_tags`, serta pemindahan `getCookie` ke berkas JavaScript bersama. |
| **Tutorial 6** | Latihan HTMX pada app terpisah `contacts`: model `Contact`, partial template, tambah, hapus, pencarian langsung dengan debouncing, dan edit di dalam baris tabel memakai atribut `hx-*`, ditambah tiga latihan (field `phone`, `hx-swap="beforeend"`, dan feedback lewat `hx-swap-oob`). |
| **Tutorial 7** | Implementasi Django REST Framework pada `Project`: `ProjectSerializer` dengan validasi dan field star hasil perhitungan, permission class `IsPortfolioOwnerOrReadOnly` dan `IsPortfolioOwnerOrEditorOrReadOnly`, API view berbasis fungsi di bawah `/api/v1/`, endpoint star, halaman Projects yang memakai API baru, serta 13 test dengan `APITestCase` termasuk pemeriksaan CSRF. |
| **Tugas 6** | Penerapan pola Django REST Framework pada bagian `Skill`: `SkillSerializer` dengan validasi `strip_tags` dan field star read-only, permission `IsPortfolioOwnerOrEditorOrReadOnly` untuk empat peran, API view berbasis fungsi di `/api/v1/skills/`, halaman kelola Skills yang menampilkan, mencari, menambah, memberi star, mengedit (`PATCH`), dan menghapus lewat API, filter kategori dan urutan star sebagai fitur tambahan, 31 test Skill termasuk pemeriksaan CSRF, GitHub Actions CI, penguatan keamanan (rate limiting, throttle API, pengaturan produksi), modul JavaScript dengan star optimistis, dan 185 test dengan coverage 99%. |
| **Tugas berikutnya** | Akan ditambahkan pada bagian ini beserta perubahan fitur, konsep yang dipelajari, dan catatan implementasinya. |

### Timeline Implementasi

```mermaid
flowchart LR
    A[Tutorial 1<br/>HTML + CSS + Django dasar]
    B[Tutorial 2<br/>MVT + Model Experience]
    C[Tugas 1<br/>Responsive Portfolio]
    D[Tugas 2<br/>Project Database]
    E[Tutorial 3<br/>ModelForm + CRUD + JSON]
    F[Tugas 3<br/>Skill + CRUD + Live JSON]
    G[Tutorial 4<br/>Auth + Session + Cookie]
    H[Tugas 4<br/>Role-based Authorization]
    I[Tutorial 5<br/>AJAX + Toast + XSS]
    J[Tugas 5<br/>AJAX pada Skill]
    K[Tutorial 6<br/>HTMX pada app contacts]
    L[Tutorial 7<br/>Django REST Framework]
    M[Tugas 6<br/>DRF pada Skill]
    N[Tugas Berikutnya<br/>Pengembangan lanjutan]

    A --> B --> C --> D --> E --> F --> G --> H --> I --> J --> K --> L --> M --> N
```

---

## Berkas Utama

Struktur berkas akan berkembang seiring bertambahnya fitur, tetapi tanggung jawab utamanya tetap dipisahkan agar mudah dipahami.

| Lokasi | Fungsi |
| --- | --- |
| `manage.py` | Menjalankan perintah pengelolaan proyek Django |
| `portofolio/settings.py` | Konfigurasi proyek, template, static files, dan pengaturan lainnya |
| `portofolio/urls.py` | Pemetaan URL utama proyek |
| `main/urls.py` | Pemetaan URL aplikasi, termasuk rute autentikasi, star, dan endpoint AJAX |
| `main/models.py` | Definisi model dan struktur data, termasuk relasi star ke `User` |
| `main/views.py` | Logika request dan response, termasuk pemeriksaan hak akses dan endpoint JSON untuk AJAX |
| `main/forms.py` | Definisi `ModelForm` beserta pembersihan input dengan `strip_tags` |
| `main/migrations/` | Riwayat perubahan struktur database, termasuk data migration grup `Editor` |
| `main/tests.py` | Pengujian fitur |
| `templates/` | HTML template |
| `templates/components/` | Komponen template yang dipakai ulang: toast, modal form tambah project dan skill, serta modal hapus |
| `static/` | CSS, gambar, dan aset statis |
| `static/js/toast.js` | Fungsi `showToast` untuk notifikasi singkat yang dimuat dari `base.html` |
| `static/js/utils.js` | Fungsi bantu lintas halaman, saat ini `getCookie` untuk membaca token CSRF |
| `requirements.txt` | Dependensi Python |
| `README.md` | Dokumentasi proyek, progres, refleksi, dan penggunaan AI |

---

## Arsitektur Aplikasi

Proyek menggunakan pola **Model-View-Template (MVT)** Django.

```mermaid
flowchart TD
    U[Pengguna / Browser]

    U --> R[URL Routing]
    R --> V[Django View]

    V --> M[Model / Django ORM]
    M --> DB[(Database)]

    V --> T[Template]
    T --> H[HTML + CSS + JavaScript]
    H --> U

    V --> API[JSON Endpoint]
    API --> U
```

Secara sederhana, terdapat dua jalur utama:

### Server-rendered page

```text
Browser
   ↓
urls.py
   ↓
View
   ↓
Model / ORM
   ↓
Database
   ↓
Template
   ↓
HTML Response
   ↓
Browser
```

### JSON delivery

```text
Browser
   ↓
GET /api/skills/
   ↓
Django View
   ↓
Django ORM
   ↓
QuerySet
   ↓
Dirakit manual menjadi dictionary
   ↓
JsonResponse
   ↓
JavaScript
   ↓
DOM
```

Sejak Tutorial 5, JSON tidak lagi dibuat dengan `serializers.serialize`, melainkan dirakit manual agar dapat menyertakan informasi yang bergantung pada pengguna yang sedang login, seperti status star.

### Session dan Pengenalan Pengguna

HTTP bersifat *stateless*, sehingga server tidak otomatis mengingat siapa yang mengirim request sebelumnya. Django menjembatani hal ini dengan menyimpan data sesi di sisi server dan mengirim token `sessionid` ke browser melalui cookie.

```mermaid
sequenceDiagram
    participant B as Browser
    participant D as Django
    participant DB as django_session

    B->>D: POST /login/ (username + password)
    D->>D: Verifikasi kredensial
    D->>DB: Simpan data sesi
    D-->>B: Set-Cookie sessionid + last_login
    B->>D: Request berikutnya (cookie otomatis disertakan)
    D->>DB: Cocokkan sessionid
    D-->>B: Kenali request.user
```

Cookie hanya menyimpan token acak, bukan data sensitif. Data sesi yang sebenarnya tetap berada di sisi server.

### Pembagian Hak Akses

```mermaid
flowchart TD
    R[Request aksi tulis]
    L{Sudah login?}
    S{Superuser?}
    E{Anggota grup Editor?}
    U{Jenis aksi?}

    R --> L
    L -->|Tidak| RED[Redirect ke /login/]
    L -->|Ya| S
    S -->|Ya| OK[Aksi diizinkan]
    S -->|Tidak| U
    U -->|Update| E
    U -->|Create / Delete| F[403 Forbidden]
    E -->|Ya| OK
    E -->|Tidak| F
```

### AJAX pada Halaman Daftar

Mulai Tutorial 5, halaman Projects dan halaman kelola Skills tidak lagi dirender penuh oleh Django. Django hanya mengirim kerangka halaman, lalu JavaScript mengambil datanya sendiri.

**Menampilkan data:**

```mermaid
sequenceDiagram
    participant B as Browser
    participant D as Django

    B->>D: GET /skills/manage/
    D-->>B: Kerangka halaman tanpa data
    B->>D: fetch GET /api/skills/?name=...
    D->>D: Susun JSON, hitung star_count dan is_starred
    D-->>B: 200 + JSON
    B->>B: Rakit baris tabel dengan textContent
```

**Menambah data lewat modal:**

```mermaid
sequenceDiagram
    participant U as Superuser
    participant B as Browser
    participant D as Django

    U->>B: Isi form di modal lalu submit
    B->>D: POST /skills/add-ajax/ + X-CSRFToken
    D->>D: Cek CSRF dan is_superuser, validasi ModelForm
    alt Bukan superuser
        D-->>B: 403 + pesan
        B-->>U: Toast merah
    else Data tidak valid
        D-->>B: 400 + daftar error
        B-->>U: Toast merah berisi pesan validasi
    else Data valid
        D-->>B: 201 + pk
        B-->>U: Modal tertutup, toast hijau, daftar dimuat ulang
    end
```

---

# Menjalankan Proyek

## 1. Clone Repository

Clone repository dari GitHub, kemudian buka terminal pada folder yang berisi `manage.py`.

```bash
git clone <repository-url>
cd <project-folder>
```

## 2. Siapkan Virtual Environment

Jika folder `env` belum tersedia:

```bash
python -m venv env
```

## 3. Aktifkan Virtual Environment

### Windows PowerShell

```powershell
.\env\Scripts\Activate.ps1
```

### Windows Command Prompt

```bat
env\Scripts\activate.bat
```

### macOS / Linux

```bash
source env/bin/activate
```

## 4. Pasang Dependensi

```bash
python -m pip install -r requirements.txt
```

Untuk menjalankan test lengkap (termasuk Selenium dan laporan coverage), pasang dependensi pengembangan:

```bash
python -m pip install -r requirements-dev.txt
python -m coverage run manage.py test main contacts
python -m coverage report
```

Test Selenium membutuhkan Google Chrome dan dilewati otomatis kalau Chrome tidak ada.

## 5. Siapkan Environment Variable

Konfigurasi lokal mengikuti kebutuhan project dan `settings.py`.

Contoh nilai sensitif yang **tidak boleh ditulis langsung ke source code**:

```text
SECRET_KEY=...
GEMINI_API_KEY=...
```

Gunakan environment variable lokal atau mekanisme secret yang disediakan platform deployment.

> Jangan commit file `.env`, API key, password, atau secret key ke repository publik.

## 6. Jalankan Pemeriksaan Django

```bash
python manage.py check
```

## 7. Terapkan Migration

```bash
python manage.py migrate
```

Perintah ini sekaligus membuat grup **Editor** melalui *data migration*, sehingga peran tersebut tersedia secara otomatis pada setiap salinan project tanpa perlu dibuat manual lebih dulu.

## 8. Siapkan Akun untuk Menguji Peran

Buat akun pemilik portofolio:

```bash
python manage.py createsuperuser
```

Untuk menguji seluruh peran, daftarkan dua akun tambahan melalui halaman `/register/`:

- satu akun dibiarkan sebagai **pengguna biasa**
- satu akun dijadikan **Editor** dengan cara masuk ke `/admin/` sebagai superuser, membuka **Users**, memilih akun tersebut, lalu memindahkan grup **Editor** ke kolom *Chosen groups* dan menyimpannya.

Keanggotaan grup tersimpan di database, sedangkan `db.sqlite3` tidak ikut di-commit. Karena itu grup `Editor` dibuat lewat migration, tetapi pengisian anggotanya tetap dilakukan melalui Django Admin.

### Pembagian Hak Akses

| Peran | Baca | Star | Ubah | Tambah / Hapus |
| --- | --- | --- | --- | --- |
| Pengunjung (belum login) | Ya | Tidak | Tidak | Tidak |
| Pengguna terdaftar | Ya | Ya | Tidak | Tidak |
| Editor | Ya | Ya | Ya | Tidak |
| Pemilik portofolio (superuser) | Ya | Ya | Ya | Ya |

Pengunjung yang belum login diarahkan ke halaman login, sedangkan pengguna yang sudah login tetapi tidak berhak menerima respons **403 Forbidden**.

## 9. Jalankan Development Server

```bash
python manage.py runserver
```

Kemudian buka:

```text
http://localhost:8000/
```

Pastikan CSS, gambar, template, dan fitur yang memerlukan backend berjalan melalui server Django, bukan dengan membuka file HTML langsung dari file manager.

## 10. Coba Fitur AJAX

Setelah server berjalan, fitur interaktif minggu ini dapat dicoba pada halaman berikut:

| Alamat | Yang bisa dicoba |
| --- | --- |
| `/projects/` | Data dimuat lewat AJAX. Ketik di kotak Cari untuk melihat debouncing, dan tambah project lewat modal (khusus superuser). |
| `/skills/manage/` | Tabel skill dimuat lewat AJAX, dicari berdasarkan nama, dan ditambah lewat modal (khusus superuser). |
| `/api/v1/skills/` dan `/api/v1/projects/` | Browsable API dari Django REST Framework. Buka di browser, login lewat tautan di pojok kanan atas, lalu coba `POST`, `PATCH`, dan `DELETE` sesuai peran akun. |
| `/api/projects/` dan `/api/skills/` | Melihat JSON mentahnya, termasuk `star_count` dan `is_starred`. Nilai `is_starred` bergantung pada akun yang sedang login. |

### Setup Mingguan

Karena repository ini akan terus dikembangkan, setup awal tidak perlu diulang setiap minggu selama virtual environment dan dependensi masih tersedia.

Untuk perubahan fitur, alur yang disarankan:

```text
Tarik perubahan terbaru
        ↓
Aktifkan virtual environment
        ↓
Install dependency baru (jika ada)
        ↓
python manage.py check
        ↓
python manage.py migrate (jika ada perubahan model)
        ↓
python manage.py test main contacts
        ↓
python manage.py runserver
```

Perintah yang sama dijalankan otomatis oleh GitHub Actions pada setiap `push` dan *pull request* ke `main` (lihat poin 8 pada Catatan Implementasi Tugas 6). Secara lokal gunakan `python manage.py test main contacts`. Test Selenium dilewati otomatis kalau Chrome tidak terpasang.

---

# Refleksi Mingguan

### Tugas 1

1. **Penggunaan elemen semantik HTML5**

   Saya menggunakan elemen semantik HTML5 untuk membagi halaman berdasarkan fungsi kontennya. Elemen `<header>` memuat identitas dan navigasi, `<nav>` mengelompokkan tautan menuju bagian halaman, dan `<main>` menandai konten utama. Bagian Profile, Experience, Featured Projects, dan Skills menggunakan `<section>` karena masing-masing mempunyai tema yang jelas. Setiap bagian juga memiliki heading agar hierarki informasi lebih mudah diikuti.

   Untuk setiap item pengalaman, proyek, dan kelompok keahlian, saya menggunakan `<article>`. Setiap kartu memuat judul dan penjelasan yang tetap dapat dipahami sebagai satu unit informasi. Sementara itu, `<footer>` digunakan untuk informasi penutup. Saya tidak menggunakan `<aside>` karena belum ada konten tambahan yang bersifat pelengkap di luar alur utama portofolio. Elemen `<div>` tetap digunakan untuk pengelompokan layout, seperti container dan grid, yang tidak selalu membutuhkan makna semantik tersendiri.

   Pembagian tersebut membantu saya membaca dan mengembangkan kode tanpa harus menafsirkan fungsi setiap `<div>` dari nama class saja. Struktur yang jelas juga membantu teknologi bantu mengenali bagian navigasi dan konten utama. Namun, elemen semantik tidak otomatis membuat tampilan menjadi rapi atau seluruh halaman menjadi aksesibel. CSS, urutan heading, teks alternatif foto, dan indikator fokus tautan tetap diperlukan. Karena itu, struktur HTML digunakan untuk menjelaskan makna konten, sedangkan CSS digunakan untuk mengatur tampilannya.

2. **Tantangan dan pertimbangan dalam membuat layout responsif**

   Tantangan utama pada kode awal adalah layout profil yang tetap menggunakan dua kolom dan kartu yang tetap menggunakan tiga kolom tanpa media query. Susunan tersebut memberi ruang untuk membaca di desktop, tetapi dapat membuat teks terlalu sempit ketika layar mengecil. Navigasi, pasangan NPM dan program studi, serta dekorasi foto yang bergeser dari batas gambar juga perlu diperhatikan agar tidak menimbulkan elemen yang melebar keluar layar.

   Pada versi revisi, kartu menggunakan tiga kolom di desktop, dua kolom pada lebar layar maksimal 900px, dan satu kolom pada lebar maksimal 600px. Untuk profil di mobile, urutannya menjadi nama, foto, kemudian bio dan informasi kontak. Nama diprioritaskan agar identitas langsung terlihat, sedangkan foto dibatasi ukurannya supaya tidak mendominasi layar. Urutan ini juga mengikuti urutan elemen dalam HTML. Navigasi dan metadata diberi kemampuan membungkus baris, sementara `minmax(0, ...)`, `min-width: 0`, dan `overflow-wrap` membantu mengendalikan konten di dalam grid.

   Dasar evaluasi saya adalah keterbacaan dan prioritas informasi, bukan sekadar mengecilkan semua ukuran secara proporsional. Teks utama perlu tetap nyaman dibaca, tautan perlu mudah dipilih, dan pengguna tidak seharusnya harus menggulir horizontal untuk membaca kartu. Breakpoint tersebut merupakan keputusan desain yang perlu dibuktikan melalui pemeriksaan browser, bukan jaminan bahwa semua ukuran layar sudah sesuai. Evaluasi visual perlu dilakukan pada lebar seperti 375px, 768px, dan 1440px, serta saat teks diperbesar. Pada saat draf dokumentasi ini disusun, pemeriksaan yang tersedia baru mencakup struktur kode, sedangkan hasil pengujian browser belum dicatat.

3. **Batasan static web dan rencana pengembangan dinamis**

   Batasan utama pada struktur saat ini adalah semua informasi portofolio ditulis langsung dalam HTML. Ketika ada pengalaman, proyek, atau keahlian baru, saya perlu mengubah markup secara manual. Pendekatan ini masih cukup untuk konten yang sedikit, tetapi pengelolaannya menjadi kurang praktis ketika jumlah item bertambah. Pengulangan struktur kartu juga berpotensi menimbulkan ketidakkonsistenan apabila setiap perubahan dilakukan satu per satu.

   Prioritas pengembangan berikutnya adalah pengelolaan data proyek melalui model Django dan antarmuka admin. Data seperti judul, deskripsi, kategori, dan tautan proyek dapat disimpan sebagai field, kemudian diambil oleh view dan ditampilkan melalui perulangan pada template. Dengan demikian, perubahan isi tidak selalu membutuhkan perubahan struktur HTML. CSS kartu yang sudah digunakan kembali pada Tugas 1 dapat dipertahankan ketika sumber datanya menjadi dinamis.

   Fitur tersebut saya prioritaskan karena langsung menjawab kebutuhan pemeliharaan portofolio. Pengembangannya juga memerlukan validasi data, pembatasan akses pengelola, dan penanganan kondisi ketika belum ada proyek. Static web sendiri tetap dapat memiliki interaksi berbasis CSS, seperti hover dan navigasi anchor. Keterbatasan yang saya maksud terutama terletak pada pengelolaan data dan pemrosesan di server. Pada Tugas 2, rencana tersebut sudah diimplementasikan. Data project kini disimpan dalam model Django, diambil melalui view, ditampilkan secara dinamis pada template Projects, dan dapat dikelola melalui database atau Django Admin.

### Tugas 2

1. **Alur yang terjadi ketika pengguna membuka halaman portofolio baru**

   Ketika pengguna membuka halaman portofolio baru, browser mengirimkan HTTP request ke alamat website. Request tersebut pertama kali diterima oleh proyek Django melalui `urls.py` utama yang berada di folder konfigurasi proyek. Berkas ini berfungsi sebagai pintu masuk routing dan menentukan aplikasi mana yang menangani URL tersebut.

   Selanjutnya, `urls.py` proyek meneruskan request ke `urls.py` milik aplikasi `main`. Pada berkas ini, URL seperti `/projects/` dihubungkan dengan fungsi view menggunakan nama rute `show_projects`.

   View `show_projects` kemudian menjalankan logika aplikasi. View mengambil data project dari database melalui model `Project` menggunakan Django ORM, misalnya dengan perintah `Project.objects.all()`. Hasil query tersebut disimpan dalam sebuah queryset dan dikirimkan ke template melalui context dengan nama `project_list`.

   Template `projects.html` menerima context tersebut dan menampilkan data menggunakan perulangan Django Template Language. Setiap object project ditampilkan sebagai sebuah kartu yang berisi nama project, kategori, dan deskripsinya. Jika database belum memiliki data project, template menampilkan pesan empty state yang memberi tahu pengguna bahwa belum ada project yang tersedia.

   Setelah template selesai diproses, Django menggabungkan struktur HTML dengan data dari database. Django kemudian mengirimkan HTML tersebut sebagai HTTP response ke browser. Browser membaca HTML dan CSS, lalu menampilkan halaman Projects yang dapat dilihat oleh pengguna.

   Secara keseluruhan, alurnya adalah:

   `Browser → urls.py proyek → urls.py aplikasi → view → model/database → template → HTTP response → browser`

   Pada alur ini, `urls.py` mengatur tujuan request, view mengatur logika pengambilan data, model menjadi penghubung dengan database, dan template mengatur tampilan akhir halaman ^^

2. **Mengapa data untuk bagian portofolio baru sebaiknya disimpan pada model dan tidak ditulis langsung di dalam template**

   Data portofolio sebaiknya disimpan pada model karena data tersebut merupakan isi aplikasi, bukan bagian dari struktur tampilan. Template seharusnya hanya mengatur bagaimana data ditampilkan. Dengan pemisahan ini, kode menjadi lebih teratur dan mengikuti konsep Model-View-Template pada Django.

   Jika data project ditulis langsung di dalam template, setiap perubahan kecil seperti mengganti nama project, memperbarui deskripsi, atau menambahkan project baru mengharuskan developer mengubah kode HTML. Cara ini tidak efisien dan dapat meningkatkan risiko kesalahan, terutama ketika jumlah data semakin banyak.

   Dengan menggunakan model, data project tersimpan di database dan dapat dikelola secara terpisah dari template. Data dapat ditambahkan, diubah, atau dihapus melalui Django Admin atau database tanpa mengubah struktur HTML. Template cukup menggunakan perulangan untuk menampilkan semua data yang tersedia.

   Penyimpanan melalui model juga membuat aplikasi lebih mudah dikembangkan. Misalnya, model `Project` dapat ditambahkan field baru seperti tahun project, teknologi yang digunakan, gambar, tautan repository, atau status project. View dan template kemudian dapat dikembangkan untuk menampilkan informasi tersebut tanpa menulis kartu HTML satu per satuuu

   Pendekatan ini juga mendukung penggunaan ulang data. Data project yang sama dapat ditampilkan pada halaman Projects, halaman Profile, dashboard admin, atau endpoint API. Jika data ditulis langsung di template, penggunaan ulang seperti ini akan lebih sulit.

   Dari sisi pemeliharaan, model membuat perubahan data lebih aman, terpusat, dan konsisten. Template menjadi lebih bersih karena hanya berisi struktur tampilan. Pemisahan antara data, logika, dan tampilan juga membuat proses pengujian lebih mudah. Developer dapat menguji model, view, dan template secara terpisah.

   Jadi, model membantu aplikasi menjadi lebih fleksibel, mudah dirawat, mudah dikembangkan, dan mampu menangani data yang terus bertambah :D

3. **Apa perbedaan fungsi `makemigrations` dan `migrate` pada Django?**

   `makemigrations` digunakan untuk membuat file migration berdasarkan perubahan yang dilakukan pada model. Perintah ini hanya mencatat perubahan struktur database dalam bentuk instruksi yang dapat dijalankan Django. Perintah ini belum mengubah database secara langsung. Sementara itu, `migrate` digunakan untuk menjalankan file migration ke database. Perintah ini benar-benar membuat, mengubah, atau menghapus tabel dan kolom sesuai instruksi yang ada di file migration

   Contohnya, ketika saya menambahkan model `Project` pada `main/models.py`, saya menjalankan `python manage.py makemigrations` untuk membuat berkas migration yang mencatat struktur model baru. Setelah itu, saya menjalankan `python manage.py migrate` untuk menerapkan migration tersebut sehingga tabel Project tersedia di database

   Kedua perintah tersebut juga diperlukan ketika menambahkan field baru, misalnya field `github_url` bertipe `URLField` pada model `Project`. Ini hanya contoh perubahan struktur model. Menambahkan atau mengubah isi data project melalui Django Admin tidak memerlukan migration karena struktur tabelnya tetap samaaa


### Tugas 3

1. **Mengapa menggunakan `ModelForm` dan mengapa perlu `{% csrf_token %}`?**

   Saya menggunakan `ModelForm` daripada membuat form HTML manual karena field form dapat mengikuti definisi model yang sudah dibuat

   Dengan pendekatan ini, Django dapat membantu membuat field dan validasi berdasarkan tipe field pada model. Misalnya, `URLField` dapat melakukan validasi terkait format URL dan `CharField` mengikuti batas `max_length`

   `ModelForm` juga menyediakan `save()` untuk membuat atau memperbarui instance model. Saya tidak perlu menulis ulang seluruh proses pemetaan data dari `request.POST` ke object model

   Dengan kata lain seperti inii

   ```text
   Model
   ↓
   ModelForm
   ↓
   Validasi
   ↓
   save()
   ↓
   Database
   ```

   Pendekatan ini mengurangi duplikasi aturan data dan membantu menjaga model sebagai sumber utama definisi struktur data

   ### CSRF Protection

   Form yang melakukan perubahan data menggunakan `POST`, misalnya

   ```text
   Create
   Update
   Delete
   ```

   Karena itu saya menambahkan

   ```django
   {% csrf_token %}
   ```

   CSRF protection membantu Django memverifikasi bahwa request perubahan data berasal dari form yang sesuai dengan aplikasi, sehingga aplikasi memiliki perlindungan terhadap pola serangan **Cross-Site Request Forgery**

   ```mermaid
   sequenceDiagram
      participant U as User
      participant B as Browser
      participant D as Django

      U->>B: Submit form
      B->>D: POST + CSRF token
      D->>D: Verifikasi token

      alt Token valid
         D->>D: Proses perubahan data
         D-->>B: Response berhasil
      else Token tidak valid
         D-->>B: Request ditolak
      end
   ```
2. **Mengapa JSON digunakan dibandingkan XML?**

   Dalam project ini, JSON lebih praktis untuk komunikasi antara backend Django dan JavaScript karena strukturnya menggunakan object dan array yang mudah diproses oleh JavaScript

   Contoh:

   ```json
   {
   "name": "Python",
   "level": "Advanced"
   }
   ```

   Di sisi frontend, response dapat diproses dengan

   ```javascript
   fetch("/api/skills/")
   .then(response => response.json())
   .then(data => {
         // data digunakan untuk render ke halaman
   });
   ```

   JSON juga memiliki sintaks yang lebih ringkas dibandingkan XML untuk struktur data sederhana.

   Contoh XML

   ```xml
   <skill>
      <name>Python</name>
      <level>Advanced</level>
   </skill>
   ```

   Perbedaannya bukan berarti XML tidak digunakan lagi. XML tetap relevan pada sistem tertentu yang membutuhkan karakteristik seperti namespace dan schema, tetapi untuk kebutuhan frontend-backend sederhana pada project ini, JSON lebih praktis

3. **Mengapa perlu serialization pada model Django?**

   Ketika view mengambil

   ```python
   Skill.objects.all()
   ```

   hasilnya adalah `QuerySet` yang berisi object model Django

   Object tersebut tidak dapat langsung dikirim sebagai JSON karena JSON tidak memahami object Python/Django beserta method dan state internalnya

   Karena itu, diperlukan proses **serialization** untuk mengubah data model menjadi struktur yang dapat direpresentasikan dalam JSON

   ```mermaid
   flowchart LR
      A[(Database)]
      B[Django ORM]
      C[QuerySet]
      D[Serializer]
      E[JSON Response]
      F[JavaScript]
      G[DOM]

      A --> B --> C --> D --> E --> F --> G
   ```

   Contoh sederhana pada backend

   ```python
   from django.core.serializers import serialize

   data = serialize("json", Skill.objects.all())
   ```

   Kemudian data tersebut dikembalikan sebagai response

   ```python
   HttpResponse(
      data,
      content_type="application/json"
   )
   ```

   Di sisi client, JavaScript menerima response tersebut dan melakukan deserialisasi melalui

   ```javascript
   response.json()
   ```

   Sehingga alur lengkapnya adalah

   ```text
   Database
      ↓
   Django ORM
      ↓
   Model / QuerySet
      ↓
   Serialization
      ↓
   JSON
      ↓
   Deserialization
      ↓
   JavaScript Object
      ↓
   DOM
   ```

### Tugas 4

> Pada Tugas 4, pertanyaan reflektif ditiadakan sesuai ketentuan tugas. Bagian ini saya isi dengan catatan implementasi agar riwayat pengembangan mingguan tetap terdokumentasi dan saya dapat mengingat apa yang saya pelajari/terapkan

1. **Perbedaan autentikasi dan otorisasi dalam implementasi ini**
   
   Autentikasi menjawab pertanyaan *siapa pengguna ini*, sedangkan otorisasi menjawab *apa yang boleh dilakukan pengguna tersebut*. Keduanya diterapkan sebagai dua lapis pemeriksaan yang terpisah di dalam view.

   Lapis pertama adalah `@login_required(login_url="/login/")`. Dekorator ini memeriksa apakah request berasal dari pengguna yang sudah login. Jika belum, Django langsung mengalihkan pengguna ke halaman login tanpa pernah menjalankan isi fungsi view.

   Lapis kedua adalah pemeriksaan peran di baris pertama fungsi. Untuk aksi create dan delete, pemeriksaannya adalah `request.user.is_superuser`. Untuk aksi update, pemeriksaannya diperluas sehingga superuser maupun anggota grup `Editor` sama-sama diizinkan. Ketika pemeriksaan gagal, view memanggil `raise PermissionDenied` sehingga Django membalas dengan status **403 Forbidden**.

   Kedua bentuk kegagalan tersebut sengaja dibedakan. Pengunjung yang belum login masih mempunyai langkah lanjutan yang jelas, yaitu login, sehingga diarahkan ke halaman login. Pengguna yang sudah login tetapi tidak berhak tidak mempunyai langkah lanjutan apa pun, sehingga permintaannya ditolak di tempat.

2. **Mengapa peran Editor menggunakan Django Group, bukan field boolean pada model**

   Django hanya menyediakan tiga atribut peran bawaan pada model `User`, yaitu `is_active`, `is_staff`, dan `is_superuser`. Tidak ada atribut `is_editor`, sehingga peran baru perlu dibentuk dengan mekanisme lain.

   Saya memilih **Django Group** karena peran bersifat data, bukan struktur. Menambahkan field boleh baru pada model akan memaksa perubahan skema database setiap kali ada peran tambahan, sedangkan grup cukup ditambahkan sebagai baris data. Keanggotaan pengguna juga dapat diubah melalui Django Admin tanpa menyentuh kode.

   Pemeriksaannya dilakukan melalui satu fungsi bantu agar tidak diulang-ulang di banyak view:

   ```python
   def is_editor(user):
       return user.groups.filter(name="Editor").exists()
   ```

   Agar peran ini tidak bergantung pada database lokal saya, grup `Editor` dibuat melalui **data migration**. Dengan demikian, siapa pun yang menjalankan `python manage.py migrate` akan langsung memiliki grup tersebut, karena `db.sqlite3` sendiri tidak ikut di-commit ke repositori.

3. **Mengapa proteksi kode rahasia dari Tugas 3 diganti**

   Pada Tugas 3, aksi create, update, dan delete dilindungi oleh sebuah kode rahasia yang disimpan pada environment variable. Mekanisme itu berfungsi sebagai lapisan proteksi sementara ketika materi autentikasi belum dipelajari, tetapi tidak mengenali identitas pengguna sama sekali.

   Setelah peran diperkenalkan, kedua mekanisme tersebut tidak dapat berjalan berdampingan. Seorang Editor berhak mengubah data menurut aturan tugas, tetapi akan tetap tertahan oleh kode rahasia yang tidak ia miliki. Dua sistem proteksi yang saling menimpa juga membuat logika view sulit dibaca dan sulit diuji.

   Karena itu seluruh pemeriksaan kode rahasia saya hapus dari view dan digantikan sepenuhnya oleh otorisasi Django. Endpoint pendukung `verify_secret_key` beserta konfigurasinya ikut dibersihkan agar tidak meninggalkan kode mati di dalam project.

4. **Cara relasi star disimpan dan diamankan pada endpoint JSON**

   Hubungan star dicatat dengan `ManyToManyField` ke model `User`, karena satu skill dapat di-star banyak pengguna dan satu pengguna dapat mem-star banyak skill. Django membuat tabel penghubungnya sendiri, sehingga tidak diperlukan model baru:

   ```python
   starred_by = models.ManyToManyField(
       User, related_name="starred_skills", blank=True
   )
   ```

   Penambahan field tersebut ternyata ikut mengubah isi endpoint JSON yang dapat dibuka siapa pun. Secara bawaan, serializer menampilkan id internal database pengguna. Karena itu serializer dipanggil dengan `use_natural_foreign_keys=True` agar relasi ditampilkan sebagai username yang memang bersifat publik, bukan id internal.

   Saat menguji hal ini saya juga menemukan bahwa akun uji yang saya daftarkan memakai alamat email sebagai username, sehingga email tersebut ikut tampil pada endpoint publik. Akun tersebut saya ganti dengan username biasa agar tidak ada data kontak yang terekspos.

5. **Pengujian yang dilakukan**

   Pemeriksaan tidak cukup dilakukan dengan melihat tombol saja, karena `{% if %}` pada template hanya mengatur apa yang terlihat dan bukan apa yang boleh dijalankan. Karena itu setiap peran diuji dengan mengetik URL aksi secara langsung pada address bar:

   | Skenario | Hasil yang diharapkan |
   | --- | --- |
   | Belum login membuka `/skills/add/` | Diarahkan ke `/login/` |
   | Pengguna biasa membuka `/skills/<id>/edit/` | 403 Forbidden |
   | Pengguna biasa menekan tombol star | Berhasil, jumlah star berubah |
   | Editor membuka `/skills/<id>/edit/` lalu menyimpan | Form terbuka dan perubahan tersimpan |
   | Editor membuka `/skills/add/` | 403 Forbidden |
   | Superuser membuka seluruh aksi | Semua diizinkan |

   Skenario yang sama diulang untuk halaman Projects. Cookie `last_login` dan `sessionid` juga diperiksa melalui tab **Application** pada Developer Tools untuk memastikan keduanya terbit saat login dan terhapus saat logout.

### Tugas 5

1. **Apa itu debouncing dan mengapa teknik ini penting pada fitur pencarian yang menggunakan AJAX?**

   Debouncing adalah teknik untuk menunda sebuah fungsi sampai tidak ada kejadian baru selama jeda tertentu. Gampangnya seperti menunggu seseorang selesai berbicara sebelum kita menjawab: selama ia masih menambah kalimat, kita belum merespons.

   Pada fitur pencarian, kejadian yang dimaksud adalah event `input`, yang terpicu setiap kali satu karakter diketik. Tanpa debouncing, mengetik "python" mengirim enam request berturut-turut ke server, padahal hasil untuk "p", "py", dan "pyt" tidak pernah dibutuhkan pengguna. Request yang berlebihan membebani server, membuat daftar berkedip-kedip, dan berisiko menimbulkan masalah urutan: respons dari request lama bisa tiba setelah respons yang lebih baru, lalu menimpanya.

   Di project ini, setiap karakter baru memanggil `clearTimeout` untuk membatalkan timer sebelumnya, lalu `setTimeout` memulai hitungan 300 ms dari awal (`SEARCH_DEBOUNCE_DELAY`). Request baru benar-benar dikirim hanya jika pengguna berhenti mengetik selama 300 ms, sehingga yang dicari adalah teks akhirnya saja. Tombol Cari dan tombol Enter tetap membatalkan timer lalu mencari langsung, agar pengguna yang sudah selesai mengetik tidak perlu menunggu. Selain itu, `AbortController` membatalkan request sebelumnya yang belum selesai agar hasil lama tidak menimpa hasil terbaru.

   Debouncing berbeda dari throttling. Throttling membatasi sebuah fungsi agar berjalan paling sering sekali per interval, sehingga cocok untuk event yang terus mengalir seperti scroll. Untuk pencarian, yang dibutuhkan adalah hasil dari nilai terakhir, sehingga debouncing lebih tepat.

2. **Apa fungsi `await` pada `fetch()` dan apa yang terjadi jika tidak digunakan?**

   `fetch()` bekerja secara asinkron. Begitu dipanggil, ia tidak menunggu server menjawab, melainkan langsung mengembalikan sebuah *Promise*, yaitu "janji" bahwa hasilnya akan datang nanti. Keyword `await`, yang hanya boleh dipakai di dalam `async function`, menghentikan jalannya fungsi itu sampai Promise selesai, lalu mengambil isinya, yaitu objek `Response`. Bagian lain dari halaman tetap berjalan, jadi tampilan tidak membeku. Karena itu kita bisa menulis `const response = await fetch(url)` dan memakai `response.ok` pada baris berikutnya seolah-olah kode berjalan berurutan.

   Tanpa `await`, variabel `response` hanya berisi Promise yang belum selesai, bukan hasil dari server. Akibatnya `response.ok` bernilai `undefined`, dan `response.json()` gagal karena Promise tidak memiliki method tersebut. Baris-baris berikutnya, seperti merender kartu atau menampilkan toast, juga langsung berjalan sebelum datanya tiba. Kegagalan jaringan pun tidak tertangkap oleh `try/catch` karena penolakan Promise terjadi di luar alur yang ditunggu. Hal yang sama berlaku untuk `response.json()`, yang juga mengembalikan Promise sehingga perlu di-`await`.

   Satu hal lain yang saya pelajari: `fetch()` tidak menolak Promise untuk status 4xx atau 5xx. Karena itu `response.ok` harus selalu diperiksa, seperti pada `addProject` dan `addSkill`, supaya respons 400 atau 403 dari server diperlakukan sebagai kegagalan dan pesan errornya ditampilkan lewat toast.

3. **Apa itu serangan XSS dan mengapa data yang ditampilkan lewat AJAX/JavaScript lebih rentan daripada lewat template Django?**

   Cross-Site Scripting (XSS) adalah serangan ketika penyerang berhasil menyisipkan JavaScript miliknya ke dalam halaman web sehingga kode itu dijalankan di browser pengguna lain. Salah satu jenisnya, *stored XSS*, terjadi ketika kode berbahaya disimpan ke database (misalnya sebagai nama skill) lalu ikut dijalankan setiap kali data itu ditampilkan. Kode tersebut bisa melakukan banyak hal, termasuk membaca cookie `csrftoken` dan mengirim request atas nama korban, sehingga perlindungan CSRF pun ikut tidak berguna.

   Data yang ditampilkan lewat template Django relatif aman karena Django melakukan *auto-escaping* pada setiap `{{ variabel }}`: karakter seperti `<` dan `>` diubah menjadi `&lt;` dan `&gt;`, sehingga browser menampilkannya sebagai teks biasa. Pada AJAX, bagian itu tidak lagi dikerjakan Django. Server hanya mengirim JSON, lalu JavaScript yang merakit tampilannya. Jika nilai dari JSON disisipkan lewat `innerHTML` atau template literal, browser akan menafsirkan tag di dalamnya sebagai HTML sungguhan, misalnya `<img src="x" onerror="...">`. Perlindungan otomatis tadi hilang, dan tanggung jawab melakukan escaping berpindah ke developer.

   Di project ini ada tiga lapis pertahanan. Pertama, kartu project dan baris tabel skill dirakit dengan `createElement` dan `textContent`, yang tidak pernah menafsirkan isinya sebagai HTML. Kedua, di server, method `clean_<field>` pada `ModelForm` memakai `strip_tags` untuk membuang tag dari input. Ketiga, `URLField` menolak URL dengan skema berbahaya seperti `javascript:`. `strip_tags` hanyalah lapisan tambahan: ia tidak cukup dijadikan satu-satunya pertahanan, dan hanya berlaku untuk data baru, sehingga data lama yang telanjur tersimpan tetap harus ditampilkan secara aman.

### Catatan Implementasi Tutorial 5 dan Tugas 5

**1. Halaman hanya merender kerangka, data menyusul lewat AJAX**

Sebelumnya, view mengirim seluruh daftar data ke template dan Django langsung merender semuanya. Sekarang `show_projects` dan `show_skills_manage` hanya mengirim kerangka halaman. Setelah halaman terbuka, JavaScript memanggil `fetch()` ke `/api/projects/` atau `/api/skills/`, lalu merakit hasilnya menjadi kartu atau baris tabel. Selama menunggu, halaman menampilkan keadaan *loading*. Jika datanya kosong, tampil pesan *empty*, dan jika permintaan gagal, tampil pesan *error*. Pengunjung yang belum login tetap dapat membaca data karena endpoint JSON bersifat publik.

**2. JSON dirakit manual, bukan dengan `serializers.serialize`**

Serializer bawaan tidak mengetahui siapa pengguna yang sedang membuka halaman, sehingga tidak bisa menjawab pertanyaan "apakah saya sudah memberi star pada item ini?". Karena itu `get_projects_json` dan `get_skills_json` menyusun dictionary sendiri lalu mengirimkannya dengan `JsonResponse`, lengkap dengan `star_count`, `is_starred` (dihitung dari `request.user`), dan `starred_by_names`. Bentuk `{"pk": ..., "fields": {...}}` saya pertahankan agar JavaScript yang sudah ada tetap cocok.

**3. Tambah data lewat modal dan `fetch`**

Form tambah data berada di dalam modal (Popover API) pada halaman daftar. Saat disubmit, JavaScript membatalkan pengiriman biasa dengan `preventDefault()`, lalu mengirim `FormData` ke `/projects/add-ajax/` atau `/skills/add-ajax/` bersama header `X-CSRFToken` yang dibaca dari cookie `csrftoken`. Server memvalidasi dengan `ModelForm` dan membalas JSON dengan status yang sesuai: **201** jika berhasil, **400** beserta daftar error per field jika tidak valid, dan **403** jika pengirimnya bukan superuser. Balasan itu dibaca JavaScript untuk menentukan langkah berikutnya: menutup modal, menampilkan toast, dan memuat ulang daftar tanpa me-reload halaman.

**4. Mengapa endpoint AJAX tidak memakai `@login_required`**

Dekorator tersebut membalas pengunjung anonim dengan redirect ke halaman login. `fetch()` mengikuti redirect itu dan menerima halaman HTML login berstatus 200, sehingga `response.ok` bernilai `true` dan JavaScript mengira data sudah tersimpan. Karena `AnonymousUser` juga memiliki `is_superuser` bernilai `False`, satu pemeriksaan `is_superuser` sudah cukup untuk menolak pengunjung anonim maupun pengguna biasa dengan JSON 403 yang mudah dibaca JavaScript. Pemeriksaan hak akses tetap dilakukan di dalam view, bukan hanya dengan menyembunyikan tombol.

**5. Jalur lama tetap dipertahankan**

View `create_project` dan `create_skill` yang lama tidak dihapus. Atribut `action` pada form di modal masih mengarah ke view lama, sehingga form tetap dapat dikirim dengan cara biasa jika JavaScript tidak berjalan.

**6. Perlindungan XSS**

Karena kartu dan baris tabel dirakit dengan `createElement` dan `textContent`, fungsi `escapeHtml` seperti pada contoh tutorial tidak diperlukan. Payload seperti `<img src="x" onerror="alert('XSS!')">` akan tampil sebagai teks biasa walaupun lolos ke database. Di sisi server, `clean_title`, `clean_category`, dan `clean_description` pada `ProjectForm`, serta `clean_name` dan `clean_category` pada `SkillForm`, membuang tag HTML dengan `strip_tags` dan menolak nama yang menjadi kosong setelahnya. Pembersihan ini menjadi lapisan kedua, bukan pengganti `textContent`.

**7. Berkas JavaScript bersama**

`showToast` dimuat dari `static/js/toast.js` melalui `base.html`. Fungsi `getCookie` awalnya hanya ada di dalam skrip halaman Projects, sehingga saya memindahkannya ke `static/js/utils.js` agar halaman Skills dapat memakainya tanpa menyalin kode.

**8. Skenario pengujian**

| Skenario | Hasil yang diharapkan |
| --- | --- |
| Pengunjung belum login membuka `/skills/manage/` | Tabel termuat lewat AJAX tanpa tombol aksi |
| Mengetik pelan di kotak Cari | Satu request setelah berhenti mengetik, daftar terfilter |
| Mencari kata yang tidak ada | Muncul pesan bahwa tidak ada skill dengan nama tersebut |
| Superuser menambah skill lewat modal | `POST` berstatus 201 dengan header `X-CSRFToken`, modal tertutup, toast hijau, daftar bertambah tanpa reload |
| Nama skill kosong atau hanya berisi tag HTML | 400, modal tetap terbuka, toast merah berisi pesan dari server |
| Nama `Py<b>thon</b>` | Tersimpan sebagai `Python` |
| Pengguna non-superuser memanggil `/skills/add-ajax/` langsung | 403 berupa JSON untuk `POST`, 405 untuk `GET` |

### Catatan Implementasi Tutorial 6

**1. HTMX dibandingkan dengan AJAX dan `fetch` (Tutorial 5)**

Pada Tutorial 5, server mengirim JSON lalu JavaScript yang merakit tampilannya dengan `createElement`. Pada HTMX, arahnya dibalik: server mengirim potongan HTML (*fragment*), dan HTMX langsung memasangnya ke bagian halaman yang dituju. Alurnya selalu sama: **event dari pengguna, request lewat atribut `hx-*`, view Django mengembalikan fragment HTML, lalu HTMX melakukan *swap* ke target**. Keuntungannya, hampir tidak ada JavaScript yang perlu saya tulis dan tampilan tetap dirender oleh template Django. Kekurangannya, server dan template terikat pada bentuk HTML tertentu, dan datanya tidak berbentuk JSON sehingga tidak bisa dipakai klien lain seperti API.

**2. Aplikasi `contacts` terpisah dari `main`**

Tutorial memakai app bernama `main`, padahal proyek ini sudah memilikinya. Mengikuti tip di tutorial, saya membuat app baru `contacts` dengan namespace URL `contacts:`, prefix `/contacts/`, dan template di `templates/contacts/` agar tidak bentrok dengan `index.html` milik `main`. Halaman Projects dari Tutorial 5 tidak saya ubah. Aplikasi ini punya model `Contact` (`name`, `email`, lalu `phone` dari latihan) dan dua migrasi, `0001_initial` dan `0002_contact_phone`, sehingga `python manage.py migrate` perlu dijalankan di database lokal.

**3. Partial template dan atribut `hx-*`**

Potongan HTML yang dikirim ke HTMX saya simpan sebagai *partial template*: `_contact_row.html` (satu baris), `_contact_rows.html` (semua baris, dengan pesan kosong), `_contact_edit_row.html` (baris berbentuk form), dan `_contact_added.html` (baris baru beserta pembaruan tambahan, lihat poin 5). Halaman utamanya, `index.html`, memuat HTMX dari CDN dan menyertakan token CSRF di `hx-headers` pada `<body>`, sehingga setiap `POST`, `PUT`, dan `DELETE` dari elemen di dalamnya membawa `X-CSRFToken`.

| Fitur | Atribut utama | Response view | Swap |
| --- | --- | --- | --- |
| Tambah | `hx-post`, `hx-target="#contact-rows"` | baris kontak baru | `beforeend` |
| Cari | `hx-get`, `hx-trigger="keyup changed delay:300ms, search"` | baris hasil filter | `innerHTML` |
| Edit | `hx-get` pada tombol Edit | baris berbentuk form | `outerHTML` pada `closest tr` |
| Simpan | `hx-put` pada form | baris tampilan | `outerHTML` |
| Batal | `hx-get` ke `contact_row` | baris tampilan | `outerHTML` |
| Hapus | `hx-delete`, `hx-confirm` | string kosong | `outerHTML` pada `closest tr` |

**4. Hal-hal yang perlu diperhatikan**

- **Hapus harus membalas 200 dengan isi kosong, bukan 204.** HTMX tidak melakukan *swap* untuk response 204, sehingga barisnya tidak akan hilang dari tabel.
- **Request `PUT` tidak mengisi `request.POST`.** Datanya ada di `request.body` sebagai string mentah, jadi `contact_update` membacanya dengan `QueryDict(request.body)`.
- **`<form>` tidak boleh membungkus `<td>`.** Pada baris edit, setiap input berada di selnya sendiri dan menunjuk form di sel terakhir lewat atribut `form="edit-form-<id>"`.
- **Debounce cukup ditulis di atribut.** `delay:300ms` pada `hx-trigger` menggantikan `setTimeout` dan `clearTimeout` yang saya tulis manual pada Tutorial 5.
- **Pencarian memakai `name="q"`**, sehingga HTMX otomatis mengirim `GET /contacts/search/?q=...`, dan filter `name__icontains` tidak membedakan huruf besar dan kecil.

**5. Latihan**

- **Field `phone`:** ditambahkan ke model (`CharField`, `blank=True`) dan ke form tambah, tampilan baris, form edit, serta view tambah dan update. Kolom `colspan` pada pesan kosong ikut disesuaikan menjadi 4.
- **`hx-swap="beforeend"`:** view tambah hanya mengembalikan baris baru, bukan seluruh daftar, lalu baris itu disisipkan di akhir tabel. Akibatnya baris "Tidak ada kontak." tidak ikut terganti, jadi response juga menyertakan `<tr id="contacts-empty" hx-swap-oob="delete">` untuk menghapus baris tersebut saat kontak pertama ditambahkan.
- **Feedback lewat `hx-swap-oob`:** satu elemen hanya bisa punya satu `hx-target`, jadi response yang sama juga menyertakan `<div id="feedback" hx-swap-oob="true">Kontak berhasil ditambahkan!</div>` untuk memperbarui `#feedback` di halaman.

**6. Pengujian dan keterbatasan**

Ada 15 test di `contacts/tests.py` yang memeriksa sisi server: halaman daftar dan pesan kosong, tambah (termasuk bahwa yang dikembalikan hanya baris baru), hapus (200 dengan isi kosong, 405 untuk method lain, 404 untuk id yang tidak ada), pencarian (tanpa membedakan huruf besar dan kecil, query kosong, tidak ada hasil), serta edit dan update lewat `PUT`. Perilaku HTMX di browser (swap, konfirmasi hapus, indikator pencarian) tidak tercakup oleh test tersebut dan perlu dicoba langsung.

Keterbatasan yang saya sadari: mengikuti tutorial, `contact_add` dan `contact_update` menyimpan input tanpa validasi di server (email hanya dibatasi oleh `type="email"` dan `required` di browser), dan tidak ada pembatasan siapa yang boleh menambah, mengubah, atau menghapus kontak. Template Django tetap melakukan *auto-escaping*, sehingga input berisi tag HTML tampil sebagai teks. Karena Tutorial 6 hanya latihan, kedua hal itu tidak saya tambahkan.

**7. Skenario pengujian**

| Skenario | Hasil yang diharapkan |
| --- | --- |
| Membuka `/contacts/` saat belum ada kontak | Tabel berisi baris "Tidak ada kontak." |
| Menambah kontak lewat form | `POST` berstatus 200, baris baru muncul di akhir tabel tanpa reload, baris "Tidak ada kontak." hilang, pesan feedback tampil, dan form dikosongkan |
| Mengetik di kolom Cari | Satu request setelah berhenti mengetik 300 ms, tabel terfilter |
| Menekan Edit, lalu Batal | Baris berubah menjadi form, lalu kembali menjadi baris tampilan tanpa menyimpan apa pun |
| Menekan Edit, mengubah data, lalu Simpan | `PUT` berstatus 200, baris tampilan menampilkan nilai baru |
| Menekan Hapus lalu OK pada konfirmasi | `DELETE` berstatus 200 dengan isi kosong, baris hilang |
| Memanggil `/contacts/<id>/delete/` dengan `POST` | 405 dan data tidak terhapus |

### Catatan Implementasi Tutorial 7

**1. Dari JSON manual ke Django REST Framework**

Pada Tutorial 5, `get_projects_json` menyusun dictionary satu per satu dan mengirimkannya dengan `JsonResponse`, sedangkan `create_project_ajax` memeriksa izin, memvalidasi form, dan memilih status HTTP di dalam satu fungsi. Pola itu berjalan, tetapi akan berulang setiap kali bagian lain (misalnya Skill) membutuhkan API. Pada Tutorial 7 tanggung jawab itu saya pisahkan: *serializer* mengurus representasi dan validasi data, *permission class* mengurus hak akses, `@api_view` menolak method yang salah, dan `Response` mengirim hasilnya.

| Tindakan | Sebelum Tutorial 7 | Tutorial 7 |
| --- | --- | --- |
| Melihat daftar project | `GET /api/projects/` | `GET /api/v1/projects/` |
| Menambah project | `POST /projects/add-ajax/` | `POST /api/v1/projects/` |
| Menghapus project | `POST /projects/<uuid>/delete/` | `DELETE /api/v1/projects/<uuid>/` |

Jalur lama tidak saya hapus. `get_projects_json`, `create_project_ajax`, `create_project`, `update_project`, `delete_project`, dan `toggle_star` masih ada, begitu pula halaman edit untuk Editor. Yang berpindah ke API baru hanya halaman Projects.

**2. Serializer dan validasi**

`ProjectSerializer` (di `main/serializers.py`) adalah `ModelSerializer` dengan daftar `fields` yang ditulis eksplisit, sehingga password atau email pengguna tidak mungkin ikut terkirim. Field `id` bersifat *read-only*. Tiga field hasil perhitungan, yaitu `star_count`, `is_starred`, dan `starred_by_names`, memakai `SerializerMethodField`, sehingga otomatis hanya dapat dibaca. `is_starred` dihitung dari `request` yang dibawa lewat `context`, dan bernilai `False` jika tidak ada request atau pengunjung belum login. Itu alasan view selalu mengirim `context={"request": request}`.

Validasi memakai method `validate_<field>`: `validate_title` membuang tag dengan `strip_tags`, lalu menolak judul yang menjadi kosong, sedangkan `validate_description` dan `validate_category` cukup membuang tag. `URLField` dari model tetap menolak `javascript:alert(1)`. Aturan ini harus ada di serializer karena `ProjectSerializer` tidak menjalankan `ProjectForm.clean_title`: input lewat API memakai jalur validasi yang berbeda dari form.

Tiga bentuk data yang sering tertukar:

- `request.data` adalah input mentah dari klien dan belum boleh dipercaya.
- `.validated_data` adalah input yang lolos `is_valid()` dan sudah dibersihkan, dan field read-only diabaikan.
- `.data` adalah representasi untuk klien (termasuk `id` dan field hasil perhitungan), dibaca setelah `.save()`.

**3. Autentikasi, otorisasi, dan CSRF**

Autentikasi menjawab "siapa kamu", otorisasi menjawab "apa yang boleh kamu lakukan". Di DRF keduanya terpisah: `SessionAuthentication` mengisi `request.user` dari session login yang sudah ada, lalu permission class memutuskan apakah request diteruskan. `IsPortfolioOwnerOrReadOnly` mengizinkan method aman (`GET`, `HEAD`, `OPTIONS`) untuk semua orang dan method lain hanya untuk `is_superuser`. Saya tidak memakai `IsAuthenticatedOrReadOnly` karena semua akun login akan boleh menulis, dan tidak memakai `IsAdminUser` karena permission itu memeriksa `is_staff`, bukan `is_superuser` seperti aturan portofolio ini. Endpoint star memakai `IsAuthenticated`, dan akun pemberi star selalu diambil dari `request.user`, bukan dari input klien.

Urutan satu request: routing, autentikasi, permission, pemeriksaan method, isi view, serializer, lalu response. Karena permission diperiksa sebelum objek dicari, pengguna biasa yang mengubah project yang tidak ada mendapat **403**, bukan 404. Pada `SessionAuthentication`, pengunjung anonim yang menulis data juga mendapat 403, bukan 401. Untuk `POST`, `PUT`, `PATCH`, dan `DELETE` dari akun yang login lewat session, token CSRF tetap wajib dikirim lewat header `X-CSRFToken`, dan saya tidak memakai `@csrf_exempt`.

Kelas `IsPortfolioOwnerOrEditorOrReadOnly` (superuser boleh semua, anggota grup Editor hanya `PUT` dan `PATCH`) sudah ada di `main/permissions.py` tetapi sengaja tidak dipasang pada endpoint Projects, sesuai tutorial. Kelas itu disiapkan untuk bagian portofolio yang diminta pada tugas berikutnya.

**4. Kontrak API**

| Method | Endpoint | Tindakan | Siapa yang boleh |
| --- | --- | --- | --- |
| GET | `/api/v1/projects/` | Daftar, `?title=` untuk mencari | Semua pengunjung |
| POST | `/api/v1/projects/` | Tambah project | Pemilik (superuser) |
| GET | `/api/v1/projects/<uuid>/` | Detail satu project | Semua pengunjung |
| PUT / PATCH | `/api/v1/projects/<uuid>/` | Ubah project | Pemilik |
| DELETE | `/api/v1/projects/<uuid>/` | Hapus project | Pemilik |
| POST | `/api/v1/projects/<uuid>/star/` | Beri atau batalkan star | Pengguna login |

Status yang dikembalikan: **200** untuk baca dan ubah, **201** setelah membuat, **204** (tanpa isi) setelah menghapus, **400** beserta error per field untuk input tidak valid, **403** untuk tindakan yang tidak diizinkan, **404** jika UUID tidak ditemukan, dan **405** untuk method yang salah. `PUT` menuntut semua field wajib, sedangkan `PATCH` memakai `partial=True` sehingga field yang tidak dikirim tetap seperti semula. Pencarian kosong mengembalikan `[]` dengan status 200, bukan 404, karena daftar kosong adalah hasil yang sah.

**5. Halaman Projects memakai API baru**

JSON sekarang datar (`item.id`, `item.title`, `item.category`, `item.link`), bukan `item.pk` dan `item.fields`, dan `starred_by_names` berupa string, bukan list. Semua permintaan tulis melewati satu helper, `writeProject(url, method, payload)`, yang mengirim JSON, header `X-CSRFToken` dari `getCookie('csrftoken')`, dan membaca error serializer lewat `apiErrorMessage`. Status 204 menghasilkan `null` sehingga `.json()` tidak dipanggil pada body kosong. Tombol star dan hapus memakai *event delegation* pada `#grid`, sehingga tetap bekerja setelah daftar dirender ulang. Tag `{% csrf_token %}` saya taruh di luar `<script>` agar cookie `csrftoken` selalu dibuat, termasuk untuk pengguna biasa yang hanya memberi star.

Tampilan Tutorial 5 saya pertahankan: kartu tetap dirakit dengan `createElement` dan `textContent` (bukan `innerHTML`), sehingga fungsi `escapeHtml` tidak diperlukan. Modal hapus dan debounce 300 ms tetap ada, dan tautan Edit untuk Editor masih menuju halaman edit lama. URL gambar dan tautan hanya ditampilkan jika berskema `http` atau `https`, untuk data lama yang tersimpan sebelum serializer memvalidasinya.

**6. Pengujian**

`main/tests_api.py` berisi 13 test `APITestCase` dari tutorial: daftar dan detail publik, pencarian, 404, penolakan tulis bagi tamu dan pengguna biasa (dengan memeriksa isi database, bukan hanya status), pembuatan oleh pemilik, validasi, `PATCH`/`PUT`/`DELETE`, star, field hasil perhitungan yang tidak bisa dipalsukan, *staff* dan Editor yang tidak boleh mengelola Projects, method yang salah, serta dua test CSRF. Hasilnya `Ran 13 tests ... OK`, dan `python manage.py test main` (43 test) juga lulus.

Dua test CSRF memakai `APIClient(enforce_csrf_checks=True)` dan `.login()` karena `force_authenticate` memilih pengguna langsung tanpa melewati proses login maupun CSRF, sehingga tidak bisa membuktikan perlindungan CSRF berjalan. Saya juga mencoba eksperimen dari tutorial: ketika permission saya longgarkan menjadi selalu `True`, `test_guest_and_visitor_cannot_write` gagal dengan `201 != 403`. Setelah dikembalikan, semua test lulus lagi.

**7. Penyesuaian terhadap proyek saya**

- Field contoh tutorial `tech_stack` dan `project_url` saya ganti menjadi `category` dan `link` sesuai model `Project` milik saya.
- Pada `test_staff_and_editor_cannot_manage_tutorial_projects`, `Group.objects.create(name="Editor")` saya ganti dengan `get_or_create`, karena migrasi `0009_create_editor_group` sudah membuat grup Editor di database test. Isi pemeriksaannya tidak berubah.
- Test lama di `main/tests.py` (`ProjectTest`) saya perbarui sesuai kontrak yang memang berubah sejak Tutorial 4 dan 5 (tambah dan hapus butuh login, bentuk JSON `pk` dan `fields`, halaman Projects hanya kerangka), lalu saya tambah test untuk peran dan izin. Tutorial menyatakan test lama boleh disesuaikan, selama tidak dihapus hanya agar lulus.
- Aplikasi `contacts` dari Tutorial 6 berdiri sendiri dan tidak dipakai oleh Tutorial 7.

**8. Skenario pengujian**

| Skenario | Hasil yang diharapkan |
| --- | --- |
| Pengunjung membuka `/projects/` | Daftar tampil lewat `GET /api/v1/projects/`, tanpa tombol tambah dan hapus, tombol star berupa tautan ke login |
| Pengguna biasa memberi lalu membatalkan star | `POST` berstatus 200, jumlah star bertambah lalu kembali, dan `is_starred` berganti |
| Superuser menambah project lewat modal | `POST` berstatus 201 dengan `X-CSRFToken`, modal tertutup, toast, daftar dimuat ulang tanpa reload |
| Judul hanya berisi spasi atau tag HTML | 400 dengan pesan dari serializer, ditampilkan lewat toast |
| Pengguna biasa memanggil `DELETE /api/v1/projects/<uuid>/` | 403 dan data di database tidak berubah |
| `POST` ke API tanpa header `X-CSRFToken` (session login) | 403 |

### Tugas 6

1. **Apa itu REST, mengapa mengembalikan JSON saja belum cukup untuk menyebut sebuah API RESTful, dan apa beda PUT dengan PATCH?**

   REST (*Representational State Transfer*) adalah gaya merancang API di atas HTTP. Intinya, setiap hal yang dikelola, misalnya sebuah skill, dianggap sebagai *resource* yang punya alamat sendiri (`/api/v1/skills/<uuid>/`). Resource itu dioperasikan lewat method HTTP standar, bukan lewat nama aksi di URL: `GET` untuk membaca, `POST` untuk membuat, `PUT` dan `PATCH` untuk mengubah, `DELETE` untuk menghapus. Server menjawab dengan status HTTP yang bermakna (201, 204, 400, 403, 404, 405), tidak menyimpan keadaan klien di antara request (*stateless*), dan setiap request membawa informasi yang cukup untuk dipahami sendiri.

   Mengembalikan JSON saja belum membuat API menjadi RESTful, karena JSON hanyalah format data. Jalur lama di project ini adalah contohnya: `/skills/add-ajax/` dan `/skills/<uuid>/delete/` mengembalikan JSON atau redirect, tetapi aksinya tertulis di URL (`add`, `delete`), semuanya memakai `POST`, dan tidak ada alamat resource yang konsisten. Pada API baru, alamatnya tetap `/api/v1/skills/<uuid>/` dan yang membedakan aksi adalah method-nya. Status HTTP juga ikut menjadi bagian kontrak: `201` setelah membuat, `204` tanpa isi setelah menghapus, `400` untuk input tidak valid, `403` untuk tindakan yang tidak diizinkan, dan `404` untuk resource yang tidak ada. API yang selalu membalas `200` dengan JSON berisi `{"success": false}` memaksa klien menebak hasilnya.

   `PUT` mengganti seluruh resource, sehingga semua field wajib dikirim. Jika ada field yang hilang, serializer menolaknya dengan 400 (di test saya, `PUT` dengan hanya `name` ditolak). `PATCH` mengubah sebagian: hanya field yang dikirim yang berubah, dan view memakai `partial=True`. Pada halaman Skill, modal edit mengirim `PATCH` karena pengguna biasanya hanya memperbaiki satu atau dua kolom, misalnya mengubah kategori dari `Tools` menjadi `Framework` tanpa menyentuh `name` dan `icon_url`. `PUT` lebih cocok saat klien memang memegang data lengkap dan ingin menggantinya sekaligus, misalnya mengimpor ulang satu skill dari berkas sumber yang lengkap. `PUT` juga idempoten: mengirim isi yang sama dua kali menghasilkan keadaan akhir yang sama.

2. **Apa peran serializer pada Django REST Framework dan apa keuntungannya dibandingkan merakit dictionary secara manual dengan `JsonResponse`?**

   Serializer adalah penerjemah dua arah antara objek model dan data yang dipertukarkan dengan klien. Ke luar, ia mengubah `Skill` menjadi dictionary (lalu JSON). Ke dalam, ia memvalidasi data mentah dari `request.data` dan menyimpannya lewat `.save()`. `SkillSerializer` di `main/serializers.py` memegang tiga tanggung jawab sekaligus: daftar `fields` yang boleh tampil, aturan validasi (`validate_name` dan `validate_category` memakai `strip_tags`, sedangkan `URLField` menolak `javascript:`), dan field hasil perhitungan yang bersifat *read-only* (`star_count`, `is_starred`, `starred_by_names`).

   Pada Tutorial 5, `get_skills_json` menyusun dictionary satu per satu, dan `create_skill_ajax` memvalidasi lewat `SkillForm`, memeriksa izin, lalu memilih status HTTP di dalam satu fungsi. Itu berjalan, tetapi ada beberapa kelemahan. Bentuk data dan aturan validasi tersebar di banyak tempat, dan setiap endpoint baru harus mengulanginya. Mudah ada field yang terlupa atau salah nama. Field yang tidak boleh diubah klien (misalnya jumlah star) tidak terlindungi secara otomatis. Dengan serializer, mengirim `star_count: 99` atau `starred_by` pada `POST` diabaikan, dan ada test yang membuktikannya. Daftar `fields` yang ditulis eksplisit juga menjamin email atau password hash pengguna tidak ikut terkirim, karena `starred_by_names` hanya berisi username.

   Keuntungan lain: serializer yang sama dipakai untuk daftar, detail, `POST`, `PUT`, `PATCH`, dan star, sehingga representasi datanya seragam. Error validasi juga otomatis berbentuk `{field: [pesan]}` dengan status 400, yang langsung bisa dibaca JavaScript dan ditampilkan lewat toast. Pembagian tugasnya jadi jelas: serializer mengurus data, permission class mengurus izin, dan view tinggal menyambungkan keduanya.

3. **Apa perbedaan autentikasi dan otorisasi pada DRF, dan mengapa hak akses harus diperiksa dengan permission class di server, bukan hanya dengan menyembunyikan tombol di template?**

   Autentikasi menjawab "siapa kamu?", sedangkan otorisasi menjawab "apa yang boleh kamu lakukan?". Di DRF keduanya terpisah. `SessionAuthentication` membaca cookie session yang sudah ada dan mengisi `request.user`, lalu permission class memutuskan apakah request itu boleh diteruskan ke view. Pengunjung anonim tetap berhasil "diautentikasi" sebagai `AnonymousUser`, tetapi tidak diotorisasi untuk menulis. Karena `SessionAuthentication` tidak punya skema `WWW-Authenticate`, penolakannya berstatus 403, bukan 401.

   Aturan empat peran pada Skill ditulis di satu tempat, `IsPortfolioOwnerOrEditorOrReadOnly`: method aman terbuka untuk semua, superuser boleh semuanya, dan Editor hanya boleh `PUT` dan `PATCH`. Endpoint star memakai `IsAuthenticated`, dan akun yang memberi star selalu diambil dari `request.user`, bukan dari body request.

   Menyembunyikan tombol hanyalah kenyamanan tampilan. Template berjalan di browser yang dikendalikan pengguna, dan siapa pun bisa membuka DevTools, memakai `curl`, atau mengirim `fetch()` sendiri ke `DELETE /api/v1/skills/<uuid>/` tanpa pernah menyentuh tombol. Kalau server tidak memeriksa, pengguna biasa bisa menghapus data. Karena itu penjagaan sesungguhnya ada di server: test saya memanggil endpoint secara langsung sebagai pengunjung, pengguna biasa, dan Editor, lalu memeriksa bahwa isi database tidak berubah. Tombol yang disembunyikan tetap berguna, tetapi hanya sebagai UX, bukan sebagai keamanan.

4. **Mengapa permintaan yang mengubah data tetap memerlukan token CSRF ketika API memakai `SessionAuthentication`, dan mengapa test dengan `force_authenticate` tidak cukup untuk membuktikan perlindungan CSRF berjalan?**

   `SessionAuthentication` mengenali pengguna dari cookie session, dan browser menyertakan cookie itu secara otomatis ke domain yang sama pada setiap request, termasuk request yang dipicu halaman milik orang lain. Jika seorang superuser sedang login lalu membuka halaman jahat, halaman itu bisa membuat form tersembunyi yang mengirim `POST` atau `DELETE` ke API saya. Browser ikut mengirim cookie `sessionid`, sehingga server mengira superuser sendiri yang meminta. Itulah serangan CSRF. Token CSRF menutup celah ini karena halaman jahat tidak bisa membaca cookie `csrftoken` milik domain saya (*same-origin policy*), jadi tidak bisa menyertakan header `X-CSRFToken` yang benar. Karena itu DRF memaksa pemeriksaan CSRF pada `SessionAuthentication` untuk method yang mengubah data (`POST`, `PUT`, `PATCH`, `DELETE`), dan halaman Skill selalu mengirim `X-CSRFToken` lewat helper `writeSkill`. Saya juga tidak memakai `@csrf_exempt`. Untuk pengguna biasa yang hanya memberi star, `{% csrf_token %}` di template memastikan cookie `csrftoken` selalu terbit.

   `force_authenticate` langsung menetapkan `request.user` dan melewati proses login. Pemeriksaan CSRF milik `SessionAuthentication` tidak pernah dijalankan, sehingga request berhasil walaupun tidak membawa token. Test yang memakainya bisa lulus padahal perlindungan CSRF rusak. Karena itu test CSRF saya memakai `APIClient(enforce_csrf_checks=True)` dan `.login()`: login lewat session sungguhan, lalu `POST`, `PATCH`, `DELETE`, dan star tanpa header `X-CSRFToken` harus berstatus 403 dan database tidak berubah. Test pasangannya mengambil token dari cookie lalu mengirimnya, dan harus berhasil dengan 201, supaya jelas bahwa 403 tadi memang karena token, bukan karena hal lain.

### Catatan Implementasi Tugas 6

**1. Bagian yang dipilih: Skill**

Pola Tutorial 7 saya terapkan pada `Skill`, yaitu bagian yang saya kerjakan sendiri pada Tugas 3 sampai 5. Skill sudah memiliki halaman kelola, pencarian, star, tambah lewat modal, dan edit lewat halaman terpisah. Model tidak berubah, dan tidak ada migrasi baru karena relasi `starred_by` sudah ada sejak Tugas 4.

| Berkas | Isi |
| --- | --- |
| `main/serializers.py` | `SkillSerializer`: `fields` eksplisit, `validate_name` dan `validate_category`, tiga field star read-only |
| `main/api_views.py` | `skill_list` (GET, POST, `?name=`, `?category=`, `?ordering=`), `skill_detail` (GET, PUT, PATCH, DELETE), `skill_star` (POST) |
| `main/api_urls.py` | `api:skill-list`, `api:skill-detail`, `api:skill-star` di bawah `/api/v1/skills/` |
| `templates/skills_manage.html` | Halaman kelola yang memakai API baru |
| `templates/components/skill_edit_modal.html` | Modal edit yang mengirim `PATCH` |
| `main/tests_api_skills.py` | 31 test: 27 `APITestCase` untuk API dan 4 untuk halaman |
| `.github/workflows/ci.yml` | GitHub Actions: `check`, `makemigrations --check`, seluruh test dengan coverage minimal 90%, pada setiap push dan PR |
| `main/decorators.py`, `main/throttles.py` | Decorator `superuser_required` dan `rate_limit`, serta throttle DRF untuk tulis dan star |
| `static/js/skills/` | Modul ES `api.js`, `dom.js`, dan `main.js` untuk halaman Skill |
| `main/tests_security.py`, `main/tests_views.py`, `main/tests_settings.py`, `contacts/tests_authorization.py` | Test keamanan, view lama, pengaturan produksi, dan otorisasi contacts |
| `main/tests_e2e_skills.py`, `requirements-dev.txt` | Sembilan test Selenium per peran dan dependensi pengembangan |

**2. Hak akses empat peran di API**

| Peran | Baca | Star | `PUT` / `PATCH` | `POST` / `DELETE` |
| --- | --- | --- | --- | --- |
| Pengunjung | Boleh | Ditolak (403) | Ditolak | Ditolak |
| Pengguna biasa | Boleh | Boleh | Ditolak | Ditolak |
| Editor | Boleh | Boleh | Boleh | Ditolak |
| Pemilik (superuser) | Boleh | Boleh | Boleh | Boleh |

Permission memakai `IsPortfolioOwnerOrEditorOrReadOnly` dari Tutorial 7, yang sebelumnya sengaja belum dipasang pada Projects. View lama sudah konsisten dengan aturan ini: `update_skill` menerima superuser dan Editor, sedangkan `create_skill` dan `delete_skill` hanya superuser, sehingga tidak ada view lama yang perlu dipersempit. Peran Editor ditentukan oleh keanggotaan Group `Editor`, yang sudah dibuat oleh migrasi `0009_create_editor_group`.

**3. Kontrak API**

| Method | Endpoint | Tindakan | Status |
| --- | --- | --- | --- |
| GET | `/api/v1/skills/` | Daftar, `?name=` mencari, `?category=` memfilter (tepat, tidak peka huruf besar), `?ordering=name` (bawaan) atau `stars` (star terbanyak dulu) | 200, 400 untuk `ordering` tidak dikenal |
| POST | `/api/v1/skills/` | Tambah skill (pemilik) | 201, 400, 403 |
| GET | `/api/v1/skills/<uuid>/` | Detail | 200, 404 |
| PUT / PATCH | `/api/v1/skills/<uuid>/` | Ubah (Editor atau pemilik) | 200, 400, 403, 404 |
| DELETE | `/api/v1/skills/<uuid>/` | Hapus (pemilik) | 204, 403, 404 |
| POST | `/api/v1/skills/<uuid>/star/` | Beri atau batalkan star (login) | 200, 403, 404 |

Pencarian yang tidak menemukan apa pun mengembalikan `[]` dengan status 200, karena daftar kosong adalah hasil yang sah.

**4. Halaman Skill**

`/skills/manage/` sekarang memuat, mencari, memfilter kategori, mengurutkan, menambah, memberi star, mengedit, dan menghapus skill lewat `/api/v1/skills/` tanpa reload. Semua request tulis melewati satu helper, `writeSkill(url, method, payload)`, yang mengirim JSON beserta header `X-CSRFToken`, dan membaca error serializer (400) maupun `detail` (403) menjadi pesan toast. Tombol star, edit, dan hapus memakai *event delegation* pada `<tbody>`. Setelah star, hanya baris yang bersangkutan dirender ulang. Tombol Edit membuka modal yang diisi dari data baris, lalu mengirim `PATCH`. Modal ini hanya dirender untuk Editor dan superuser. Baris tetap dirakit dengan `createElement` dan `textContent`, sehingga nilai teks tidak pernah ditafsirkan sebagai HTML. Dua dropdown (kategori dan urutan) adalah fitur tambahan di luar instruksi: pilihan kategori diisi dari data yang dikembalikan API, dan mengganti dropdown langsung memanggil ulang `GET /api/v1/skills/` dengan parameter yang sesuai. Jalur lama (`get_skills_json`, `create_skill_ajax`, `update_skill`, `delete_skill`, `toggle_skill_star`) saya pertahankan, begitu pula star pada landing page yang masih memakai form biasa.

**5. Pengujian**

`python manage.py test main contacts` menjalankan 185 test dan semuanya lulus. Dari jumlah itu, 43 test berasal dari tutorial, 31 test untuk Skill, dan sisanya dari penguatan pada poin 9 (keamanan, view lama, model, pesan error, dan test browser). Test mencakup setiap peran, pemeriksaan isi database pada penolakan, validasi dan pembersihan tag, star (termasuk bahwa akun pemberi star diambil dari `request.user` dan pengunjung ditolak), serta memastikan email dan password hash tidak muncul di JSON. Test CSRF memakai `APIClient(enforce_csrf_checks=True)` dan `.login()` untuk tiga peran. Seperti pada Tutorial 7, saya mencoba eksperimen sebaliknya: ketika permission Skill sementara saya ganti menjadi `AllowAny`, `test_guest_and_regular_user_cannot_write` dan `test_editor_cannot_create_or_delete` gagal dengan `201 != 403`. Setelah dikembalikan, semuanya lulus lagi.

Selain test otomatis, perilaku JavaScript di browser saya periksa dengan Selenium (Chrome *headless* terhadap `StaticLiveServerTestCase`, berkas `main/tests_e2e_skills.py`) yang memakai session login sungguhan untuk tiap peran. Sembilan skenarionya lulus. Pengunjung hanya melihat tabel dan tautan login. Pengguna biasa menekan star dua kali tanpa reload halaman (penanda `window.__marker` tetap ada). Editor mengubah kategori lewat modal dan nama tetap utuh karena `PATCH`, sedangkan Editor yang mengirim `<b></b>` melihat toast "tidak boleh kosong" dan database tidak berubah. Pemilik bisa menambah lalu menghapus skill, dan pencarian, filter kategori, serta urutan star bekerja. Tiga skenario lain memeriksa star optimistis. Tampilan berubah seketika sebelum server menjawab (fetch sengaja diperlambat), star yang ditolak server dikembalikan ke keadaan semula disertai toast, dan klik kedua saat permintaan masih berjalan diabaikan. Test ini ikut dijalankan di CI dan dilewati otomatis kalau Chrome tidak ada. Pada percobaan pertama, dua kegagalan berasal dari skripnya sendiri (elemen baris yang sudah dirender ulang, dan id field modal edit yang salah ketik), bukan dari aplikasi. Belakangan satu test toast sesekali gagal karena Selenium membaca teks toast saat animasinya baru menampilkan judul. Test lalu diubah agar membaca elemen pesan secara langsung, dan lulus tiga kali berturut-turut.

Database test sudah berisi 12 skill hasil migrasi data, sehingga test saya memakai nama skill unik dan membandingkan jumlah dengan nilai awal, bukan angka mutlak. Test pertama saya sempat gagal delapan kali (`13 != 1`) karena asumsi yang salah ini, dan sumber masalahnya ada di test, bukan di kode produksi.

**6. Keterbatasan yang saya sadari**

- Test browser bergantung pada Chrome. Di mesin tanpa Chrome test itu dilewati, sehingga hanya test sisi server yang berjalan.
- Penghitung rate limit memakai cache memori lokal (`LocMemCache`). Kalau aplikasi dijalankan dengan beberapa proses `gunicorn`, setiap proses menghitung sendiri, jadi batas efektifnya sebanyak jumlah proses kali batas yang ditulis. Untuk satu proses angkanya tepat.
- Daftar kategori pada dropdown dibangun dari skill yang pernah dimuat. Kategori yang baru ditambahkan lewat tab lain baru muncul setelah halaman dimuat ulang.
- Pesan 403 pada endpoint Skill ditulis dalam bahasa Indonesia lewat atribut `message` pada `IsPortfolioOwnerOrEditorOrReadOnly`, supaya toast di halaman mudah dibaca. Endpoint star memakai `IsAuthenticated` bawaan DRF, sehingga penolakannya untuk pengunjung masih berbahasa Inggris, tetapi halaman tidak pernah memicunya karena pengunjung hanya melihat tautan ke login.
- Star pada landing page (`#skills`) masih memakai form POST ke `toggle_skill_star`, sehingga memuat ulang halaman. Yang memakai API hanya halaman `/skills/manage/`.

**7. Skenario pengujian**

| Skenario | Hasil yang diharapkan |
| --- | --- |
| Pengunjung membuka `/skills/manage/` | Tabel dimuat lewat `GET /api/v1/skills/`, tanpa tombol aksi, star berupa tautan ke login |
| Pengguna biasa menekan star dua kali | `POST` berstatus 200 lalu jumlah naik dan kembali, hanya baris itu yang berubah |
| Editor menekan Edit, mengubah kategori, lalu Simpan | `PATCH` berstatus 200, modal tertutup, toast, baris menampilkan nilai baru |
| Editor memanggil `POST` atau `DELETE` ke API | 403 dan database tidak berubah, serta tombol Hapus tidak tampil |
| Superuser menambah skill lewat modal | `POST` berstatus 201 dengan `X-CSRFToken`, modal tertutup, toast, daftar dimuat ulang |
| Nama berisi spasi atau hanya tag HTML | 400, toast berisi pesan serializer |
| `POST` ke API tanpa header `X-CSRFToken` (session login) | 403 |
| Membuka `/api/v1/skills/` di browser | Browsable API tampil |
| Memilih "Star terbanyak" lalu satu kategori | `GET /api/v1/skills/?ordering=stars&category=...`, hanya skill kategori itu, star terbanyak di atas |
| `GET /api/v1/skills/?ordering=created_at` | 400 berisi pilihan yang valid |

**8. CI (GitHub Actions)**

Berkas `.github/workflows/ci.yml` berjalan pada setiap `push` dan *pull request* ke `main` di Ubuntu dengan Python 3.11. Langkahnya: pasang `requirements-dev.txt` (dengan cache pip), `python manage.py check`, `python manage.py makemigrations --check --dry-run` (menggagalkan build jika ada perubahan model tanpa migrasi), lalu `python -m coverage run manage.py test main contacts` yang menjalankan seluruh test termasuk Selenium, dan terakhir `coverage report --fail-under=90` yang menggagalkan build kalau coverage turun di bawah 90%. Hasil terakhir 185 test dan coverage 99%. `SECRET_KEY` diisi nilai palsu khusus CI karena test memakai SQLite dan tidak memanggil layanan luar, sehingga tidak ada secret asli di repository. Run yang tertimpa push baru pada branch yang sama dibatalkan otomatis (`concurrency`), dan izin token dibatasi `contents: read`.


**9. Penguatan keamanan dan kualitas**

Setelah fitur Skill selesai, saya mengaudit keseluruhan proyek terhadap deskripsi skor tertinggi pada rubrik penilaian (CRUD, interaktivitas, security, testing, Git, dokumentasi), bukan terhadap batas minimalnya. Hasilnya beberapa perbaikan, masing-masing dikerjakan di branch sendiri.

- **Pengaturan produksi.** `DEBUG` sebelumnya di-*hardcode* `True`, sehingga halaman error produksi bisa membocorkan kode dan konfigurasi. Sekarang `DEBUG` mati secara bawaan saat `PRODUCTION=True`, dan cookie session serta CSRF hanya dikirim lewat HTTPS. Test memuat modul settings di proses terpisah untuk membuktikannya.
- **Rate limiting.** Decorator `rate_limit` membatasi `/api/chat/` (setiap pesan memanggil Gemini yang berbayar) dan percobaan login serta registrasi, masing-masing 10 per menit. Pemakai yang login dihitung per akun, pengunjung per alamat IP. Di balik proxy hanya entri terakhir `X-Forwarded-For` yang dipercaya, karena entri sebelumnya bisa dipalsukan klien. Pada API, throttle DRF membatasi tulis (30 per menit) dan star (60 per menit) per akun, sementara membaca tetap bebas.
- **Pesan error yang bisa dibaca.** `main/api_errors.py` mengganti teks bawaan DRF untuk login, 404, 405, 429, dan body yang rusak menjadi pesan berbahasa Indonesia (misalnya "Terlalu banyak permintaan. Coba lagi dalam 12 detik."), dan serializer Skill memberi pesan per field. Kode status tidak berubah, hanya `detail` yang diganti, jadi toast di halaman selalu menampilkan kalimat yang jelas.
- **Logout lewat POST.** Sebelumnya logout adalah tautan `GET`, sehingga halaman mana pun bisa mengeluarkan pengunjung dengan sebuah gambar atau tautan. Sekarang logout berupa form dengan token CSRF, dan `GET` dijawab 405. Setelah logout pengunjung dikembalikan ke halaman profil, bukan ke halaman login.
- **Decorator kustom.** `superuser_required` menggantikan pemeriksaan `is_superuser` yang tadinya diulang di beberapa view.
- **Modul contacts.** Tugas tidak menyebut modul ini, tetapi membiarkan siapa pun, termasuk pengunjung tanpa login, menambah, mengubah, dan menghapus kontak adalah kelemahan keamanan, sehingga saya menutupnya. Sekarang hanya pemilik yang boleh menulis (403 untuk yang lain), tombol tulis disembunyikan dari non-pemilik, dan `ContactForm` memvalidasi input serta membuang tag HTML. Sebelumnya `POST` tanpa nama menghasilkan error 500.
- **Query teroptimasi dan teruji.** Daftar skill dan project memakai `prefetch_related`, dan urutan star memakai `annotate`. Test menghitung query dengan `CaptureQueriesContext` dan membuktikan jumlahnya tetap sama untuk 2 maupun 40 baris, sehingga tidak ada masalah N+1.
- **Docstring.** Setiap API view, permission, throttle, validator, dan view contacts kini punya docstring yang menjelaskan perilakunya, termasuk parameter query yang diterima.
- **Test.** Coverage naik dari 79% menjadi 99%. View lama (form, akun, CRUD Project dan Skill) kini teruji, dan `chat_with_ai` diuji dengan model Gemini yang di-*mock* sehingga tidak ada panggilan jaringan.
- **JavaScript halaman Skill.** Kode yang tadinya satu blok `<script>` di template kini dipecah menjadi tiga modul ES (`api.js` untuk permintaan, `dom.js` untuk membangun baris, `main.js` untuk alur halaman). Konfigurasi dikirim lewat atribut `data-*`. Tombol star memakai pembaruan optimistis: baris berubah seketika, lalu diganti jawaban server, atau dikembalikan ke keadaan semula disertai toast kalau permintaan gagal.

Untuk pengaturan produksi, rate limiting, decorator, dan modul contacts, saya mengerjakannya dengan urutan *red-green*: test yang gagal di-commit lebih dulu (misalnya `test(security): specify rate limiting, throttling and the superuser decorator (red)`), baru implementasinya di commit berikutnya. Urutan itu bisa dilihat di `git log`.

---


# Penggunaan AI
## AI Disclosure

Saya menggunakan AI sebagai **pendamping belajar, debugging assistant, dan alat untuk membantu mengeksplorasi alternatif solusi**.

AI tidak digunakan sebagai pengganti proses implementasi dan verifikasi. Setiap saran perlu saya pahami, sesuaikan dengan struktur project, kemudian diuji kembali melalui kode dan browser.

### Tools yang Digunakan

| Tools | Peran dalam proses |
| --- | --- |
| **ChatGPT** | Membantu memahami HTML/CSS, debugging frontend, responsive layout, dan penyusunan dokumentasi/refleksi pada tugas-tugas awal |
| **Claude** | Membantu memahami konsep `ModelForm`, serializer Django, JSON, CSRF, AJAX, dan XSS, merencanakan branch, menyusun prompt kerja, membuat diagram pada README, menyusun draf dokumentasi, serta debugging backend/deployment |
| **Claude Code** | Digunakan pada Tutorial 4 sampai Tugas 6 sebagai asisten implementasi di dalam VS Code untuk menulis perubahan kode langsung pada repository, dengan pembagian pekerjaan per branch |

### Pembagian Peran pada Tutorial 4 sampai Tugas 6

Pada beberapa minggu terakhir saya memisahkan dua jenis penggunaan AI secara sadar:

```text
Claude (chat)                     Claude Code (VS Code)
      │                                    │
Memahami konsep                   Menulis perubahan kode
Menyusun rencana branch           Menjalankan migration
Menyusun prompt kerja             Membuat commit per fitur
      │                                    │
      └──────────────┬─────────────────────┘
                     ↓
        Verifikasi manual oleh saya
        (browser, DevTools, git log)
```

Pemisahan ini saya lakukan supaya perencanaan tidak tercampur dengan eksekusi. Rencana kerja dan pemahaman konsep saya susun lebih dulu, baru instruksinya dijalankan pada repository



## Strategi Prompting

Saya tidak hanya menggunakan satu prompt besar untuk seluruh pengerjaan. Saya menggunakan pendekatan bertahap agar masalah dapat dipahami dan diuji satu per satu.

```text
1. Berikan konteks project
        ↓
2. Jelaskan tujuan / requirement tugas serta minta dijelaskan bagian yang rumit
        ↓
3. Tunjukkan bagian kode atau error yang relevan
        ↓
4. Minta penjelasan penyebab, bukan hanya jawaban
        ↓
5. Minta beberapa kemungkinan solusi bila perlu
        ↓
6. Implementasikan dan uji secara manual
        ↓
7. Kembali ke AI dan minta dijelaskan alasan kenapa belum sesuai bila hasil belum sesuai
        ↓
8. Rapikan solusi final + dokumentasikan pemahamannya
```

### Strategi Prompting Tugas 6: Mengantisipasi Kasus Umum AI

Pada Tugas 6 saya tidak meminta "buatkan API untuk Skill" lalu menerima hasilnya. Petunjuk tugas sudah memuat beberapa titik rawan, dan dari pengalaman Tutorial 4 sampai 7 saya tahu AI cenderung jatuh di titik yang sama. Karena itu setiap prompt saya arahkan sambil meminta bukti, bukan hanya kode. Perencanaan dilakukan lebih dulu dengan Claude (chat), lalu eksekusi per branch dengan Claude Code.

| Kasus yang sering muncul saat memakai AI | Mengapa penting (kaitannya dengan tugas) | Arahan dan bukti di proyek ini |
| --- | --- | --- |
| AI memilih model termudah, misalnya `Project` yang sudah dipakai di tutorial | Tugas meminta bagian yang saya kerjakan sendiri pada Tugas 3 sampai 5, bukan model tutorial | Saya menanyakan "Emg ga bole pilih bagian lain?" untuk memahami batasannya. Setelah membandingkan Project, Skill, dan Experience, saya tetap memakai `Skill` |
| Semua test memakai `force_authenticate`, lalu CSRF dianggap terbukti | `force_authenticate` melewati proses login dan pemeriksaan CSRF | Test CSRF memakai `APIClient(enforce_csrf_checks=True)` dan `.login()` untuk tiga peran, dipasangkan dengan test yang berhasil (201) saat token dikirim, supaya jelas 403 tadi karena token |
| Test hijau, tetapi tidak benar-benar menjaga aturan | Test yang tidak pernah gagal tidak membuktikan apa pun | Permission Skill sementara saya longgarkan menjadi `AllowAny`, sehingga dua test gagal dengan `201 != 403`, lalu dikembalikan |
| Penolakan hanya diperiksa lewat status HTTP | Tugas meminta isi database ikut diperiksa | `assertSkillUntouched()` memastikan jumlah dan nama skill tidak berubah setelah setiap penolakan |
| Test mengasumsikan database kosong | Petunjuk menyebut database test kosong, tetapi migrasi data project ini menyeed 12 skill | Delapan test gagal `13 != 1`, lalu test diperbaiki dengan nama unik dan jumlah relatif terhadap nilai awal |
| Peran Editor dibuat ulang di test dengan cara yang bentrok | Petunjuk meminta grup `Editor` dibuat di `setUp()`, padahal migrasi `0009` sudah membuatnya | Memakai `get_or_create`, sehingga test tetap benar di database yang sudah berisi grup tersebut |
| Siapa pemberi star diambil dari body request | Tugas meminta akun selalu dari `request.user` | Ada test yang mengirim `user` dan `user_id` milik akun lain dan hasilnya tetap akun yang login |
| Serializer membocorkan data akun lewat `starred_by` | Email dan password hash tidak boleh tampil | `starred_by_names` hanya berisi username, dan test memeriksa bahwa email serta `pbkdf2` tidak ada di respons |
| Field hasil perhitungan bisa ditimpa klien | Field star harus read-only | Test mengirim `star_count: 99` dan `starred_by` pada `POST` dan semuanya diabaikan |
| Star lewat `fetch()`, tetapi cookie `csrftoken` tidak pernah terbit untuk pengguna biasa | Petunjuk menyebut halaman harus tetap menyetel cookie CSRF | Template menyertakan `{% csrf_token %}`, dan test memeriksa cookie untuk pengunjung, pengguna biasa, Editor, dan pemilik |
| Tombol disembunyikan, tetapi server tidak memeriksa | Hak akses harus ditegakkan di permission class | Test memanggil API langsung sebagai tiap peran, termasuk akun `is_staff` tanpa peran, yang tetap ditolak |
| AI menambah cakupan di luar permintaan | Pekerjaan yang tidak saya pahami tidak bisa saya pertanggungjawabkan | Star di landing page sengaja tidak diubah, perubahan dibatasi pada halaman Skill, dan trailer `Co-Authored-By` otomatis saya minta dihilangkan |
| AI melaporkan "selesai" padahal masih ada yang bisa dikerjakan | Laporan AI bukan bukti | Saya menegur "loh, perbaiki apa yg perlu kamu perbaiki dong", lalu pesan 403 diindonesiakan dan diberi test |
| AI menambah fitur tanpa bukti bahwa nilai rubrik ikut naik | Rubrik menilai coverage, keamanan, dan riwayat Git secara terukur | Saya meminta audit terhadap rubrik lebih dulu ("tolong diaudit ya keseluruhan"). Hasilnya terukur: coverage naik dari 79% ke 99%, dan commit test yang gagal mendahului implementasi |

Pola prompt yang saya pakai berulang: meminta AI membandingkan hasilnya dengan teks tugas, meminta bukti (test yang gagal ketika aturan dilanggar, perintah Git, isi database) alih-alih ringkasan, dan memutuskan sendiri pilihan yang menyangkut cakupan, misalnya tetap memakai `Skill` dan membiarkan `index.html` apa adanya. Riwayat lengkap percakapan tersimpan di sesi Claude Code saya.

# Evaluasi Kritis terhadap AI

Saya menyadari bahwa jawaban AI tidak otomatis benar hanya karena terlihat masuk akal atau karena kode yang diberikan dapat dijalankan.

Beberapa keterbatasan AI yang saya temukan:

### 1. AI tidak mengetahui konteks project secara sempurna

Saran yang benar pada project Django lain belum tentu cocok dengan struktur folder, nama model, URL, atau cara implementasi pada project saya.

Karena itu, saran AI perlu disesuaikan dengan kode aktual.

### 2. AI dapat memberikan solusi yang terlalu umum

Contohnya, solusi CSS yang secara teori benar belum tentu menghasilkan layout yang sesuai dengan desain ketika dijalankan pada viewport tertentu.

Karena itu, saya tetap menggunakan browser sebagai alat verifikasi

### 3. AI tidak menggantikan testing

Jawaban AI tidak membuktikan bahwa:

- migration berhasil
- endpoint mengembalikan data yang benar
- static files termuat
- layout mobile tidak bertumpuk
- environment variable berhasil dibaca
- pembatasan hak akses benar-benar menolak pengguna yang tidak berhak
- deployment berjalan sesuai harapan.

Semua hal tersebut tetap perlu diuji secara langsung dan debugging mandiri agar terlatih

### 4. AI dapat menghasilkan lebih dari satu solusi

Beberapa masalah memiliki banyak cara penyelesaian. Saya tidak selalu mengambil solusi pertama yang diberikan. Saya mencoba memahami trade-off-nya, menyesuaikan dengan materi kuliah, lalu memilih pendekatan yang paling sesuai dengan struktur project.

### 5. AI dapat mengerjakan lebih dari yang diminta

Pada branch fitur star, AI menambahkan penanganan parameter `next` pada view login yang sama sekali tidak saya minta. Fitur tersebut memang disebut sebagai latihan opsional pada tutorial, tetapi kodenya melibatkan konsep *open redirect* yang belum saya pelajari, dan ruang lingkupnya tidak berkaitan dengan branch yang sedang dikerjakan.

Saya membatalkan perubahan tersebut, karena menyimpan kode yang belum saya pahami di dalam submission bukan keputusan yang bisa saya pertanggungjawabkan jika ditanya.

### 6. AI dapat memilih pendekatan yang belum diajarkan

Masih pada branch yang sama, tombol star sempat diubah agar bekerja tanpa memuat ulang halaman menggunakan `fetch`, sehingga view `toggle_star` ikut diubah supaya mengembalikan JSON. Padahal tutorial secara eksplisit menyatakan bahwa Fetch API baru akan dipelajari pada tutorial berikutnya, dan seluruh form pada modul ini masih berupa form HTML standar.

Saya mengembalikan implementasinya ke form HTML biasa dengan `{% csrf_token %}`, agar sesuai dengan materi dan agar saya tidak kehilangan kesempatan mempelajari konversinya sendiri nanti.

### 7. AI dapat keliru melaporkan status pekerjaan

Ketika saya menanyakan apakah suatu tahap sudah dikerjakan, saya pernah menerima jawaban bahwa pekerjaan tersebut sudah selesai, padahal belum. Saya menemukannya karena memeriksa sendiri melalui `git diff` dan pencarian pada file, bukan karena diberi tahu.

Sejak itu saya membiasakan memverifikasi status pekerjaan melalui perintah Git, bukan melalui ringkasan yang diberikan AI.

### 8. Kesalahan alur kerja tetap menjadi tanggung jawab saya

Satu branch berisi pembatasan hak akses `Project` sempat hampir tidak ikut ter-*merge* ke `main` karena saya keburu melanjutkan ke branch berikutnya. Kesalahan ini bukan berasal dari AI, melainkan dari alur kerja saya sendiri.

Masalahnya baru ketahuan ketika saya membaca ulang `main/views.py` dan menyadari bahwa dekorator `@login_required` tidak ada di sana. Setelah itu saya membiasakan memeriksa `git log --oneline --graph` setiap selesai satu branch, sebelum berpindah ke pekerjaan berikutnya.

### 9. AI dapat menyimpang dari spesifikasi tanpa memberi tahu

Pada endpoint tambah project lewat AJAX, versi awal yang dibuat AI membalas JSON dengan bentuk yang berbeda dari tutorial: pesan 403 diganti, respons 400 tidak dibungkus dalam `errors`, respons 201 tidak menyertakan `pk`, dan JavaScript tidak membaca isi respons sama sekali. Akibatnya toast selalu menampilkan teks generik, sehingga pesan validasi dari server (misalnya dari `clean_title`) tidak pernah sampai ke pengguna.

Perbedaan itu baru terlihat ketika saya meminta AI membandingkan kodenya dengan spesifikasi. AI mendaftar tujuh perbedaan, lalu saya memutuskan untuk menyamakan semuanya dengan tutorial.

### 10. AI dapat memperkenalkan kesalahan lewat penggantian teks massal

Saat membuat modal form skill dari salinan modal project, AI memakai penggantian teks otomatis dan ikut mengubah `class="project-form"` menjadi `skill-form`, padahal CSS hanya mengenal `project-form`. AI menemukan dan memperbaikinya sendiri saat menguji. Kesalahan seperti ini tidak akan terlihat dari tes backend karena yang rusak hanya tampilan, sehingga tampilan modal tetap perlu diperiksa langsung di browser.

### 11. Hasil uji otomatis dari AI perlu dibaca dengan teliti

Tes otomatis yang ditulis AI sempat menunjukkan bahwa modal ikut dirender untuk pengguna non-superuser. Ternyata teks `add-skill-modal` yang dicocokkan juga muncul di dalam kode JavaScript, bukan hanya pada elemen HTML-nya. Setelah pencarian dipersempit ke elemen HTML-nya, hasilnya benar: modal tidak dirender. Pelajarannya, hasil uji perlu dibaca dengan memeriksa apa sebenarnya yang dicocokkan.

### 12. Branch yang terlewat di-merge kembali terulang

Dua branch, yaitu `feature/xss-protection` dan `feature/search-debounce`, belum masuk ke `main` ketika saya mengira Tutorial 5 sudah selesai. Keduanya terlihat setelah saya memeriksa `git log` dan `git branch --merged`. Merge branch debounce memunculkan konflik pada `projects.html`, yang saya selesaikan dengan mempertahankan kedua sisi (debounce dan tambah project lewat AJAX), lalu diuji ulang.

Seperti sebelumnya, ini kesalahan alur kerja saya, bukan kesalahan AI. Sejak itu saya memeriksa `git branch --merged` sebelum mengumpulkan tugas.

### 13. Spesifikasi dan kenyataan database test bisa berbeda

Petunjuk tugas menyebut database pengujian selalu kosong. Pada project ini ternyata tidak: migrasi data menyeed 12 skill. Test pertama yang ditulis AI mengasumsikan hanya ada satu skill, sehingga delapan test gagal dengan `13 != 1`. Kesalahannya ada di asumsi test, bukan di kode produksi. AI mengubahnya agar memakai nama skill yang unik dan membandingkan jumlah dengan nilai awal. Pelajarannya: asumsi dari teks tugas tetap perlu dicek terhadap project sendiri.

### 14. AI berhenti terlalu cepat dan menyerahkan pekerjaan kembali

Setelah test lulus, AI melaporkan pekerjaan selesai dan menyerahkan hal yang sebenarnya bisa ia kerjakan sendiri, yaitu pesan 403 berbahasa Inggris. Saya harus menegur ("perbaiki apa yg perlu kamu perbaiki dong") sebelum itu dikerjakan. Saat itu AI juga sempat menyatakan tidak punya alat browser, padahal pengujian browser tetap bisa dilakukan lewat Selenium. Baru ketika saya meminta memaksimalkan hasil, pengujian browser itu dikerjakan.

### 15. Verifikasi bisa tertinggal di belakang commit

Dalam satu perintah AI menjalankan `manage.py check` dengan Python sistem (bukan virtual environment), perintah itu gagal karena `rest_framework` tidak ditemukan, tetapi `git commit` pada rangkaian perintah yang sama tetap berjalan. AI mengakuinya dan memverifikasi sesudahnya dengan Python dari `env/`. Serializer terbukti benar, tetapi urutannya salah. Virtual environment proyek ternyata juga belum memasang `djangorestframework` walaupun ada di `requirements.txt`.

### 16. Perintah shell panjang gagal dan harus diganti

Dua kali AI menulis berkas besar lewat *heredoc* di Bash dan gagal dengan `unexpected EOF` karena ada tanda kutip tunggal di dalam teks. Karena gagal sebelum menulis apa pun, tidak ada berkas setengah jadi, tetapi AI harus memeriksa `git status` dulu lalu beralih ke alat tulis berkas. Selain itu, bawaan Claude Code menyarankan trailer `Co-Authored-By` pada commit, tetapi saya meminta trailer itu tidak dipakai dan AI memeriksa riwayat dengan `git log --format=%B | grep -ci co-authored` bernilai 0.

### 17. Rantai perintah yang tidak berhenti dan asersi yang terlalu luas

AI menjalankan test lalu `git commit` dalam satu rangkaian perintah yang tidak berhenti ketika test gagal, sehingga satu test yang masih gagal ikut ter-commit. Penyebabnya asersi yang terlalu luas: test mencari teks `fetch(` di halaman Skill, padahal widget chat pada `base.html` juga memakai `fetch`. AI memperbaikinya dengan commit susulan yang mengganti asersi menjadi pemeriksaan logika Skill. Pelajarannya, hasil test harus dibaca sebelum commit dan asersi perlu mencocokkan hal yang benar-benar dimaksud.

### 18. Test browser yang sesekali gagal

Satu test Selenium lulus saat dijalankan sendiri tetapi sesekali gagal pada run penuh dengan pesan `'tidak boleh kosong' not found in 'Gagal'`. Kesalahannya ada di test, bukan di aplikasi: Selenium membaca teks toast ketika animasinya baru menampilkan judul. AI tidak menambah jeda acak, melainkan mengubah test agar membaca elemen pesan secara langsung, lalu menjalankannya tiga kali berturut-turut untuk memastikan stabil.

### 19. Fitur keamanan baru memengaruhi test lama

Rate limiting menyimpan penghitung di cache, dan cache itu dipakai bersama oleh semua test dalam satu proses. Tanpa penanganan, test lama bisa gagal dengan 429 hanya karena test sebelumnya sudah memakai jatah. AI menambahkan `cache.clear()` pada setiap `setUp` yang terdampak, lalu menjalankan seluruh suite sebelum commit untuk membuktikan tidak ada yang rusak.

### 20. AI salah membaca rubrik penilaian

Ketika saya menunjukkan rubrik, AI menyebut kondisi pada kolom skor 1 ("any user can access, edit, or delete any data") sebagai alasan untuk mengembalikan modul kontak ke keadaan terbuka. Itu keliru: kolom skor rendah menggambarkan hasil yang harus dihindari, bukan acuan. Saya mengoreksinya ("jgn ikutin yang nilai 1, tapi nilai 4"), dan modul kontak tetap dibatasi. Pelajarannya, AI perlu diberi tahu arah penilaiannya dengan jelas, dan saya perlu membaca sendiri alasan di balik tiap rekomendasi.

Tidak semua temuan bersifat negatif. Saat memindahkan `getCookie` ke berkas bersama, AI menemukan salinan lain dari fungsi yang sama di widget chat pada `base.html`, lalu melaporkannya tanpa mengubahnya karena berada di luar permintaan. Perilaku seperti inilah yang saya harapkan, melapor, bukan diam-diam memperluas cakupan pekerjaan.

---

# Perbaikan Manual Setelah Menggunakan AI

AI berfungsi sebagai titik awal analisis. Setelah menerima saran, saya melakukan penyesuaian dan verifikasi secara manual

| Masalah | Bantuan AI | Perbaikan / Verifikasi Manual |
| --- | --- | --- |
| `.section-title` tidak terhubung ke heading | Menjelaskan hubungan selector HTML-CSS | Memeriksa dan memperbaiki class pada HTML |
| Kartu bertumpuk pada mobile | Memberi kemungkinan penyebab dan contoh media query | Menyesuaikan breakpoint dan layout lalu mengecek browser |
| `ModelForm` dan validasi | Menjelaskan konsep | Mencocokkan field form dengan model project |
| Serialization JSON | Menjelaskan alur model → serializer → JSON | Menguji endpoint dan response frontend |
| Duplicate key pada context | Membantu menemukan sumber masalah | Memeriksa context aktual dan memperbaiki struktur dictionary |
| Environment variable | Menjelaskan pola konfigurasi secret | Menyesuaikan dengan konfigurasi lokal/deployment PWS |
| Fitur `next` yang tidak diminta | Menulis kodenya tanpa diminta | Membatalkan commit tersebut sebelum di-*push* |
| Tombol star memakai `fetch` | Mengubah implementasi menjadi asinkronus | Mengembalikannya ke form HTML standar sesuai materi tutorial |
| Status pekerjaan yang salah dilaporkan | Menyatakan tahap sudah selesai | Memverifikasi ulang melalui `git diff` dan memintanya dikerjakan |
| Branch otorisasi belum ter-*merge* | Tidak ada | Ditemukan sendiri saat membaca `views.py`, lalu di-*merge* dan diperiksa ulang |
| Email tampil pada endpoint publik | Tidak ada | Mengganti akun uji dengan username biasa lalu memeriksa ulang `/api/skills/` |
| Bentuk respons AJAX menyimpang dari tutorial | Menulis versi awal dan mendaftar perbedaannya saat diminta membandingkan | Menyamakan seluruh bentuk respons dan cara JavaScript membacanya dengan tutorial |
| Branch `xss-protection` dan `search-debounce` belum ter-*merge* | Tidak ada | Ditemukan lewat `git log` dan `git branch --merged`, lalu di-*merge*. Konflik `projects.html` diselesaikan dengan mempertahankan kedua fitur |
| Test Skill gagal `13 != 1` | Menulis test dengan asumsi database kosong | Menelusuri penyebabnya (data migration menyeed 12 skill), lalu test memakai nama unik dan jumlah relatif terhadap nilai awal |
| Pesan 403 Editor berbahasa Inggris | Menyerahkannya kembali sebagai "keterbatasan" | Meminta AI memperbaikinya, lalu `message` ditambahkan pada permission dan ada test yang memeriksa isinya |
| Trailer `Co-Authored-By` pada commit | Bawaan Claude Code menyarankannya | Meminta menghilangkannya, lalu memeriksa `git log` bernilai 0 trailer |
| Perilaku JavaScript belum teruji | Menyatakan tidak punya alat browser | Meminta hasil maksimal, lalu enam skenario browser dijalankan lewat Selenium untuk tiap peran, dan dua kegagalan awal terbukti salah skrip, bukan salah aplikasi |
| `DEBUG = True` di-*hardcode* untuk produksi | Tidak menyadarinya saat menulis fitur | Ditemukan saat audit terhadap rubrik, lalu diperbaiki dengan test yang gagal lebih dulu |
| Modul contacts bisa diubah siapa saja | Menulis view tanpa pemeriksaan peran pada Tutorial 6 | Ditemukan saat membaca kode, lalu dibatasi untuk pemilik dengan test otorisasi dan validasi |
| Test lama gagal 429 setelah rate limiting | Menambah fitur tanpa memikirkan cache bersama antar test | Seluruh suite dijalankan sebelum commit, lalu cache dibersihkan di `setUp` |
| Test toast Selenium sesekali gagal | Menulis test yang bergantung pada animasi | Test diubah membaca elemen pesan dan dijalankan berulang kali sampai stabil |
| Rekomendasi mengembalikan kontak ke keadaan terbuka | Membaca deskripsi skor 1 pada rubrik sebagai acuan | Saya mengoreksi arahnya ke deskripsi skor 4, lalu audit diulang dan modul kontak tetap dibatasi |
| Pesan error API berbahasa Inggris | Mengandalkan teks bawaan DRF | Ditemukan saat audit UX toast, lalu ditambahkan `api_errors.py` dengan test yang gagal lebih dulu |
| `getCookie` hanya tersedia di halaman Projects | Memindahkannya ke `static/js/utils.js` dan melaporkan salinan lain di widget chat | Menguji ulang tambah project setelah pemindahan dan membiarkan salinan lokal widget chat tetap terpisah |

---

## Refleksi Penggunaan AI

Penggunaan AI paling membantu ketika saya menggunakannya untuk **memahami alasan di balik suatu solusi**, bukan hanya meminta kode final.

Perbedaan yang saya rasakan adalah:

```text
"Berikan saya kode yang benar"
                ↓
   Mendapatkan solusi
                ↓
       Pemahaman terbatas
```

dibandingkan:

```text
"Jelaskan mengapa masalah ini terjadi
 pada kode saya dan bagaimana cara
 menguji apakah solusinya benar"
                ↓
       Memahami penyebab
                ↓
       Mencoba solusi
                ↓
           Melakukan test
                ↓
        Memahami hasil akhir
```

Pelajaran terbesar dari Tutorial 5 dan Tugas 5 adalah bahwa pekerjaan yang dibagi menjadi banyak branch kecil memang memudahkan saya memeriksa hasil AI, tetapi menuntut disiplin pada hal yang bukan kode: memastikan setiap branch benar-benar masuk ke `main`, dan memverifikasi laporan AI lewat perintah Git atau pengujian langsung, bukan hanya mempercayai ringkasannya.

Pada Tugas 6 pelajarannya bertambah: laporan "selesai" dari AI belum berarti selesai. Test hijau tidak membuktikan JavaScript di browser berjalan, Karena itu pada Tugas 6 saya menuntut dua bukti tambahan: percobaan dengan sengaja merusak permission agar test gagal, dan klik-through otomatis di browser untuk setiap peran.

AI saya gunakan sebagai **learning companion**. Keberhasilan suatu solusi tetap saya ukur dari implementasi dan pengujian pada project yang sebenarnya^^

---

# Catatan Keamanan

Project ini merupakan project pembelajaran dan belum dimaksudkan sebagai aplikasi production

Beberapa prinsip yang sudah saya terapkan:

- Form perubahan data menggunakan CSRF protection, dan permintaan AJAX membawa token yang sama melalui header `X-CSRFToken`.
- Secret/API key disimpan melalui environment variable dan tidak ditulis pada source code.
- Password pengguna tidak pernah disimpan sebagai teks biasa, melainkan di-*hash* oleh sistem autentikasi bawaan Django.
- Cookie hanya menyimpan token sesi dan waktu login terakhir, bukan data kredensial.
- Pembatasan hak akses dilakukan di **sisi server**, bukan hanya dengan menyembunyikan tombol pada template.
- Endpoint AJAX membalas JSON 403 untuk pengguna yang tidak berhak, bukan redirect ke halaman login yang bisa disalahartikan sebagai keberhasilan.
- Data yang ditampilkan lewat JavaScript dirakit dengan `textContent`, bukan `innerHTML`, sehingga isinya tidak pernah ditafsirkan sebagai HTML.
- Input teks pada form dibersihkan dari tag HTML di server dengan `strip_tags` sebagai lapisan tambahan.
- Endpoint JSON publik tidak menampilkan id internal database maupun data kontak pengguna.

Mekanisme proteksi berbasis kode rahasia yang digunakan pada Tugas 3 sudah dihapus sepenuhnya dan digantikan oleh sistem autentikasi serta otorisasi Django.

Untuk aplikasi production, konfigurasi seperti `DEBUG = False`, penggunaan HTTPS, serta pengelolaan sesi dan cookie yang lebih ketat tetap diperlukan.

---

# Referensi

- [Django: The Development Server](https://docs.djangoproject.com/en/5.2/intro/tutorial01/#the-development-server)
- [Django: Model Forms](https://docs.djangoproject.com/en/5.2/topics/forms/modelforms/)
- [Django: Serialization](https://docs.djangoproject.com/en/5.2/topics/serialization/)
- [Django: CSRF Protection](https://docs.djangoproject.com/en/5.2/ref/csrf/)
- [Django: Using the Django authentication system](https://docs.djangoproject.com/en/5.2/topics/auth/default/)
- [Django: How to use sessions](https://docs.djangoproject.com/en/5.2/topics/http/sessions/)
- [Django: Data Migrations](https://docs.djangoproject.com/en/5.2/topics/migrations/#data-migrations)
- [Django: JsonResponse](https://docs.djangoproject.com/en/5.2/ref/request-response/#jsonresponse-objects)
- [Django: strip_tags](https://docs.djangoproject.com/en/5.2/ref/utils/#django.utils.html.strip_tags)
- [MDN: Using the Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)
- [MDN: async function dan await](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Async_JS)
- [MDN: Popover API](https://developer.mozilla.org/en-US/docs/Web/API/Popover_API)
- [OWASP: Cross Site Scripting (XSS)](https://owasp.org/www-community/attacks/xss/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Shields.io](https://shields.io/badges/static-badge)