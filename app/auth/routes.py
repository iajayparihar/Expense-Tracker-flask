from flask import request, jsonify
from .models import User
from app.extensions import db, jwt
from flask_jwt_extended import create_access_token
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
def getting_all_users():
        users = User.query.all()
        output = []
        for user in users:
            user_data = {}
            user_data['id'] = user.id
            user_data['name'] = user.name
            user_data['email'] = user.email
            user_data['mobile'] = user.mobile
            # user_data['password'] =  user.password
            output.append(user_data)
        return jsonify({'users': output}),200


@auth_bp.route('/update/<int:id>',methods=['put'])
def user_update_model(id):
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        mobile = request.form['mobile']
        if name and email and password and mobile:
            user.name = name
            user.email = email
            user.password =  password
            user.mobile = mobile
            db.session.commit()
            return f'user {id=} is updated'
        else:
            return jsonify({'msg':'Please fill all the fields'}),400

@auth_bp.route('/update/<int:id>',methods=['patch'])
def user_patch_update(id):
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.form

        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.password = data['password']
        if 'mobile' in data:
            user.mobile = data['mobile']

        db.session.commit()

        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "mobile": user.mobile,
        })


@auth_bp.route('/delete/<int:id>',methods=['delete'])
def user_delete_model(id):
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()
        return f'user {id=} is deleted'


