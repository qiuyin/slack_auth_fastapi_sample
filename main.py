from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import requests
import logging
import json
import os

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/sso", response_class=HTMLResponse)
async def sso():
    return f"""
    <html>
        <head>
            <title>Slack SSO</title>
        </head>
        <body>
            <a href="https://slack.com/oauth/v2/authorize?client_id={os.getenv('SLACK_CLIENT_ID')}&scope=chat:write,channels:read&state=statestring&redirect_uri=http://localhost:3004/slack-auth-redirect"><img alt=""Add to Slack"" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a>
        </body>
    </html>
    """


@app.get("/slack-auth-redirect")
async def slack_auth_redirect(code: str):
    logging.debug(code)
    payload = {'client_id': os.getenv('SLACK_CLIENT_ID'),
               'client_secret': os.getenv('SLACK_CLIENT_SECRET'),
               'code': code}
    r = requests.post("https://slack.com/api/oauth.v2.access", data=payload)
    return JSONResponse(content=json.loads(r.content))
