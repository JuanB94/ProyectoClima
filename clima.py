from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Configuración inicial
API_KEY = '63930c33610897dca594df84d0daae4d'  # Reemplaza con tu clave de API
iconos_clima = {
    "clear sky": "☀️", "few clouds": "🌤️", "scattered clouds": "⛅",
    "broken clouds": "🌥️", "shower rain": "🌦️", "rain": "🌧️",
    "thunderstorm": "⛈️", "snow": "❄️", "mist": "🌫️", "overcast clouds": "☁️"
}

def obtener_clima(ciudad):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}&units=metric&lang=es'
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        datos_clima = respuesta.json()

        # Extracción de datos relevantes
        dia = 'Hoy'  # O puedes personalizar esto si lo deseas
        temperatura = datos_clima['main']['temp']
        humedad = datos_clima['main']['humidity']
        velocidad_viento = datos_clima['wind']['speed']
        descripcion = datos_clima['weather'][0]['description']
        probabilidad_lluvia = datos_clima.get('rain', {}).get('1h', 0)
        icono = iconos_clima.get(descripcion, "🌈")
        latitud = datos_clima['coord']['lat']
        longitud = datos_clima['coord']['lon']

        return {
            "dia": dia,  # Asegúrate de pasar el día
            "temperatura": temperatura,
            "humedad": humedad,
            "velocidad_viento": velocidad_viento,
            "probabilidad_lluvia": probabilidad_lluvia,
            "descripcion": descripcion,
            "icono": icono,
            "latitud": latitud,
            "longitud": longitud
        }
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


@app.route('/', methods=['GET', 'POST'])
def index():
    ciudad = 'Guayaquil, EC'  # Ciudad predeterminada
    clima_datos = {}

    if request.method == 'POST':
        ciudad = request.form['ciudad']
        clima_datos = obtener_clima(ciudad)
    
    return render_template("index.html", clima=clima_datos, ciudad=ciudad)

@app.route('/cv')
def cv():
    return render_template('cv.html')  # retorna la página del cv

if __name__ == '__main__':
    app.run(debug=True)
