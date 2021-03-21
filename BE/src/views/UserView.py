from flask import request, json, Response, Blueprint
from ..models.UserModel import UserModel, UserSchema
from ..shared.auth import Auth

user_api = Blueprint('users', __name__)
user_schema = UserSchema()


@user_api.route('/register', methods=['POST'])
def create_user():
    req_data = request.get_json()
    print(req_data, "REQ")
    data = user_schema.load(req_data)

    print(data, 'DATA HERE')
    # print(error, 'ERR HERE')

    # if error:
    #     return custom_response({error: 'Err here'}, 400)
    # try:
    #     data = user_schema.load(req_data)
    # except ValidationError as err:
    #     print(err.messages)
    #     print(err.valid_data)
    # see if user exists
    user_exists = UserModel.get_user_by_username(data.get('username'))
    if user_exists:
        message = {'error': 'User already exists.'}
        return custom_response(message, 400)
    # if they don't, make em
    user = UserModel(data)
    user.save()

    ser_data = user_schema.dump(user).data
    token = Auth.generate_token(ser_data.get('id'))
    return custom_response({'jwt_token': token}, 201)


@user_api.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()
    data, err = user_schema.load(req_data)

    # if err, return that err, if username or pw in req aren't there, tell them they need those
    if err:
        return custom_response(err, 400)
    if not data.get('username') or not data.get('password'):
        return custom_response({'error': 'You need username and password to login.'}, 400)

    # since this is login, user will have already been created.
    # check to see if the corresponding username is in the db
    # if not, they have invalid creds. If password hash doesn't check out, invalid creds
    user = UserModel.get_user_by_username(data.get('username'))
    if not user:
        return custom_response({'error': 'Invalid Creds.'}, 400)
    if not user.check_hash(data.get('password')):
        return custom_response({'error': 'Invalid Creds.'}, 400)
    ser_data = user_schema.dump(user).data
    token = Auth.generate_token(ser_data.get('id'))

    return custom_response({'jwt_token': token}, 200)


@user_api.route('/', methods=['GET'])
@Auth.auth_req
def get_users():
    users = UserModel.get_all_users()
    ser_users = user_schema.dump(users, many=True).data
    return custom_response(ser_users, 200)


@user_api.route('/<int:user_id>', methods=['GET'])
@Auth.auth_req
def get_user(user_id):
    user = UserModel.get_user_by_id(user_id)

    if not user:
        return custom_response({'error': 'User does not exist.'}, 404)

    ser_user = user_schema.dump(user).data
    return custom_response(ser_user, 200)


@user_api.route('/profile', methods=['PUT'])
@Auth.auth_req
def update_user():
    req_data = request.get_json()
    # partial=true here since they may not be updating all of the info, just some
    data, err = user_schema.load(req_data, partial=True)
    if err:
        return custom_response(err, 400)

    user = UserModel.get_user_by_id(g.user.get('id'))
    user.update(data)
    ser_user = user_schema.dump(user).data
    return custom_response(ser_user, 200)


@user_api.route('/profile', methods=['DELETE'])
@Auth.auth_req
def delete_user():
    user = UserModel.get_user_by_id(g.user.get('id'))
    user.delete()
    return custom_response({'message': 'deleted user'}, 204)


@user_api.route('/profile', methods=['GET'])
@Auth.auth_req
def get_profile():
    user = UserModel.get_user_by_id(g.user.get('id'))
    ser_user = user_schema.dump(user).data

    return custom_response(ser_user, 200)


def custom_response(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
