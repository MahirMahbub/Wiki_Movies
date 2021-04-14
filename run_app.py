import uvicorn
from app.config import AppConfig
import os
from run_package import install_packages

# PORT = AppConfig.APP_HOST_PORT
# BIND = AppConfig.APP_HOST_NAME
PORT = 8000
BIND = '127.0.0.1'
WORKERS = 10
RELOAD = True

if __name__ == "__main__":
    # install_packages()
    # uvicorn.run("hello:app", host=BIND, port=int(PORT), reload=RELOAD, debug=RELOAD, workers=int(WORKERS))
    uvicorn.run("app.main:app", host=BIND, port=int(PORT), reload=RELOAD, debug=RELOAD, workers=int(WORKERS))