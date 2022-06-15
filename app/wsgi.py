import json
import logging
import os

from flask import (
    Flask,
    jsonify,
    request
)

import tensorflow as tf

from prometheus_client import (
    Counter,
    Histogram,
    make_wsgi_app
)
from werkzeug.middleware.dispatcher import DispatcherMiddleware


from s3_util import (
    downloadDirectoryFromS3
)


application = Flask(__name__)

logging.info(f'Tensorflow version: {tf.__version__}')
logging.info(f"S3_REGION: {os.environ['S3_REGION']}")
logging.info(f"S3_ACCESS_KEY_ID: {os.environ['S3_ACCESS_KEY_ID']}")
logging.info(f"S3_BUCKET: {os.environ['S3_BUCKET']}")

remote_folder = "models/vitals_simple/1651022813/"
logging.info(f"Downloading s3://{os.environ['S3_BUCKET']}/{remote_folder}")
downloadDirectoryFromS3(os.environ['S3_BUCKET'], remote_folder)

# Load, print and make a prediction.
loaded_model = tf.keras.models.load_model(remote_folder)


#
# Define the Prometheus metrics.
#
c = Counter('model_server_requests', 'Requests')
legit = Counter('model_server_legit_predictions', 'Legitimate Transactions')
fraud = Counter('model_server_fraud_predictions', 'Fraudulent Transactions')
latency = Histogram('model_server_request_latency_seconds', 'Prediction processing time', buckets=[0.009, 0.0095, 0.01])

logging.basicConfig(level=logging.INFO)

@application.route('/')
@application.route('/status')
def status():
    logging.info(f'{Flask.response_class()}')
    return jsonify({'status': 'ok'})

@latency.time()
@application.route('/predictions', methods=['POST'])
def create_prediction():
    with latency.time():
        c.inc()
        data = request.data or '{}'
        body = json.loads(data)
        prediction = loaded_model((tf.constant(body['hr'], shape=(1,1)), tf.constant(body['resp'], shape=(1,1)), tf.constant(body['temp'], shape=(1,1)))).numpy()[0][0]

        #
        # Increment the prediction metric counts.
        #
        if prediction == 1:
            legit.inc()
        else:
            fraud.inc()

        logging.debug(f'Prediction: {prediction}')

        r = jsonify({'isSepsis': prediction})
        return r

@application.errorhandler(404)
def invalid_route(e):
    logging.info(f'errorCode : 404, message : Route not found')
    return jsonify({'errorCode' : 404, 'message' : 'Route not found'})

#
# Add prometheus wsgi middleware to route /metrics requests
#
application.wsgi_app = DispatcherMiddleware(application.wsgi_app, {
    '/metrics': make_wsgi_app()
})
