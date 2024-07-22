from flask import Flask, render_template, redirect, url_for, session, request, flash
import time

app = Flask(__name__)
app.secret_key = 'supersecretkey'

class Cliente:
    def __init__(self, nombre, apellidos, numero_tarjeta, contraseña, monto, tipo_cliente):
        self.nombre = nombre
        self.apellidos = apellidos
        self.numero_tarjeta = numero_tarjeta
        self.contraseña = contraseña
        self.monto = monto
        self.tipo_cliente = tipo_cliente

    def registrar_interaccion(self):
        # Completar: Registrar la fecha y hora actuales en fecha_interaccion
        pass

    def consultar_saldo(self):
        return self.monto

    def depositar(self, cantidad):
        self.monto += cantidad

    def retirar(self, cantidad):
        if self.monto >= cantidad:
            self.monto -= cantidad
        else:
            return False
        return True

clientes = [
    Cliente('Juan', 'Perez', '1234567890123456', '4321', 1500.00, 'Premium'),
    Cliente('Maria', 'Gomez', '9876543210987654', '1234', 2000.00, 'Estandar')
]

@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        numero_tarjeta = request.form['numero_tarjeta']
        contraseña = request.form['contraseña']
        
        for cliente in clientes:
            if cliente.numero_tarjeta == numero_tarjeta and cliente.contraseña == contraseña:
                session['cliente'] = cliente.numero_tarjeta
                return redirect(url_for('menu'))
        
        flash("Número de tarjeta de crédito o contraseña incorrectos.")
    
    return render_template('index.html')

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if 'cliente' not in session:
        return redirect(url_for('login'))
    
    cliente_actual = next(cliente for cliente in clientes if cliente.numero_tarjeta == session['cliente'])

    if request.method == 'POST':
        if 'consultar' in request.form:
            saldo = cliente_actual.consultar_saldo()
            flash(f"Saldo actual: ${saldo:.2f}")
        elif 'depositar' in request.form:
            cantidad = float(request.form['cantidad'])
            cliente_actual.depositar(cantidad)
            flash(f"Se ha depositado ${cantidad:.2f}.")
        elif 'retirar' in request.form:
            cantidad = float(request.form['cantidad'])
            if cliente_actual.retirar(cantidad):
                flash(f"Se ha retirado ${cantidad:.2f}.")
            else:
                flash("Fondos insuficientes.")
    
    return render_template('menu.html')

if __name__ == '__main__':
    app.run(debug=True)
