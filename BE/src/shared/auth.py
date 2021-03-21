import jwt
import os
import datetime
from functools import wraps
from flask import json, Response, request, g
from ..models.UserModel import UserModel


class Auth():
    """
    Auth Class
    """
    @staticmethod
    def generate_token(user_id):
        """
        Generate Token Method
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                os.getenv('JWT_SECRET_KEY'),
                'HS256'
            ).decode("utf-8")
        except Exception as e:
            return Response(
                mimetype="application/json",
                response=json.dumps(
                    {'error': 'error in generating user token'}),
                status=400
            )

    @staticmethod
    def decode_token(token):
        """
        Decode token method
        """
        re = {'data': {}, 'error': {}}
        try:
            payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'))
            re['data'] = {'user_id': payload['sub']}
            return re
        except jwt.ExpiredSignatureError as e1:
            re['error'] = {'message': 'token expired, please login again'}
            return re
        except jwt.InvalidTokenError:
            re['error'] = {
                'message': 'Invalid token, please try again with a new token'}
            return re

    @staticmethod
    def auth_req(func):
        # function for checking if user has auth to access routes
        @wraps(func)
        def decorated_auth(*args, **kwargs):
            # if headers don't contain api_token, error
            if 'api_token' not in request.headers:
                return Response(
                    mimetype="application/json",
                    response=json.dumps(
                        {'error': 'Auth Token not present, please login'}),
                    status=401
                )
            token = request.headers.get('api_token')
            data = Auth.decode_token(token)
            # if token decoding returns an error, that token is no longer valid
            if data['error']:
                return Response(
                    mimetype="application/json",
                    response=json.dumps(data['error']),
                    status=400
                )
            user_id = data['data']['user_id']
            check_user = UserModel.get_user_by_id(user_id)
            # if no user is returned, then there is no user
            if not check_user:
                return Response(
                    mimetype="application/json",
                    response=json.dumps({'error': 'User does not exist'}),
                    status=400
                )
            g.user = {'id': user_id}
            return func(*args, **kwargs)
        return decorated_auth
