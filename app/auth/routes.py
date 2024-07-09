from flask import request, jsonify
from .models import User
from .schemas import users_schema
from app.extensions import db, jwt
from flask_jwt_extended import create_access_token, jwt_required
from . import auth_bp

@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    name = request.form['name']
    email = request.form['email']
    mobile = request.form['mobile']

    user = User(username=username, password=password, name=name, email=email, mobile=mobile)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = create_access_token(identity=user.id)
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401


@auth_bp.route('/allusers',methods=['GET'])
@jwt_required()
def getting_all_users():
        users = User.query.all()
        return jsonify(users_schema.dump(users))

# BLOW CODE IS DOING SAME AS KNOW WITH (users_schema.dump(users)) THIS PIEACE OF CODE 
        # output = []
        # for user in users:
        #     user_data = {}
        #     user_data['id'] = user.id
        #     user_data['name'] = user.name
        #     user_data['email'] = user.email
        #     user_data['mobile'] = user.mobile
        #     output.append(user_data)
        # return jsonify({'users': output}),200



@auth_bp.route('/update/<int:id>',methods=['PUT','PATCH'])
@jwt_required()
def user_patch_update(id):
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.form

        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.mobile = data.get('mobile', user.mobile)
        user.password = data.get('password', user.password)

        # if 'name' in data:
        #     user.name = data['name']
        # if 'email' in data:
        #     user.email = data['email']
        # if 'password' in data:
        #     user.password = data['password']
        # if 'mobile' in data:
        #     user.mobile = data['mobile']

        db.session.commit()

        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "mobile": user.mobile,
        })


@auth_bp.route('/delete/<int:id>',methods=['delete'])
@jwt_required()
def user_delete_model(id):
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()
        return f'user {id=} is deleted'


