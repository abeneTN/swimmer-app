from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt, unset_jwt_cookies
from werkzeug.security import generate_password_hash, check_password_hash
from championship.process_html_files import process_html
from db.setup import connect, get_user_by_email, insert_user, insert_club

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['JWT_SECRET_KEY'] = 'mysecretkey'  # Change this!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # Set token expiration to 1 hour
jwt = JWTManager(app)

@app.route('/register', methods=['POST'])
@cross_origin()
def register():
    if not request.json:
        return jsonify({"msg": "Invalid JSON data"}), 400

    email = request.json.get('email')
    password = request.json.get('password')
    
    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400
    
    conn = connect()
    if conn is None:
        return jsonify({"msg": "Database connection error"}), 500
    
    existing_user = get_user_by_email(conn, email)
    if existing_user:
        conn.close()
        return jsonify({"msg": "Email already registered"}), 400
    
    password_hash = generate_password_hash(password)
    user_id = insert_user(conn, email, password_hash)
    conn.close()
    
    if user_id:
        return jsonify({"msg": "User registered successfully", "user_id": user_id}), 201
    else:
        return jsonify({"msg": "Registration failed"}), 500

@app.route('/create_club', methods=['POST'])
@jwt_required()
@cross_origin()
def create_club():
    current_user = get_jwt_identity()
    if not request.json:
        return jsonify({"msg": "Invalid JSON data"}), 400
    
    club_name = request.json.get('club_name')
    city = request.json.get('city')

    if not club_name:
        return jsonify({"msg": "Missing club name"}), 400

    conn = connect()
    if conn is None:
        return jsonify({"msg": "Database connection error"}), 500

    user = get_user_by_email(conn, current_user)
    if not user:
        conn.close()
        return jsonify({"msg": "User not found"}), 404

    club_id = insert_club(conn, club_name, city, user[0])
    conn.close()

    if club_id:
        return jsonify({"msg": "Club created successfully", "club_id": club_id}), 201
    else:
        return jsonify({"msg": "Failed to create club"}), 500

@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    if not request.json:
        return jsonify({"msg": "Invalid JSON data"}), 400

    email = request.json.get('email')
    password = request.json.get('password')
    
    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400
    
    conn = connect()
    if conn is None:
        return jsonify({"msg": "Database connection error"}), 500
    
    user = get_user_by_email(conn, email)
    conn.close()
    
    if user and check_password_hash(user[2], password):
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token)
    else:
        return jsonify({"msg": "Bad email or password"}), 401

@app.route('/upload', methods=['POST'])
@jwt_required()
@cross_origin()
def upload_files():
    current_user = get_jwt_identity()
    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No files uploaded!"}), 400
    
    ranks = process_html(files)
    return jsonify({"ranks": ranks, "user": current_user})

@app.route('/logout', methods=['POST'])
@jwt_required(optional=True)
@cross_origin()
def logout():
    response = jsonify({"msg": "Successfully logged out"})
    unset_jwt_cookies(response)
    return response, 200

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/delete_user', methods=['DELETE'])
@jwt_required()
@cross_origin()
def delete_user():
    current_user = get_jwt_identity()
    print("current_user", current_user)
    
    conn = connect()
    if conn is None:
        return jsonify({"msg": "Database connection error"}), 500
    
    try:
        cur = conn.cursor()
        
        # First, delete the user's club if they own one
        cur.execute("DELETE FROM clubs WHERE owner_id = (SELECT id FROM users WHERE email = %s)", (current_user,))
        
        # Then, delete the user
        cur.execute("DELETE FROM users WHERE email = %s", (current_user,))
        
        if cur.rowcount == 0:
            conn.rollback()
            return jsonify({"msg": "User not found"}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        
        # Revoke the user's JWT token
        jti = get_jwt()['jti']
        revoke_token(jti)
        
        return jsonify({"msg": "User account deleted successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"msg": f"An error occurred: {str(e)}"}), 500
    finally:
        if conn:
            conn.close()

def revoke_token(jti):
    # In a production environment, you would typically store revoked tokens
    # in a fast database like Redis. For simplicity, we're using a set here.
    # This set will be cleared when the server restarts.
    # Use a global variable for revoked tokens instead of attaching it to the app object
    global revoked_tokens
    if 'revoked_tokens' not in globals():
        revoked_tokens = set()
    revoked_tokens.add(jti)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    global revoked_tokens
    return jti in revoked_tokens if 'revoked_tokens' in globals() else False