from sys import path
from fastapi import FastAPI, Response, status
from fastapi.params import Cookie
from fastapi.responses import HTMLResponse, JSONResponse
import requests
import logging
import json
import os
import uuid

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/sso", response_class=HTMLResponse)
async def sso(response: Response):
    state_string = uuid.uuid4()
    response.set_cookie(key="slack_auth_state",
                        value=state_string, path="*", httponly=True)
    return f"""
    <html>
        <head>
            <title>Slack SSO</title>
        </head>
        <body>
            <a href="https://slack.com/oauth/v2/authorize?client_id={os.getenv('SLACK_CLIENT_ID')}&scope=chat:write,channels:read&state={state_string}&redirect_uri={os.getenv('SLACK_AUTH_REDIRECT_URL')}"><img alt=""Add to Slack"" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a>
        </body>
    </html>
    """


@app.get("/slack-auth-redirect")
async def slack_auth_redirect(code: str, state:  str, slack_auth_state: str = Cookie(...), ):
    logging.debug(code)
    if state != slack_auth_state:
        return HTMLResponse(content="SLACKログイン失敗", status_code=status.HTTP_401_UNAUTHORIZED)

    payload = {'client_id': os.getenv('SLACK_CLIENT_ID'),
               'client_secret': os.getenv('SLACK_CLIENT_SECRET'),
               'code': code}
    r = json.loads(requests.post(
        "https://slack.com/api/oauth.v2.access", data=payload).content)
    if not r["ok"]:
        return HTMLResponse(content="SLACKログイン失敗", status_code=status.HTTP_401_UNAUTHORIZED)
    return JSONResponse(content=r)
