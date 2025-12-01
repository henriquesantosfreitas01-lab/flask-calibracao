import qrcode
import pandas as pd
import os

df = pd.read_excel(r"C:\Users\guilherme.h.santos\Desktop\Pasta rapida\PY\Site\Site\base_instrumentos.xlsx")


# cria pasta caso não exista
os.makedirs("qrcodes", exist_ok=True)


for index, row in df.iterrows():
    tag = row["TAG"]

    # URL correta do Flask
    url = f"http://10.62.166.62:5000/?tag={tag}"

    img = qrcode.make(url)
    img.save(f"qrcodes/{tag}.png")


print("QR Codes gerados com sucesso!")
