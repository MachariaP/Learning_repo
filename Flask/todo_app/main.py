from flask import Flask, request, Response
import json
import helper

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/item/new', methods=['POST'])
def add_item():
    req_data = request.get_json()
    item = req_data['item']
    res_data = helper.add_to_list(item)
    if res_data is None:
        response = Response("{'error': 'Item not added - " + item + "'}", status=400, mimetype='application/json')
        return response
    response = Response(json.dumps(res_data), mimetype='application/json')
    return response

@app.route('/items/all')
def get_all_items():
    res_data = helper.get_all_items()
    response = Response(json.dumps(res_data), mimetype='application/json')
    return response

@app.route('/item/status', methods=['GET'])
def get_item():
    item_name = request.args.get('name')
    status = helper.get_item(item_name)
    if status is None:
        response = Response("{'error': 'Item Not Found - %s'}" % item_name, status=404, mimetype='application/json')
        return response
    res_data = {'status': status}
    response = Response(json.dumps(res_data), status=200, mimetype='application/json')
    return response

@app.route('/item/update', methods=['PUT'])
def update_status():
    req_data = request.get_json()
    item = req_data['item']
    status = req_data['status']
    res_data = helper.update_status(item, status)
    if res_data is None:
        response = Response("{'error': 'Error updating item - " + item + ", " + status + "}", status=400, mimetype='application/json')
        return response
    response = Response(json.dumps(res_data), mimetype='application/json')
    return response

@app.route('/item/remove', methods=['DELETE'])
def delete_item():
    req_data = request.get_json()
    item = req_data['item']
    res_data = helper.delete_item(item)
    if res_data is None:
        response = Response("{'error': 'Error deleting item - " + item + "}", status=400, mimetype='application/json')
        return response
    response = Response(json.dumps(res_data), mimetype='application/json')
    return response

if __name__ == '__main__':
    app.run(debug=True)
