# DASH
VOST Portugal Internal Dashboard project
## Objectives 

The dashboard aims to aggregate information coming from official datasources, via the API created by [@tomahock](https://github.com/tomahock)
- The dashboard has an operation / current events monitoring funcion 
- The dashboard has an historical comparasion with current events function 
- The dashboard presents information in *real time*
- The dashboard allows for the user to filter data by type, date and date range, district, council, parish 
- The dashboard should also have an operstional map running with mapbox 

## Requirements 
### Run locally with docker
- `docker build -t dash:latest .`
- `docker run -p 8052:8052 dash`

# DESCRIPTIONS 

## app.py 
<img width="1792" alt="apppy" src="https://user-images.githubusercontent.com/34355337/123448393-c501a580-d5d2-11eb-9f4d-8148b8c2fcf6.png">

This dashboard makes a JSON request to `fogos.pt` API (by [@tomahock](https://github.com/tomahock) ) and renders four different graphs and a table with the last 10 events. 

The dashboard updates every minute 
