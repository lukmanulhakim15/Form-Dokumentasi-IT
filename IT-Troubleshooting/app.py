
from flask import Flask, request, render_template_string, url_for
import requests
import json
import os
from datetime import date

from config import BOT_TOKEN, CHAT_ID


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 310 * 1024 * 1024

TELEGRAM = f"https://api.telegram.org/bot{BOT_TOKEN}/"


HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IT Troubleshooting Documentation</title>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style>
* {
    box-sizing: border-box;
}

:root {
    --navy: #0b1729;
    --blue: #2563eb;
    --text: #1e293b;
    --muted: #64748b;
}

body {
    margin: 0;
    min-height: 100vh;
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: var(--text);
    background:
        radial-gradient(ellipse at 10% 10%, rgba(59,130,246,.35), transparent 35%),
        radial-gradient(ellipse at 90% 85%, rgba(96,165,250,.30), transparent 35%),
        linear-gradient(135deg, #0b1729 0%, #172554 48%, #1d4ed8 100%);
    background-attachment: fixed;
}

.background-decoration {
    position: fixed;
    inset: 0;
    overflow: hidden;
    pointer-events: none;
    z-index: 0;
}

.circle {
    position: absolute;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,.13);
}

.circle-one {
    width: 450px;
    height: 450px;
    top: -190px;
    right: -100px;
}

.circle-two {
    width: 300px;
    height: 300px;
    bottom: -130px;
    left: -100px;
}

.circle-three {
    width: 130px;
    height: 130px;
    top: 45%;
    right: 8%;
    background: rgba(255,255,255,.035);
}

.glow {
    position: absolute;
    width: 250px;
    height: 250px;
    border-radius: 50%;
    background: rgba(96,165,250,.12);
    filter: blur(70px);
}

.glow-one {
    top: 20%;
    left: -100px;
}

.glow-two {
    bottom: 10%;
    right: -100px;
}

.header {
    position: relative;
    z-index: 1;
    padding: 38px 20px 85px;
    color: #fff;
}

.header-content {
    max-width: 1000px;
    margin: auto;
}

.brand {
    display: flex;
    align-items: center;
    gap: 15px;
}

.brand-logo {
    width: 58px;
    height: 58px;
    flex: 0 0 58px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 5px;
    object-fit: contain;
    border-radius: 14px;
    background: rgba(255,255,255,.96);
    border: 1px solid rgba(255,255,255,.4);
    box-shadow: 0 5px 18px rgba(0,0,0,.16);
}

.brand h1 {
    margin: 0;
    font-size: 20px;
    font-weight: 800;
    letter-spacing: 1px;
}

.brand p {
    margin: 5px 0 0;
    color: #bfdbfe;
    font-size: 10px;
    letter-spacing: 1.5px;
    font-weight: 600;
}

.header-description {
    margin-top: 38px;
}

.tagline {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 7px 13px;
    margin-bottom: 15px;
    border: 1px solid rgba(255,255,255,.2);
    background: rgba(255,255,255,.10);
    border-radius: 30px;
    color: #dbeafe;
    font-size: 11px;
    font-weight: 700;
}

.header-description h2 {
    margin: 0 0 12px;
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -.8px;
}

.header-description p {
    max-width: 650px;
    margin: 0;
    color: #dbeafe;
    font-size: 13px;
    line-height: 1.9;
}

.main-container {
    position: relative;
    z-index: 2;
    max-width: 1000px;
    margin: -48px auto 40px;
    padding: 0 18px;
}

.form-card {
    overflow: hidden;
    background: #fff;
    border: 1px solid rgba(255,255,255,.6);
    border-radius: 19px;
    box-shadow:
        0 25px 60px rgba(0,0,0,.20),
        0 5px 15px rgba(0,0,0,.05);
}

.card-body-custom {
    padding: 34px;
}

.section-heading {
    display: flex;
    align-items: center;
    gap: 14px;
    padding-bottom: 23px;
    margin-bottom: 25px;
    border-bottom: 1px solid #edf0f5;
}

.section-icon {
    width: 48px;
    height: 48px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 13px;
    background: #eaf1ff;
    color: #2563eb;
    font-size: 21px;
}

.section-heading h3 {
    margin: 0;
    color: #0f172a;
    font-size: 17px;
    font-weight: 800;
}

.section-heading p {
    margin: 5px 0 0;
    color: #64748b;
    font-size: 11px;
}

.field {
    height: 100%;
    padding: 17px;
    border-radius: 12px;
    border: 1px solid #e6ebf2;
    background: #f8fafc;
    transition: .2s ease;
}

.field:hover {
    border-color: #bfdbfe;
    background: #f7faff;
}

.field label {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 10px;
    color: #334155;
    font-size: 12px;
    font-weight: 800;
}

.field label i {
    color: #2563eb;
    font-size: 15px;
}

.form-control,
.form-select {
    width: 100%;
    min-height: 45px;
    padding: 11px 13px;
    border: 1px solid #dbe3ee;
    border-radius: 8px;
    background: #fff;
    color: #1e293b;
    font-family: inherit;
    font-size: 12px;
    box-shadow: none;
    transition: .2s ease;
}

.form-control:hover,
.form-select:hover {
    border-color: #93b4ed;
}

.form-control:focus,
.form-select:focus {
    border-color: #2563eb;
    box-shadow: 0 0 0 .20rem rgba(37,99,235,.12);
}

.form-control::placeholder {
    color: #a0aec0;
}

textarea.form-control {
    min-height: 120px;
    resize: vertical;
    line-height: 1.8;
}

.form-control[type=file] {
    padding: 9px;
    border: 1px dashed #9aacc4;
    background: #fff;
}

.form-control[type=file]::file-selector-button {
    margin-right: 10px;
    padding: 9px 12px;
    border: 0;
    border-radius: 6px;
    background: #eaf1ff;
    color: #1d4ed8;
    font-size: 11px;
    font-weight: 800;
    cursor: pointer;
}

.small-info {
    margin-top: 9px;
    color: #64748b;
    font-size: 10px;
    line-height: 1.8;
}

.form-note {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 13px 15px;
    margin-top: 23px;
    background: #eff6ff;
    border: 1px solid #dbeafe;
    border-radius: 9px;
    color: #1e40af;
    font-size: 11px;
    line-height: 1.7;
}

.form-note i {
    font-size: 16px;
}

.submit-area {
    margin-top: 22px;
}

.btn-submit {
    width: 100%;
    padding: 15px 20px;
    border: 0;
    border-radius: 9px;
    background: linear-gradient(110deg, #2563eb, #1d4ed8);
    color: #fff;
    font-family: inherit;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: .5px;
    cursor: pointer;
    transition: .25s ease;
    box-shadow: 0 7px 17px rgba(37,99,235,.22);
}

.btn-submit:hover {
    background: linear-gradient(110deg, #1d4ed8, #1e40af);
    transform: translateY(-2px);
    box-shadow: 0 10px 22px rgba(37,99,235,.28);
}

.btn-submit i {
    margin-right: 8px;
    font-size: 15px;
}

.message {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 14px 16px;
    margin-bottom: 22px;
    border-radius: 9px;
    font-size: 12px;
    line-height: 1.7;
}

.message.success {
    color: #166534;
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
}

.message.error {
    color: #991b1b;
    background: #fef2f2;
    border: 1px solid #fecaca;
}

.footer {
    position: relative;
    z-index: 1;
    padding: 0 15px 30px;
    text-align: center;
    color: #dbeafe;
    font-size: 11px;
    line-height: 1.9;
}

.footer strong {
    color: #fff;
    font-weight: 800;
}

.footer-line {
    width: 45px;
    height: 3px;
    margin: 0 auto 12px;
    border-radius: 5px;
    background: #93c5fd;
}

@media (max-width: 700px) {
    .header {
        padding: 28px 18px 70px;
    }

    .header-description {
        margin-top: 30px;
    }

    .header-description h2 {
        font-size: 25px;
    }

    .main-container {
        margin-top: -37px;
        padding: 0 13px;
    }

    .card-body-custom {
        padding: 22px 16px;
    }

    .field {
        padding: 14px;
    }

    .section-heading {
        gap: 11px;
    }
}

@media (max-width: 400px) {
    .brand h1 {
        font-size: 16px;
    }

    .brand-logo {
        width: 46px;
        height: 46px;
        flex-basis: 46px;
    }

    .header-description h2 {
        font-size: 22px;
    }

    .card-body-custom {
        padding: 19px 13px;
    }

    .form-control,
    .form-select {
        font-size: 11px;
    }
}
</style>
</head>

<body>

<div class="background-decoration">
    <div class="circle circle-one"></div>
    <div class="circle circle-two"></div>
    <div class="circle circle-three"></div>
    <div class="glow glow-one"></div>
    <div class="glow glow-two"></div>
</div>

<header class="header">
    <div class="header-content">

        <div class="brand">
            <!-- Simpan logo di: static/images/Logo-smku.png -->
            <img
                class="brand-logo"
                src="{{ url_for('static', filename='images/Logo-smku.png') }}"
                alt="Logo PT. Samugara Multikarya Utama"
                onerror="this.style.display='none'; document.getElementById('logoFallback').style.display='flex';"
            >

            <div
                id="logoFallback"
                style="display:none;width:58px;height:58px;align-items:center;justify-content:center;border-radius:14px;background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.25);font-size:25px;color:white;"
            >
                <i class="bi bi-building"></i>
            </div>

            <div>
                <h1>IT SUPPORT SYSTEM</h1>
                <p>DOCUMENTATION &amp; MONITORING</p>
            </div>
        </div>

        <div class="header-description">
            <div class="tagline">
                <i class="bi bi-shield-check"></i>
                IT SUPPORT &amp; NETWORK INFRASTRUCTURE
            </div>

            <h2>IT Troubleshooting</h2>

            <p>
                Sistem dokumentasi pekerjaan IT Support, pemeliharaan perangkat,
                jaringan, dan infrastruktur teknologi informasi. Catat setiap
                pekerjaan dengan dokumentasi yang terstruktur dan mudah dipantau.
            </p>
        </div>

    </div>
</header>

<main class="main-container">

    <div class="form-card">
        <div class="card-body-custom">

            <div class="section-heading">
                <div class="section-icon">
                    <i class="bi bi-clipboard-data"></i>
                </div>

                <div>
                    <h3>Formulir Dokumentasi</h3>
                    <p>Lengkapi informasi pekerjaan troubleshooting</p>
                </div>
            </div>

            {% if message %}
            <div class="message {% if color == 'green' %}success{% else %}error{% endif %}">

                {% if color == 'green' %}
                    <i class="bi bi-check-circle-fill"></i>
                {% else %}
                    <i class="bi bi-exclamation-triangle-fill"></i>
                {% endif %}

                <div>{{ message }}</div>
            </div>
            {% endif %}

            <form action="/send" method="POST" enctype="multipart/form-data">

                <div class="row g-3">

                    <div class="col-md-6">
                        <div class="field">
                            <label>
                                <i class="bi bi-calendar-event"></i>
                                Tanggal pekerjaan
                            </label>

                            <input
                                class="form-control"
                                type="date"
                                name="tanggal"
                                value="{{ today }}"
                                required
                            >
                        </div>
                    </div>

                    <div class="col-md-6">
                        <div class="field">
                            <label>
                                <i class="bi bi-grid"></i>
                                Jenis troubleshooting
                            </label>

                            <select class="form-select" name="kategori" required>
                                <option value="">Pilih kategori</option>
                                <option>PC / Laptop</option>
                                <option>Printer / Scanner</option>
                                <option>LAN / Jaringan</option>
                                <option>Internet / WiFi</option>
                                <option>CCTV</option>
                                <option>Server</option>
                                <option>Aplikasi / Sistem</option>
                                <option>Instalasi / Konfigurasi</option>
                                <option>Pemeliharaan</option>
                                <option>Lainnya</option>
                            </select>
                        </div>
                    </div>

                    <div class="col-md-6">
                        <div class="field">
                            <label>
                                <i class="bi bi-diagram-3"></i>
                                Departemen / Divisi
                            </label>

                            <select class="form-select" name="Divisi" required>
                                <option value="">Pilih departemen / divisi</option>
                                <option>IT Support</option>
                                <option>HR / Human Resources</option>
                                <option>Finance / Keuangan</option>
                                <option>Marketing Komersial</option>
                                <option>Project Engineer</option>
                                <option>Admin Fasgal</option>
                                <option>Gudang</option>
                                <option>Produksi</option>
                                <option>Security</option>
                                <option>HSSE</option>
                                <option>QC</option>
                                <option>GA</option>
                                <option>Lainnya</option>
                            </select>
                        </div>
                    </div>

                    <div class="col-12">
                        <div class="field">
                            <label>
                                <i class="bi bi-exclamation-circle"></i>
                                Permasalahan
                            </label>

                            <textarea
                                class="form-control"
                                name="masalah"
                                required
                                placeholder="Jelaskan permasalahan yang ditemukan..."
                            ></textarea>
                        </div>
                    </div>

                    <div class="col-md-6">
                        <div class="field">
                            <label>
                                <i class="bi bi-flag"></i>
                                Status pekerjaan
                            </label>

                            <select class="form-select" name="status">
                                <option>Selesai</option>
                                <option>Dalam proses</option>
                                <option>Belum selesai</option>
                                <option>Perlu tindak lanjut</option>
                            </select>
                        </div>
                    </div>

                    <div class="col-md-6">
                        <div class="field">
                            <label>
                                <i class="bi bi-images"></i>
                                Foto dokumentasi
                            </label>

                            <input
                                class="form-control"
                                type="file"
                                name="foto"
                                accept="image/jpeg,image/png"
                                multiple
                            >

                            <div class="small-info">
                                <i class="bi bi-info-circle"></i>
                                Format JPG atau PNG.<br>
                                Maksimal 30 foto, 10 MB per foto.
                            </div>
                        </div>
                    </div>

                </div>

                <div class="form-note">
                    <i class="bi bi-info-circle-fill"></i>

                    <div>
                        Pastikan seluruh informasi pekerjaan telah diisi dengan
                        benar sebelum mengirimkan laporan.
                    </div>
                </div>

                <div class="submit-area">
                    <button type="submit" class="btn-submit">
                        <i class="bi bi-telegram"></i>
                        KIRIM LAPORAN KE TELEGRAM
                    </button>
                </div>

            </form>

        </div>
    </div>

</main>

<footer class="footer">
    <div class="footer-line"></div>

    <strong>IT Troubleshooting Documentation System</strong><br>
    IT Support &amp; Network Infrastructure<br>
    <span>© 2026 IT Department</span>
</footer>

</body>
</html>
"""


# ==========================================
# TELEGRAM API
# ==========================================
def telegram(method, data=None, files=None):
    response = requests.post(
        TELEGRAM + method,
        data=data,
        files=files,
        timeout=180
    )

    try:
        result = response.json()
    except ValueError:
        raise Exception(
            f"Respons Telegram tidak valid: HTTP {response.status_code}"
        )

    if not response.ok or not result.get("ok"):
        raise Exception(
            result.get(
                "description",
                f"Telegram error HTTP {response.status_code}"
            )
        )

    return result


# ==========================================
# SEND SINGLE PHOTO
# ==========================================
def send_photo_single(photo, caption):
    photo.stream.seek(0)

    files = {
        "photo": (
            photo.filename,
            photo.stream,
            photo.mimetype or "image/jpeg"
        )
    }

    return telegram(
        "sendPhoto",
        data={
            "chat_id": CHAT_ID,
            "caption": caption[:1024]
        },
        files=files
    )


# ==========================================
# SEND PHOTO ALBUM
# ==========================================
def send_photo_album(photos, caption):
    media = []
    files = {}

    for index, photo in enumerate(photos):
        key = f"photo{index}"
        photo.stream.seek(0)

        item = {
            "type": "photo",
            "media": f"attach://{key}"
        }

        if index == 0:
            item["caption"] = caption[:1024]

        media.append(item)

        files[key] = (
            photo.filename,
            photo.stream,
            photo.mimetype or "image/jpeg"
        )

    return telegram(
        "sendMediaGroup",
        data={
            "chat_id": CHAT_ID,
            "media": json.dumps(media)
        },
        files=files
    )


# ==========================================
# HOME
# ==========================================
@app.route("/")
def home():
    return render_template_string(
        HTML,
        today=date.today().isoformat(),
        message="",
        color="green"
    )


# ==========================================
# SEND REPORT
# ==========================================
@app.route("/send", methods=["POST"])
def send():
    try:
        tanggal = request.form.get("tanggal", "").strip()
        kategori = request.form.get("kategori", "").strip()

        # Nama field HTML dan backend harus sama: name="Divisi"
        divisi = request.form.get("Divisi", "").strip()

        masalah = request.form.get("masalah", "").strip()
        status = request.form.get("status", "-").strip()

        if not all([tanggal, kategori, divisi, masalah]):
            raise Exception(
                "Mohon isi tanggal, kategori, divisi, dan permasalahan."
            )

        caption = f"""🛠️ LAPORAN DOKUMENTASI IT

📅 Tanggal: {tanggal}
🏷️ Kategori: {kategori}
📍 Divisi: {divisi}
🚦 Status: {status}

❗ PERMASALAHAN:
{masalah}"""

        photos = [
            p for p in request.files.getlist("foto")
            if p and p.filename
        ]

        if len(photos) > 30:
            raise Exception("Maksimal 30 foto per laporan.")

        for photo in photos:
            if photo.mimetype not in ["image/jpeg", "image/png"]:
                raise Exception(
                    f"Format foto tidak didukung: {photo.filename}"
                )

            photo.stream.seek(0, os.SEEK_END)
            size = photo.stream.tell()
            photo.stream.seek(0)

            if size > 10 * 1024 * 1024:
                raise Exception(
                    f"Ukuran foto maksimal 10 MB: {photo.filename}"
                )

            if size == 0:
                raise Exception(f"Foto kosong: {photo.filename}")

        # Kirim laporan teks, lalu foto jika ada
        telegram(
            "sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": caption
            }
        )

        if len(photos) == 1:
            send_photo_single(
                photos[0],
                "📷 Dokumentasi pekerjaan"
            )

        elif len(photos) >= 2:
            for start in range(0, len(photos), 10):
                send_photo_album(
                    photos[start:start + 10],
                    "📷 Dokumentasi pekerjaan"
                )

        return render_template_string(
            HTML,
            today=date.today().isoformat(),
            message=f"Berhasil! Laporan dan {len(photos)} foto telah dikirim ke Telegram.",
            color="green"
        )

    except Exception as e:
        return render_template_string(
            HTML,
            today=date.today().isoformat(),
            message="Pengiriman gagal: " + str(e),
            color="red"
        )


# ==========================================
# UPLOAD SIZE ERROR
# ==========================================
@app.errorhandler(413)
def file_too_large(error):
    return render_template_string(
        HTML,
        today=date.today().isoformat(),
        message="Ukuran total upload terlalu besar.",
        color="red"
    ), 413


# ==========================================
# RUN APPLICATION
# ==========================================
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
