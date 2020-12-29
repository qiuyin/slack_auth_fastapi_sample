# install package

```
poetry install
```

# Env setting

```
export SLACK_CLIENT_ID=111.111
export SLACK_CLIENT_SECRET=\*\*\*
export SLACK_AUTH_REDIRECT_URL=http://localhost:3004/slack-auth-redirect
```

# run

```
poetry run uvicorn main:app --reload --port 3004
```
