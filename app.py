from flask import Flask, render_template, request, jsonify
import json
import mysql.connector

app = Flask(__name__)

class Interprete:
    def __init__ (self, diccionario_ventas):
        self.diccionario_ventas = diccionario_ventas
        self.contador = 0
    def agregar_venta(self, nombre_empresa, fecha, valor_venta):
        self.contador = self.contador + 1
        prefix = "venta_"
        self.diccionario_ventas["ventas"][f"{prefix}{self.contador}"] = {
            "nombre_empresa": nombre_empresa,
            "fecha": fecha,
            "valor_venta": valor_venta
        }
    def reiniciar_diccionario(self):
        self.diccionario_ventas = ventas_init
        self.contador = 0

ventas_init = {
    "ventas": {}
}

db_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "mysql_admin_Colombia*1",
    "database": "sw-arch"
}
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

interprete = Interprete(ventas_init)

@app.route("/", methods=["GET"])
def get_root():
    return render_template("index.html"), 200

@app.route("/post_data", methods=["POST"])
def post_data():
    if request.content_type == 'text/plain':
        # Ejemplo: MIEMPRESA          2023-10-2858000000
        data = request.data.decode('utf-8')
        nombre_empresa = data[0:19].strip()
        fecha = data[19:29].strip()
        valor_venta = data[29:].strip()
        interprete.agregar_venta(nombre_empresa, fecha, valor_venta)
        return f"Received plain text data: {data}", 200
    elif request.content_type == "application/json":
        # Ejemplo: {"fecha": "2023-10-28", "nombre_empresa": "MIEMPRESA", "valor_venta": "58000000"}
        data = request.get_json()
        interprete.agregar_venta(data["nombre_empresa"], data["fecha"], data["valor_venta"])
        return f"Received json data:\n" + json.dumps(data), 200
    else:
        return f"Incorrect data format", 400

@app.route("/get_ventas", methods=["GET"])
def get_ventas():
    return jsonify(interprete.diccionario_ventas), 200

@app.route("/reiniciar_diccionario", methods=["GET"])
def reiniciar_diccionario():
    interprete.reiniciar_diccionario()
    return f"Diccionario de datos reinicializado.", 200

@app.route("/persistir_datos", methods=["GET"])
def persistir_datos():
    insert_query = "INSERT INTO ventas (empresa_local, valor_venta, fecha_venta) VALUES (%s, %s, %s)"
    for venta in interprete.diccionario_ventas:
        data_to_insert = (venta["nombre_empresa"], venta["valor_venta"], venta["fecha"])
        cursor.execute(insert_query, data_to_insert)
        conn.commit()
    cursor.close()
    conn.close()
    return f"Datos persistidos en la db.", 200

@app.route("/cargar_desde_db", methods=["GET"])
def cargar_desde_db():
    interprete.reiniciar_diccionario(ventas_init)
    select_query = "SELECT empresa_local, valor_venta, fecha_venta FROM ventas"
    cursor.execute(select_query)
    for venta in cursor.fetchall():
        interprete.agregar_venta(venta["empresa_local"], venta["fecha_venta"], venta["valor_venta"])
    cursor.close()
    conn.close()
    return f"Datos persistidos en la db.", 200

if __name__ == '__main__':
    app.run(debug=False)