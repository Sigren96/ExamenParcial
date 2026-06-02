from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Esto le da permiso a Vercel para conectarse

@app.route("/")
def home():
    # En vez de un HTML, ahora devolvemos datos puros (JSON)
    return jsonify({
        "estado": "Exito",
        "mensaje": "¡El backend en Render está funcionando perfectamente!"
    })

if __name__ == "__main__":
    app.run(debug=True)