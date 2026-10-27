from flask import Flask, render_template, request
from statistics import mean, median, multimode
from collections import Counter

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    hasil = None
    error = None
    teks_data = ""
    if request.method == "POST":
        teks_data = request.form.get("data", "").strip()
        try:
            if not teks_data:
                raise ValueError
            teks = teks_data.replace(",", " ").replace(";", " ")
            data = [float(x) for x in teks.split()]
            if not data:
                raise ValueError
            frekuensi = Counter(data)
            modus = multimode(data)
            ada_modus = max(frekuensi.values()) > 1
            def fmt(x):
                return str(int(x)) if float(x).is_integer() else str(x)
            pasangan = sorted(frekuensi.items())
            hasil = {
                "jumlah": len(data), "mean": round(mean(data), 2),
                "median": median(data),
                "modus": ", ".join(fmt(x) for x in modus) if ada_modus else "Tidak ada modus",
                "maksimum": max(data), "minimum": min(data),
                "jangkauan": round(max(data)-min(data), 2),
                "label": [fmt(x) for x, _ in pasangan],
                "frekuensi": [n for _, n in pasangan]
            }
        except (ValueError, TypeError):
            error = "Data tidak valid. Masukkan angka, pisahkan dengan koma atau spasi."
    return render_template("index.html", hasil=hasil, error=error, teks_data=teks_data)

if __name__ == "__main__":
    app.run(debug=True)
