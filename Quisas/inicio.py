import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from pymongo import MongoClient
from flask import redirect, url_for
from flask import Flask, render_template, request

# Crear una conexión a MongoDB
client = MongoClient('localhost', 27017)
db = client['Login']
coleccion_usuarios = db['Usuarios']
coleccion_contraseña = db['Contraseña']

# Define todas las entradas lingüísticas y sus valores permitidos
entradas_permitidas = {
    'tipo_de_gato': {'gato_domestico', 'maine_conn'},
    'meses': {'menos_de_5_meses', 'mas_de_6_meses'},
    'peso': {'ligero', 'medio', 'pesado'},
    'temperatura': {'frio', 'templado', 'caliente'},
    'desparacitacion': {'reciente', 'medio', 'nunca'}
}

# Definir un diccionario para mapear las entradas lingüísticas a valores numéricos
mapeo_tipo_de_gato = {'gato_domestico': 0, 'maine_conn': 1}
mapeo_meses = {'menos_de_5_meses': 0, 'mas_de_6_meses': 1}
mapeo_peso = {'ligero': 0, 'medio': 1, 'pesado': 2}
mapeo_temperatura = {'frio': 35, 'templado': 37.5, 'caliente': 40}
mapeo_desparacitacion = {'reciente': 0, 'medio': 1, 'nunca': 2}


# Definición de las variables de entrada
tipo_de_gato = ctrl.Antecedent(np.arange(0, 2.1, 1), 'tipo_de_gato')
meses = ctrl.Antecedent(np.arange(0, 2.1, 1), 'meses')
peso = ctrl.Antecedent(np.arange(0, 3.1, 1), 'peso')
temperatura = ctrl.Antecedent(np.arange(35, 41, 1), 'temperatura')
desparacitacion = ctrl.Antecedent(np.arange(0, 3.1, 1), 'desparacitacion')

# Definición de la variable de salida
salida = ctrl.Consequent(np.arange(0, 11, 1), 'salida')

# Funciones de membresía para las variables de entrada y salida
tipo_de_gato.automf(3, names=['gato_domestico', 'maine_conn'])
meses.automf(3, names=['menos_de_5_meses', 'mas_de_6_meses'])
peso.automf(3, names=['ligero', 'medio', 'pesado'])
temperatura.automf(3, names=['frio', 'templado', 'caliente'])
desparacitacion.automf(3, names=['reciente', 'medio', 'nunca'])

# Funciones de membresía para la variable de salida
salida['alta_temperatura'] = fuzz.trimf(salida.universe, [7, 9, 10])
salida['gato_sano'] = fuzz.trimf(salida.universe, [0, 0, 3])
salida['gato_obeso'] = fuzz.trimf(salida.universe, [6, 9, 10])
salida['gato_desnutrido'] = fuzz.trimf(salida.universe, [4, 7, 10])
salida['gato_necesita_desparacitar'] = fuzz.trimf(salida.universe, [6, 8, 10])
salida['gato_muy_enfermo'] = fuzz.trimf(salida.universe, [5, 8, 10])
salida['gato_muy_frio'] = fuzz.trimf(salida.universe, [0, 2, 5])
salida['gato_saludable'] = fuzz.trimf(salida.universe, [0, 3, 6])

# Reglas difusas
rule1 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['mas_de_6_meses'] & peso['medio'] & temperatura['caliente'] & desparacitacion['reciente'], salida['alta_temperatura'])
rule2 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['menos_de_5_meses'] & peso['medio'] & temperatura['templado'] & desparacitacion['reciente'], salida['gato_sano'])
rule3 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['mas_de_6_meses'] & peso['pesado'] & temperatura['templado'] & desparacitacion['medio'], salida['gato_obeso'])
rule4 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['mas_de_6_meses'] & peso['medio'] & temperatura['frio'] & desparacitacion['medio'], salida['gato_muy_frio'])
rule5 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['menos_de_5_meses'] & peso['medio'] & temperatura['templado'] & desparacitacion['nunca'], salida['gato_necesita_desparacitar'])
rule6 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['mas_de_6_meses'] & peso['pesado'] & temperatura['caliente'] & desparacitacion['nunca'], salida['alta_temperatura'])
rule7 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses ['mas_de_6_meses'] & peso['pesado'] & temperatura['caliente'] & desparacitacion['reciente'], salida['alta_temperatura'])
rule8 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['menos_de_5_meses'] & peso['ligero'] & temperatura['caliente'] & desparacitacion['medio'], salida['alta_temperatura'])
rule9 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['menos_de_5_meses'] & peso['ligero'] & temperatura['frio'] & desparacitacion['reciente'], salida['gato_muy_frio'])
rule10 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['menos_de_5_meses'] & peso['ligero'] & temperatura['templado'] & desparacitacion['medio'], salida['gato_desnutrido'])
rule11 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['mas_de_6_meses'] & peso['ligero'] & temperatura['caliente'] & desparacitacion['nunca'], salida['gato_muy_enfermo'])
rule12 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['mas_de_6_meses'] & peso['ligero'] & temperatura['caliente'] & desparacitacion['nunca'], salida['alta_temperatura'])
rule13 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['mas_de_6_meses'] & peso['pesado'] & temperatura['frio'] & desparacitacion['reciente'], salida['gato_muy_frio'])
rule14 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['mas_de_6_meses'] & peso['pesado'] & temperatura['templado'] & desparacitacion['reciente'], salida['gato_obeso'])
rule15 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['mas_de_6_meses'] & peso['ligero'] & temperatura['frio'] & desparacitacion['nunca'], salida['gato_muy_frio'])
rule16 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['menos_de_5_meses'] & peso['ligero'] & temperatura['templado'] & desparacitacion['medio'], salida['gato_desnutrido'])
rule17 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['mas_de_6_meses'] & peso['pesado'] & temperatura['frio'] & desparacitacion['reciente'], salida['gato_muy_frio'])
rule18 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['mas_de_6_meses'] & peso['pesado'] & temperatura['templado'] & desparacitacion['reciente'], salida['gato_obeso'])
rule19 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['mas_de_6_meses'] & peso['pesado'] & temperatura['caliente'] & desparacitacion['nunca'], salida['alta_temperatura'])
rule20 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['menos_de_5_meses'] & peso['pesado'] & temperatura['caliente'] & desparacitacion['nunca'], salida['alta_temperatura'])
rule21 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['menos_de_5_meses'] & peso['pesado'] & temperatura['caliente'] & desparacitacion['nunca'], salida['alta_temperatura'])
rule22 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['menos_de_5_meses'] & peso['medio'] & temperatura['frio'] & desparacitacion['reciente'], salida['gato_muy_frio'])
rule23 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['menos_de_5_meses'] & peso['medio'] & temperatura['templado'] & desparacitacion['nunca'], salida['gato_necesita_desparacitar'])
rule24 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['mas_de_6_meses'] & peso['medio'] & temperatura['caliente'] & desparacitacion['medio'], salida['alta_temperatura'])
rule25 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['mas_de_6_meses'] & peso['medio'] & temperatura['frio'] & desparacitacion['nunca'], salida['gato_muy_frio'])
rule26 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['menos_de_5_meses'] & peso['ligero'] & temperatura['caliente'] & desparacitacion['reciente'], salida['alta_temperatura'])
rule27 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['mas_de_6_meses'] & peso['medio'] & temperatura['templado'] & desparacitacion['medio'], salida['gato_saludable'])
rule28 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['menos_de_5_meses'] & peso['medio'] & temperatura['templado'] & desparacitacion['reciente'], salida['gato_sano'])
rule29 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['menos_de_5_meses'] & peso['ligero'] & temperatura['templado'] & desparacitacion['reciente'], salida['gato_desnutrido'])
rule30 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['mas_de_6_meses'] & peso['pesado'] & temperatura['caliente'] & desparacitacion['reciente'], salida['alta_temperatura'])
rule31 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['menos_de_5_meses'] & peso['pesado'] & temperatura['frio'] & desparacitacion['reciente'], salida['gato_muy_frio'])
rule32 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['menos_de_5_meses'] & peso['ligero'] & temperatura['frio'] & desparacitacion['medio'], salida['gato_muy_frio'])
rule33 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['menos_de_5_meses'] & peso['medio'] & temperatura['caliente'] & desparacitacion['medio'], salida['alta_temperatura'])
rule34 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['menos_de_5_meses'] & peso['pesado'] & temperatura['templado'] & desparacitacion['medio'], salida['gato_obeso'])
rule35 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['mas_de_6_meses'] & peso['ligero'] & temperatura['templado'] & desparacitacion['medio'], salida['gato_saludable'])
rule36 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['mas_de_6_meses'] & peso['medio'] & temperatura['templado'] & desparacitacion['medio'], salida['gato_saludable'])
rule37 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['mas_de_6_meses'] & peso['medio'] & temperatura['caliente'] & desparacitacion['medio'], salida['alta_temperatura'])
rule38 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['menos_de_5_meses'] & peso['ligero'] & temperatura['caliente'] & desparacitacion['medio'], salida['alta_temperatura'])
rule39 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['menos_de_5_meses'] & peso['medio'] & temperatura['frio'] & desparacitacion['medio'], salida['gato_muy_frio'])
rule40 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['menos_de_5_meses'] & peso['ligero'] & temperatura['templado'] & desparacitacion['reciente'], salida['gato_desnutrido'])
rule41 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['menos_de_5_meses'] & peso['medio'] & temperatura['templado'] & desparacitacion['medio'], salida['gato_sano'])
rule42 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['mas_de_6_meses'] & peso['medio'] & temperatura['templado'] & desparacitacion['reciente'], salida['gato_saludable'])
rule43 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['mas_de_6_meses'] & peso['medio'] & temperatura['frio'] & desparacitacion['medio'], salida['gato_muy_frio'])
rule44 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['menos_de_5_meses'] & peso['pesado'] & temperatura['templado'] & desparacitacion['nunca'], salida['gato_necesita_desparacitar'])
rule45 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['menos_de_5_meses'] & peso['pesado'] & temperatura['frio'] & desparacitacion['medio'], salida['gato_muy_frio'])
rule46 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['menos_de_5_meses'] & peso['medio'] & temperatura['frio'] & desparacitacion['nunca'], salida['gato_muy_frio'])
rule47 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['mas_de_6_meses'] & peso['pesado'] & temperatura['templado'] & desparacitacion['nunca'], salida['gato_obeso'])
rule48 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['menos_de_5_meses'] & peso['medio'] & temperatura['templado'] & desparacitacion['medio'], salida['gato_sano'])
rule49 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['mas_de_6_meses'] & peso['ligero'] & temperatura['templado'] & desparacitacion['reciente'], salida['gato_saludable'])
rule50 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['mas_de_6_meses'] & peso['ligero'] & temperatura['frio'] & desparacitacion['reciente'], salida['gato_muy_frio'])
rule51 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['mas_de_6_meses'] & peso['medio'] & temperatura['caliente'] & desparacitacion['nunca'], salida['alta_temperatura'])
rule52 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['menos_de_5_meses'] & peso['pesado'] & temperatura['templado'] & desparacitacion['medio'], salida['gato_obeso'])
rule53 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['menos_de_5_meses'] & peso['ligero'] & temperatura['frio'] & desparacitacion['reciente'], salida['gato_muy_frio'])
rule54 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['mas_de_6_meses'] & peso['ligero'] & temperatura['templado'] & desparacitacion['reciente'], salida['gato_saludable'])
rule55 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['menos_de_5_meses'] & peso['pesado'] & temperatura['frio'] & desparacitacion['nunca'], salida['gato_muy_frio'])
rule56 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['menos_de_5_meses'] & peso['pesado'] & temperatura['caliente'] & desparacitacion['medio'], salida['alta_temperatura'])
rule57 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['mas_de_6_meses'] & peso['ligero'] & temperatura['frio'] & desparacitacion['medio'], salida['gato_muy_frio'])
rule58 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['menos_de_5_meses'] & peso['medio'] & temperatura['caliente'] & desparacitacion['reciente'], salida['alta_temperatura'])
rule59 = ctrl.Rule(tipo_de_gato['maine_conn'] & meses['menos_de_5_meses'] & peso['ligero'] & temperatura['templado'] & desparacitacion['nunca'], salida['gato_desnutrido'])
rule60 = ctrl.Rule(tipo_de_gato['gato_domestico'] & meses['mas_de_6_meses'] & peso['pesado'] & temperatura['templado'] & desparacitacion['medio'], salida['gato_obeso'])


# Creación del sistema de control difuso
sistema_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20, rule21, rule22,rule23,rule24,rule25,rule26,rule27,rule28,rule29,rule30,rule31,rule32,rule33,rule34,rule35,rule36,rule37,rule38,rule39,rule40,rule41,rule42,rule43,rule44,rule45,rule46,rule47,rule48,rule49,rule50,rule51,rule52,rule53,rule54,rule55,rule56,rule57,rule58,rule59,rule60])

app = Flask(__name__)

@app.route('/')
def iniciar():
    return render_template('iniciar.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        
        # Buscar el usuario en la colección de usuarios
        usuario_encontrado = coleccion_usuarios.find_one({'usuario': usuario})
        
        if usuario_encontrado:
            # Verificar la contraseña correspondiente al usuario encontrado
            if contraseña == usuario_encontrado['contraseña']:
                # Redirigir al usuario a la página frente.html después del inicio de sesión exitoso
                return redirect(url_for('frente'))
            else:
                return redirect(url_for('Incorrecta'))
        else:
            return redirect(url_for('NoEncontrado'))


@app.route('/Registrar')
def Registrar():
    return render_template('Registrar.html')

@app.route('/Incorrecta')
def Incorrecta():
    return render_template('Incorrecta.html')

@app.route('/NoEncontrado')
def NoEncontrado():
    return render_template('NoEncontrado.html')

@app.route('/registro', methods=['POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        
        # Verificar si el usuario ya existe en la colección de usuarios
        if coleccion_usuarios.find_one({'usuario': usuario}):
            return redirect(url_for('Exis'))
        
        # Insertar el nuevo usuario en la colección de usuarios
        coleccion_usuarios.insert_one({'usuario': usuario, 'contraseña': contraseña})
        
        return redirect(url_for('Exitoso'))
    
@app.route('/Exitoso')
def Exitoso():
    return render_template('Exitoso.html')

@app.route('/Exis')
def Exis():
    return render_template('Exis.html')

@app.route('/frente')
def frente():
    return render_template('frente.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/resultado', methods=['POST'])
def resultado():
    salida_gato = ctrl.ControlSystemSimulation(sistema_ctrl)

    # Obtener todas las entradas del formulario
    entradas = {key: request.form[key] for key in entradas_permitidas.keys()}

    # Verificar si todas las entradas están dentro del rango definido por las funciones de membresía
    entradas_validas = all(valor in entradas_permitidas[entrada] for entrada, valor in entradas.items())
    if not entradas_validas:
        print("Error: Al menos una entrada contiene un valor no válido.")
        return "Error: Al menos una entrada contiene un valor no válido."

    # Asignar los valores numéricos a las entradas del sistema
    valores_entradas = {entrada: mapeo.get(entradas[entrada], 0) for entrada, mapeo in zip(entradas_permitidas.keys(), [mapeo_tipo_de_gato, mapeo_meses, mapeo_peso, mapeo_temperatura, mapeo_desparacitacion])}

    for entrada, valor in valores_entradas.items():
        salida_gato.input[entrada] = valor

    print("Valores de entrada asignados:")
    print(valores_entradas)

    # Se computa el resultado
    salida_gato.compute()

    # Obtener el valor numérico devuelto por el sistema difuso y redondearlo
    valor_resultado = round(salida_gato.output['salida'], 2)
    print("Valor del resultado:", valor_resultado)

    # Descripciones de los valores numéricos
    descripciones = {
    1: 'Buena tu gato está sano.',
    2: 'Mala tu gato tiene la temperatura baja',
    5: 'Mala tiene sobre peso.',
    6: 'Mala tu gato esta desnutrido..',
    7: 'Mala tu gato esta muy enfermo y necesita desparacitarse',
    8: 'Mala tu gato tiene alta temperatura',


        # Agrega más descripciones según sea necesario
    }

    # Obtener la descripción correspondiente al valor numérico calculado
    descripcion_resultado = descripciones.get(int(valor_resultado), 'No se puede determinar el estado del gato.')
    print("Descripción del resultado:", descripcion_resultado)

    # Renderizar la plantilla HTML con el resultado y su descripción
    return render_template('resultado.html', resultado=valor_resultado, descripcion=descripcion_resultado)




if __name__ == '__main__':
    app.run(debug=True)
