"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

John = {
    "first_name" : "John ",
    "last_name" : jackson_family.last_name,
    "age" : 33,
    "lucky_numbers" : [7, 13, 22]
}

Jane = {
    "first_name" : "Jane",
    "last_name" : jackson_family.last_name,
    "age" : 35,
    "lucky_numbers" : [10, 14, 3]
}

Jimmy = {
    "first_name" : "Jimmy",
    "last_name" : jackson_family.last_name,
    "age" : 5,
    "lucky_numbers" : [1]
}

jackson_family.add_member(John)
jackson_family.add_member(Jane)
jackson_family.add_member(Jimmy)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#### GET
@app.route('/members',methods=['GET'])
def get_member_list():

    members = jackson_family.get_all_members()
   
    return jsonify(members), 200
    
#### GET 1 MEMBER
@app.route('/member/<int:id>', methods=['GET'])
def get_one_member(id):

    try:
        jackson_family
    except NameError:
        return jsonify({"error" : "Namerror"}), 500

    member = jackson_family.get_member(id)

    if member:
        print("-------------------------------------------------------------",member)
        response_body = {
            "family_member": member
        }
        
        return jsonify({"name":f"{member['first_name']} {member['last_name']}",
                        "age": member['age'],
                        "id" : member['id'],
                        "lucky_numbers": member['lucky_numbers']
                        }), 200
    else:
        return jsonify({"error": "Member not found"}), 404
    

#### POST
@app.route('/member',methods=['POST'])
def create_member():

    new_member = request.json
    jackson_family.add_member(new_member)
    if new_member is not None:
        response_body = {"message": f"Created member: {new_member}"}

        return jsonify(response_body), 200
    else:
        response_body = {"message": "Error creating new member:"}
        return jsonify(response_body), 404


#### DELETE 
@app.route('/member/<int:id>',methods=['DELETE'])
def handle_delete_member(id):

    deleted_member = jackson_family.get_member(id)

    if deleted_member :

        jackson_family.delete_member(id)
        return jsonify({"done": True}), 200
       
    else:
        return jsonify({"message": "Member not found"}), 404
    

#### PUT 
@app.route('/members/<int:id>',methods=['PUT'])
def handle_update_members():

    updated_member_data = request.json
    updated_member = jackson_family.update_member(id,updated_member_data)
    
    if updated_member:
        response_body = {"message": f"Member updated: {updated_member}"}

        return jsonify(response_body), 200
    else:
        response_body = {"message": "Member not found"}
        
        return jsonify(response_body), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
