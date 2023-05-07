# preciosLUZp

# Calculador de precios medios de la luz horarios de referecnia OMIE por periodos

preciosLUZp es una aplicación basada en Python con una interfaz gráfica de usuario (GUI) que permite descargar y procesar datos de la página web del [Operador del Mercado Ibérico de Energía](https://www.omie.es/es/market-results/daily/daily-market/daily-hourly-price) (OMIE).

La aplicación permite seleccionar un intervalo de fechas y, a continuación, descarga los archivos pertinentes que contienen los precios marginales de la electricidad en el mercado ibérico. Procesa los datos y proporciona los resultados en un formato fácil de usar.

## Características

- Selección de un intervalo de fechas personalizado para la descarga de datos
- Descarga automática de los ficheros relevantes de OMIE
- Procesamiento de los datos descargados, incluyendo precios marginales y días festivos
- Interfaz gráfica de usuario para facilitar la interacción
- Barra de progreso para mostrar el estado de las descargas

## Requisitos

- Python 3.6 o superior
- Se requieren los siguientes paquetes de Python
  - `requests`
  - `pandas`
  - `tkinter`
  - `ttkthemes`
  - `tkcalendar`
  - `tqdm`
  - `babel`

Puede instalar los paquetes necesarios con pip:

```
pip install -r requisitos.txt
```

## Uso

Para ejecutar la aplicación, ejecute el siguiente comando en su terminal o símbolo del sistema:

```
python main.py
```

La aplicación se iniciará con una interfaz gráfica de usuario. Elija las fechas de inicio y fin de los datos que desea descargar y procesar y, a continuación, pulse el botón "Calcular precios €/kWh". Los datos se descargarán y el progreso se mostrará en la barra de progreso.

## Contribuir

Si quieres contribuir a este proyecto, no dudes en enviar un pull request o abrir un issue en GitHub.

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](https://opensource.org/licenses/MIT). Vea el archivo [LICENSE](LICENSE) para más información.


# preciosLUZp

preciosLUZp is a Python-based application with a graphical user interface (GUI) that allows you to download and process data from the [Operador del Mercado Ibérico de Energía](https://www.omie.es/es/market-results/daily/daily-market/daily-hourly-price) (OMIE) website.

The application allows you to select a date range and then downloads the relevant files containing the marginal prices of electricity in the Iberian market. It processes the data and provides the results in a user-friendly format.

## Features

- Select a custom date range for downloading data
- Automatic downloading of relevant files from OMIE
- Processing of downloaded data, including marginal prices and bank holidays
- Graphical user interface for easy interaction
- Progress bar to display the status of downloads

## Requirements

- Python 3.6 or higher
- The following Python packages are required:
  - `requests`
  - `pandas`
  - `tkinter`
  - `ttkthemes`
  - `tkcalendar`
  - `tqdm`
  - `babel`

You can install the required packages using pip:

```
pip install -r requirements.txt
```

## Usage

To run the application, execute the following command in your terminal or command prompt:

```
python main.py
```

The application will launch with a graphical user interface. Choose the start and end dates for the data you want to download and process, then click the "Calcular precios €/kWh" button. The data will be downloaded, and the progress will be displayed in the progress bar.

## Contributing

If you'd like to contribute to this project, feel free to submit a pull request or open an issue on GitHub.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). See the [LICENSE](LICENSE) file for more information.

