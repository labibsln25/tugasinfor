import os
import sys
import base64
import webview

def get_resource_path(relative_path):
    """Mendapatkan lokasi file index.html baik saat mode .py maupun setelah jadi .exe"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def get_exe_dir():
    """Mendapatkan folder tempat aplikasi .exe berada untuk menyimpan Struk PDF & HTML"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

class PosBridgeAPI:
    def simpan_struk_html(self, nama_file, isi_html):
        """Menyimpan file Struk_INV-....html langsung di sebelah aplikasi .exe"""
        try:
            path_lengkap = os.path.join(get_exe_dir(), nama_file)
            with open(path_lengkap, "w", encoding="utf-8") as f:
                f.write(isi_html)
            return {"status": "success", "path": path_lengkap}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def simpan_file_pdf_base64(self, nama_file, data_uri):
        """Menyimpan file Struk_INV-....pdf langsung di sebelah aplikasi .exe"""
        try:
            header, encoded = data_uri.split(",", 1) if "," in data_uri else ("", data_uri)
            pdf_bytes = base64.b64decode(encoded)
            path_lengkap = os.path.join(get_exe_dir(), nama_file)
            with open(path_lengkap, "wb") as f:
                f.write(pdf_bytes)
            return {"status": "success", "path": path_lengkap}
        except Exception as e:
            return {"status": "error", "message": str(e)}

if __name__ == '__main__':
    api = PosBridgeAPI()
    html_file = get_resource_path("index.html")

    window = webview.create_window(
        title="Smart POS Toko Serba Ada — Kasir: Labib",
        url=html_file,
        js_api=api,
        width=1280,
        height=820,
        min_size=(960, 640),
        text_select=False
    )

    webview.start()