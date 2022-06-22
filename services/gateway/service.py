import http
from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from dependencies.session import SessionProvider, session_start
import json


class GatewayService:
    name = 'gateway_service'
    file_rpc = RpcProxy('file_service')
    news_rpc = RpcProxy('news_service')
    user_rpc = RpcProxy('user_service')
    session_provider = SessionProvider()

    # user methods

    @http('POST', '/register')
    @session_start
    def register(self, request, session, response):
        request_body = [
            ("username", str),
            ("password", str)
        ]

        response.mimetype = "application/json"
        response.status_code = 400

        try:
            data = json.loads(request.get_data().decode("utf-8"))

        except Exception as e:
            response.set_data(json.dumps(
                {
                    "action": "register",
                    "action_status": "error",
                    "message": "Bad request: invalid data"
                }
            ))
            return response

        for key in request_body:
            if key[0] not in data or data[key[0]] == "" or data[key[0]] == None:
                response.set_data(json.dumps(
                    {
                        "action": "register",
                        "action_status": "error",
                        "message": f"Bad request: missing '{key}' parameter"
                    }
                ))
                return response
            else:
                if not isinstance(data[key[0]], key[1]):
                    response.set_data(json.dumps(
                        {
                            "action": "register",
                            "action_status": "error",
                            "message": f"Bad request: '{key[0]}' parameter is not of type '{key[1]}'"
                        }
                    ))
                    return response

        response.status_code = 200

        if session["username"]:
            response.set_data(json.dumps(
                {
                    "action": "register",
                    "action_status": "success",
                    "register_status": "already_logged_in",
                    "message": "Already logged in, please logout first before registering"
                }
            ))
            return response

        if self.user_rpc.check_username_exist(data["username"]):
            response.set_data(json.dumps(
                {
                    "action": "register",
                    "action_status": "success",
                    "register_status": "username_registered",
                    "message": "Username already registered"
                }
            ))
            return response

        self.user_rpc.register_user(data["username"], data["password"])

        response.status_code = 201
        response.set_data(json.dumps(
            {
                "action": "register",
                "action_status": "success",
                "register_status": "success",
                "username": data["username"],
                "message": "Registration successful"
            }
        ))
        return response

    @http('POST', '/login')
    @session_start
    def login(self, request, session, response):
        request_body = [
            ("username", str),
            ("password", str)
        ]

        response.mimetype = "application/json"
        response.status_code = 400

        try:
            data = json.loads(request.get_data().decode("utf-8"))

        except Exception as e:
            response.set_data(json.dumps(
                {
                    "action": "login",
                    "action_status": "error",
                    "message": "Bad request: invalid data"
                }
            ))
            return response

        for key in request_body:
            if key[0] not in data or data[key[0]] == "" or data[key[0]] == None:
                response.set_data(json.dumps(
                    {
                        "action": "login",
                        "action_status": "error",
                        "message": f"Bad request: missing '{key}' parameter"
                    }
                ))
                return response
            else:
                if not isinstance(data[key[0]], key[1]):
                    response.set_data(json.dumps(
                        {
                            "action": "login",
                            "action_status": "error",
                            "message": f"Bad request: '{key[0]}' parameter is not of type '{key[1]}'"
                        }
                    ))
                    return response

        if data["username"] == None or data["username"] == "" or data["password"] == None or data["password"] == "":
            response.set_data(json.dumps(
                {
                    "action": "login",
                    "action_status": "error",
                    "message": "Bad request: username or password is empty"
                }
            ))
            return response

        response.status_code = 200

        if session["username"]:
            response.set_data(json.dumps(
                {
                    "action": "login",
                    "action_status": "success",
                    "login_status": "already_logged_in",
                    "message": "Already logged in, please logout first before logging back in"
                }
            ))
            return response

        if not self.user_rpc.check_username_exist(data["username"]):
            response.set_data(json.dumps(
                {
                    "action": "login",
                    "action_status": "success",
                    "login_status": "username_not_exist",
                    "message": "Username does not exist"
                }
            ))
            return response

        if not self.user_rpc.check_password_match(data["username"], data["password"]):
            response.set_data(json.dumps(
                {
                    "action": "login",
                    "action_status": "success",
                    "login_status": "password_not_match",
                    "message": "Password does not match"
                }
            ))
            return response

        session["username"] = data["username"]
        response.set_data(json.dumps(
            {
                "action": "login",
                "action_status": "success",
                "login_status": "success",
                "username": data["username"],
                "message": "Login successful"
            }
        ))
        return response

    @http('DELETE', '/logout')
    @session_start
    def logout(self, request, session, response):
        session.destroy()
        response.mimetype = "application/json"
        response.status_code = 200
        response.set_data(json.dumps(
            {
                "action": "logout",
                "action_status": "success",
                "message": "Logged out successfully"
            }
        ))
        return response

    # news methods

    @http('GET', '/news')
    @session_start
    def get_news(self, request, session, response):
        response.mimetype = "application/json"
        response.status_code = 200
        all_news = self.news_rpc.get_all_news()
        response.set_data(json.dumps(
            {
                "action": "get_all_news",
                "action_status": "success",
                "message": "News fetched successfully",
                "news": all_news,
                "count": len(all_news)
            }
        ))
        return response

    @http('GET', '/news/<int:news_id>')
    @session_start
    def get_news_by_id(self, request, session, response, news_id):
        response.mimetype = "application/json"
        response.status_code = 400

        if news_id is None:
            response.set_data(json.dumps(
                {
                    "action": "get_news_by_id",
                    "action_status": "error",
                    "message": f"Bad request: missing news_id parameter"
                }
            ))
            return response

        response.status_code = 404

        if not self.news_rpc.check_news_id_exist(news_id):
            response.set_data(json.dumps(
                {
                    "action": "get_news_by_id",
                    "action_status": "error",
                    "message": "News id does not exist"
                }
            ))
            return response

        response.status_code = 200
        response.set_data(json.dumps(
            {
                "action": "get_news_by_id",
                "action_status": "success",
                "message": "News fetched successfully",
                "news": self.news_rpc.get_news_by_id(news_id)[0]
            }
        ))

        return response

    @http('POST', '/news/post')
    @session_start
    def post_news(self, request, session, response):
        request_body = [
            ("title", str),
            ("content", str),
            ("datetime", str),
            ("files", list)
        ]

        request_body_files = [
            ("file_name", str),
            ("base64_data", str)
        ]

        response.mimetype = "application/json"

        if not session["username"]:
            response.status_code = 401
            response.set_data(json.dumps(
                {
                    "action": "post_new_news",
                    "action_status": "error",
                    "message": "Unauthorized: please login first"
                }
            ))
            return response

        response.status_code = 400

        try:
            data = json.loads(request.get_data().decode("utf-8"))

        except Exception as e:
            response.set_data(json.dumps(
                {
                    "action": "post_new_news",
                    "action_status": "error",
                    "message": "Bad request: invalid data"
                }
            ))
            return response

        for key in request_body:
            if key[0] not in data or data[key[0]] == "" or data[key[0]] == None:
                response.set_data(json.dumps(
                    {
                        "action": "post_new_news",
                        "action_status": "error",
                        "message": f"Bad request: missing '{key}' parameter"
                    }
                ))
                return response
            else:
                if not isinstance(data[key[0]], key[1]):
                    response.set_data(json.dumps(
                        {
                            "action": "post_new_news",
                            "action_status": "error",
                            "message": f"Bad request: '{key[0]}' parameter is not of type '{key[1]}'"
                        }
                    ))
                    return response

        for idx, file_body in enumerate(data["files"]):
            for key in request_body_files:
                if key[0] not in file_body:
                    response.set_data(json.dumps(
                        {
                            "action": "post_new_news",
                            "action_status": "error",
                            "message": f"Bad request: missing '{key}' parameter at file index {idx}"
                        }
                    ))
                    return response
                else:
                    if not isinstance(file_body[key[0]], key[1]):
                        response.set_data(json.dumps(
                            {
                                "action": "post_new_news",
                                "action_status": "error",
                                "message": f"Bad request: '{key[0]}' parameter is not of type '{key[1]}' at file index {idx}"
                            }
                        ))
                        return response

        new_news_id = self.news_rpc.post_news(data["title"], data["content"], data["datetime"], session["username"])

        self.file_rpc.post_files(new_news_id, data["files"])

        response.status_code = 201
        response.set_data(json.dumps(
            {
                "action": "post_new_news",
                "action_status": "success",
                "message": "News posted successfully",
                "news_id": new_news_id
            }
        ))

        return response

    @http('PUT', '/news/<int:news_id>')
    @session_start
    def edit_news(self, request, session, response, news_id):
        request_body = [
            ("title", str),
            ("content", str),
            ("datetime", str),
            ("files", list)
        ]

        request_body_dict = {
            "title": str,
            "content": str,
            "datetime": str,
            "files": list
        }

        request_body_set = set([x[0] for x in request_body])

        request_body_files = [
            ("file_name", str),
            ("base64_data", str)
        ]

        request_body_files_set = set([x[0] for x in request_body_files])

        response.mimetype = "application/json"

        if not session["username"]:
            response.status_code = 401
            response.set_data(json.dumps(
                {
                    "action": "edit_news",
                    "action_status": "error",
                    "message": "Unauthorized: please login first"
                }
            ))
            return response

        response.status_code = 400

        try:
            data = json.loads(request.get_data().decode("utf-8"))

        except Exception as e:
            response.set_data(json.dumps(
                {
                    "action": "edit_news",
                    "action_status": "error",
                    "message": "Bad request: invalid data"
                }
            ))
            return response

        unknown_keys = set(data.keys()) - request_body_set
        if len(unknown_keys) > 0:
            response.set_data(json.dumps(
                {
                    "action": "edit_news",
                    "action_status": "error",
                    "message": f"Bad request: unknown parameters: {', '.join(list(unknown_keys))}"
                }
            ))
            return response

        for key in data.keys():
            if not isinstance(data[key], request_body_dict[key]):
                response.set_data(json.dumps(
                    {
                        "action": "edit_news",
                        "action_status": "error",
                        "message": f"Bad request: '{key}' parameter is not of type '{request_body_dict[key]}'"
                    }
                ))
                return response

            if data[key] == "" or data[key] == None:
                response.set_data(json.dumps(
                    {
                        "action": "edit_news",
                        "action_status": "error",
                        "message": f"Bad request: '{key}' parameter cannot be empty'"
                    }
                ))
                return response

        if "files" in data.keys():
            for idx, file_body in enumerate(data["files"]):
                unknown_keys_files = set(file_body.keys()) - request_body_files_set
                if len(unknown_keys_files) > 0:
                    response.set_data(json.dumps(
                        {
                            "action": "edit_news",
                            "action_status": "error",
                            "message": f"Bad request: unknown parameters: {', '.join(list(unknown_keys_files))} at file index {idx}"
                        }
                    ))

                    return response

                for key in request_body_files:
                    if key[0] not in file_body:
                        response.set_data(json.dumps(
                            {
                                "action": "edit_news",
                                "action_status": "error",
                                "message": f"Bad request: missing '{key}' parameter at file index {idx}"
                            }
                        ))
                        return response
                    else:
                        if not isinstance(file_body[key[0]], key[1]):
                            response.set_data(json.dumps(
                                {
                                    "action": "edit_news",
                                    "action_status": "error",
                                    "message": f"Bad request: '{key[0]}' parameter is not of type '{key[1]}' at file index {idx}"
                                }
                            ))
                            return response

        if not self.news_rpc.check_news_id_exist(news_id):
            response.status_code = 404
            response.set_data(json.dumps(
                {
                    "action": "edit_news",
                    "action_status": "error",
                    "message": "News id does not exist"
                }
            ))
            return response

        news_data = self.news_rpc.get_news_by_id(news_id)[0]
        response.status_code = 403

        if news_data["publisher"] != session["username"]:
            response.set_data(json.dumps(
                {
                    "action": "edit_news",
                    "action_status": "error",
                    "message": "Forbidden: you are not the publisher of this news"
                }
            ))
            return response

        response.status_code = 200

        self.news_rpc.edit_news(news_id, data.get("title", None), data.get("content", None), data.get("datetime", None))

        if "files" in data.keys():
            self.file_rpc.edit_files(news_id, data["files"])

        response.set_data(json.dumps(
            {
                "action": "edit_news",
                "action_status": "success",
                "message": "News edited successfully"
            }
        ))

        return response

    @http('DELETE', '/news/<int:news_id>')
    @session_start
    def delete_news(self, request, session, response, news_id):
        response.mimetype = "application/json"

        if not session["username"]:
            response.status_code = 401
            response.set_data(json.dumps(
                {
                    "action": "post_new_news",
                    "action_status": "error",
                    "message": "Unauthorized: please login first"
                }
            ))
            return response

        response.status_code = 400

        if news_id is None:
            response.set_data(json.dumps(
                {
                    "action": "delete_news",
                    "action_status": "error",
                    "message": f"Bad request: missing news_id parameter"
                }
            ))

        response.status_code = 404

        if not self.news_rpc.check_news_id_exist(news_id):
            response.set_data(json.dumps(
                {
                    "action": "delete_news",
                    "action_status": "error",
                    "message": "News id does not exist"
                }
            ))
            return response

        news_data = self.news_rpc.get_news_by_id(news_id)[0]
        response.status_code = 403

        if news_data["publisher"] != session["username"]:
            response.set_data(json.dumps(
                {
                    "action": "delete_news",
                    "action_status": "error",
                    "message": "Forbidden: you are not the publisher of this news"
                }
            ))
            return response

        response.status_code = 200

        self.news_rpc.delete_news(news_id)

        response.set_data(json.dumps(
            {
                "action": "delete_news",
                "action_status": "success",
                "message": "News deleted successfully"
            }
        ))

        return response

    # file methods

    @http('GET', '/file/<int:news_id>')
    @session_start
    def get_file(self, request, session, response, news_id):
        response.mimetype = "application/json"

        response.status_code = 400

        if news_id is None:
            response.set_data(json.dumps(
                {
                    "action": "get_files_from_news_id",
                    "action_status": "error",
                    "message": f"Bad request: missing news_id parameter"
                }
            ))
            return response

        response.status_code = 404

        if not self.news_rpc.check_news_id_exist(news_id):
            response.set_data(json.dumps(
                {
                    "action": "get_files_from_news_id",
                    "action_status": "error",
                    "message": "News id does not exist"
                }
            ))
            return response

        response.status_code = 200
        all_files = self.file_rpc.get_all_files_by_news_id(news_id)
        response.set_data(json.dumps(
            {
                "action": "get_files_from_news_id",
                "action_status": "success",
                "message": "Files fetched successfully",
                "files": all_files,
                "count": len(all_files)
            }
        ))
        return response
