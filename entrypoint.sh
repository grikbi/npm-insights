#!/bin/bash

# gunicorn --pythonpath /recommendation_engine -b 0.0.0.0:$SERVICE_PORT --workers=2 -k sync -t $SERVICE_TIMEOUT flask_predict:app
if [[ -z "${SERVICE_PORT}" ]]; then
  SERVICE_PORT="6005"
fi
# Need to export these variables since Click complains otherwise
export LC_ALL="en_US.UTF-8"
export LANG="en_US.UTF-8"

uvicorn --host 0.0.0.0 --port $SERVICE_PORT recommendation_engine.flask_predict:app