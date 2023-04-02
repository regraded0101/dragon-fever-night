# Wine Insights

## Streamlit App with Meteostat API Data

This Streamlit app displays weather data from the Meteostat API to provide insights on wine taste. It allows users to select a wine region and a year to understand the weather during that year. 

Requirements

Python 3.9 or later
Streamlit 1.20.0 or later
PlotLy 5.14.0 or later
Meteostat 1.6.5 or later (to reproduce the dataset)

## Installation
To see the app in product, go the [Streamlit App](https://regraded0101-dragon-fever-night-app-bdkgf2.streamlit.app)


Clone the repository:
Copy code
```bash
git clone https://github.com/regraded0101/dragon-fever-night.git
cd dragon-fever-night
```
Install the required packages:
```bash
pip install -r requirements.txt
```

To start the app, run the following command:

```bash
streamlit run app.py
```
Once the app is running, you can select a location and a year using the dropdown menus. The app will display a time series and metrics of the temperatures vs averages across multiple years, as well as the locations of the weather stations used to collect the data

Contributing

Contributions are welcome! If you'd like to contribute to this project, please open an issue or submit a pull request.

License

This project is licensed under the MIT License. See the LICENSE file for more information.