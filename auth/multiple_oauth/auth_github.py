from rauth import OAuth2Service
from flask import request, redirect
from rauth.compat import parse_qsl
from multiple_oauth.oauth import OAuthSignIn


class GithubSignIn(OAuthSignIn):
    def __init__(self):
        super(GithubSignIn, self).__init__("github")
        self.service = OAuth2Service(
            name="github",
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url="https://github.com/login/oauth/authorize",
            access_token_url="https://github.com/login/oauth/access_token",
            base_url="https://api.github.com/user",
        )

    def authorize(self):
        return redirect(
            self.service.get_authorize_url(
                scope="email",
                response_type="code",
                redirect_uri=self.get_callback_url(),
            )
        )

    def callback(self):
        def parse_utf8_qsl(s):
            d = dict(parse_qsl(s))
            ans = dict()
            for k, v in d.items():  # pragma: no cover
                if not isinstance(k, bytes) and not isinstance(v, bytes):
                    # skip this iteration if we have no keys or values to update
                    continue
                k_ = k
                v_ = v
                if isinstance(k, bytes):
                    k_ = k.decode("utf-8")
                if isinstance(v, bytes):
                    v_ = v.decode("utf-8")
                ans[k_] = v_
            return ans

        if "code" not in request.args:
            return None, None, None

        request_token = request.args["code"]
        print(request_token)
        data = {
            "code": request.args["code"],
            "grant_type": "authorization_code",
            "redirect_uri": self.get_callback_url(),
        }

        oauth_session = self.service.get_auth_session(data=data, decoder=parse_utf8_qsl)
        
        user_info = oauth_session.get(
            self.service.base_url, params={"format": "json"}
        ).json()
        return user_info
