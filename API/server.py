from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
from datetime import datetime
import os

# -------------------------------
# CONFIGURAÇÕES DE CAMINHOS
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INSTRUMENTOS_XLSX = os.path.join(BASE_DIR, "Site_Publicado", "base_instrumentos.xlsx")
REGISTROS_XLSX = os.path.join(BASE_DIR, "registros_execucao.xlsx")

# -------------------------------
# APP FLASK
# -------------------------------
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# -------------------------------
# FUNÇÃO DE BUSCA
# -------------------------------
def buscar_instrumento(tag):
    try:
        df = pd.read_excel(INSTRUMENTOS_XLSX, engine="openpyxl", dtype=str)
    except FileNotFoundError:
        app.logger.error("Arquivo base_instrumentos.xlsx não encontrado")
        return None
    except Exception as e:
        app.logger.error("Erro ao ler base_instrumentos.xlsx: %s", e)
        return None

    df["TAG"] = df["TAG"].astype(str).str.strip()
    linha = df[df["TAG"].str.upper() == str(tag).upper()]

    if linha.empty:
        return None

    row = linha.iloc[0].to_dict()
    for k, v in row.items():
        if pd.isna(v):
            row[k] = None
    return row

# -------------------------------
# ROTAS
# -------------------------------
@app.route("/")
def pagina():
    return render_template("index.html")


@app.route("/dados/<tag>", methods=["GET"])
def dados_tag(tag):
    instrumento = buscar_instrumento(tag)
    if not instrumento:
        return jsonify({"error": "instrumento não encontrado"}), 404
    return jsonify(instrumento)


@app.route("/confirmar", methods=["POST"])
def confirmar():
    data = request.get_json(force=True, silent=True)
    if not data or "tag" not in data:
        return jsonify({"error": "json inválido, informe campo 'tag'"}), 400

    tag = data.get("tag")
    tecnico = data.get("tecnico", "")
    ordem = data.get("ordem", "")
    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "Finalizado"

    # Cria o arquivo se não existir
    if not os.path.exists(REGISTROS_XLSX):
        df0 = pd.DataFrame(columns=["TAG", "ORDEM", "TECNICO", "DATA_HORA", "STATUS"])
        df0.to_excel(REGISTROS_XLSX, index=False, engine="openpyxl")

    try:
        df = pd.read_excel(REGISTROS_XLSX, engine="openpyxl", dtype=str)
    except Exception as e:
        return jsonify({"error": f"erro ao acessar arquivo de registros: {e}"}), 500

    novo = {"TAG": tag, "ORDEM": ordem, "TECNICO": tecnico, "DATA_HORA": horario, "STATUS": status}
    df.loc[len(df)] = novo

    try:
        df.to_excel(REGISTROS_XLSX, index=False, engine="openpyxl")
    except PermissionError:
        return jsonify({"error": "registros_execucao.xlsx está aberto (feche e tente novamente)"}), 500

    return jsonify({"status": "ok", "tag": tag, "hora": horario})

# -------------------------------
# EXECUÇÃO LOCAL
# -------------------------------
if __name__ == "__main__":
    # Para execução local
    app.run(host="0.0.0.0", port=5000, debug=True)
