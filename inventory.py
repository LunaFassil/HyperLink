# Backend code -> add Iteration 1 Functions here

#IMPORTS FOR FLASK
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  #allow frontend JavaScript to make API requests

#temp in memory storage for inventory
inventory = []
next_id = 0

@app.route("/")
def home():
    return render_template("inventory.html")  #flask will use HTML File

@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory)  #return full inventory as JSON


#TO DO: SAVE INVENTORY TO A FILE SO THAT IT DOESnT GO AWAY WHEN REFRESHED 
@app.route("/add", methods=["POST"])
def add_item():
    global next_id
    
    data = request.json

    #make sure all fields filled out or error
    if not data or not all(k in data for k in ("name", "quantity", "price", "color")):
        return jsonify({"error": "Missing required fields"}), 400
    
    #saved data of item assigns id
    item = {
        "id": next_id,
        "name": data["name"],
        "quantity": int(data["quantity"]),
        "price": float(data["price"]),
        "color": data["color"]
    }
    inventory.append(item)#add item to inventory
    next_id += 1 #go to next id so no items have same one
    
    return jsonify({"message": "Item added successfully", "item": item}), 201 #alert item added

# route to handle removing an item from the inventory
@app.route("/remove", methods=["POST"])
def remove_item():
    data = request.json
    if "id" not in data:
        return jsonify({"error": "ID is required"}), 400 # return error if ID is missing

    item_id = data["id"]
    
    # find item in inventory
    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item) # remove the item from the inventory
            return jsonify({"message": f"Item with ID {item_id} removed successfully"}), 200
    # return an error if no matching item was found
    return jsonify({"error": "Item not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)