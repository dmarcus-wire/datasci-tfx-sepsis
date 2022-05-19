import json
from pydoc import pager
from flask import Flask, jsonify, request
from prediction import predict
from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Histogram
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
import logging
import time
import boto3

application = Flask(__name__)

s3 = boto3.client('s3',
                  os.environ['S3_REGION'],
                  aws_access_key_id = os.environ['S3_ACCESS_KEY_ID'],
                  aws_secret_access_key = os.environ['S3_SECRET_ACCESS_KEY'])

s3.download_file(os.environ['S3_BUCKET'], "models/vitals_simple/1651022813/saved_model.pb", 'saved_model.pb')

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
        p = predict(body)

        #
        # Increment the prediction metric counts.
        #
        if p["prediction"] == "legitimate":
                legit.inc()
        if p["prediction"] == "fraud":
                fraud.inc()

        logging.debug(f'Prediction: {p["prediction"]}')

        r = jsonify(p)
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