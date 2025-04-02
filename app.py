from flask import Flask, request, jsonify
from flask_cors import CORS
import requests  

app = Flask(__name__)
CORS(app) 
OSRM_URL = "http://router.project-osrm.org/route/v1/driving"
city_coordinates = {
    'Delhi': [77.1025, 28.7041],
    'Mumbai': [72.8777, 19.0760],
    'Jaipur': [75.7873, 26.9124],
    'Chennai': [80.2707, 13.0827],
    'Bangalore': [77.5946, 12.9716],
    'Ahmedabad': [72.5714, 23.0225],
    'Kolkata': [88.3639, 22.5726],
    'Hyderabad': [78.4867, 17.3850],
    'Lucknow': [80.9462, 26.8467],
    'Bhopal': [77.4126, 23.2599],
    'Patna': [85.1376, 25.5941],
    'Chandigarh': [76.7794, 30.7333],
    'Thiruvananthapuram': [76.9366, 8.5241],
    'Guwahati': [91.7362, 26.1445],
    'Ranchi': [85.3096, 23.3441],
    'Panaji': [73.8278, 15.4909],
    'Dehradun': [78.0322, 30.3165],
    'Aizawl': [92.7146, 23.7367],
    'Kohima': [94.1100, 25.6747],
    'Imphal': [93.9368, 24.8170],
    'Itanagar': [93.6053, 27.0844],
    'Agartala': [91.2868, 23.8315],
    'Shillong': [91.8832, 25.5788],
    'Gangtok': [88.6122, 27.3314],
    'Shimla': [77.1734, 31.1048],
    'Panchkula': [76.8606, 30.6942], 
    'Amritsar': [74.8723, 31.6340]
}
@app.route('/shortest-path', methods=['GET'])
def shortest_path():
    start = request.args.get('start')
    end = request.args.get('end')

    if not start or not end:
        return jsonify({"error": "Start and end locations are required"}), 400

    if start not in city_coordinates or end not in city_coordinates:
        return jsonify({"error": "Invalid start or end location"}), 400

    start_coords = city_coordinates[start]
    end_coords = city_coordinates[end]

    route_url = f"{OSRM_URL}/{start_coords[0]},{start_coords[1]};{end_coords[0]},{end_coords[1]}?overview=full&geometries=geojson"
    response = requests.get(route_url)
    data = response.json()

    if 'routes' not in data or not data['routes']:
        return jsonify({"error": "No route found"}), 404

    route_geometry = data['routes'][0]['geometry']['coordinates']
    
    return jsonify({"route": route_geometry})

if __name__ == '__main__':
    app.run(debug=True)
