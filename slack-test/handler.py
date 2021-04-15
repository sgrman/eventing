from flask import Flask, request, jsonify
import requests
from cloudevents.http import from_http
import logging,json
from slack_sdk.webhook import WebhookClient

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__)
url = 'https://hooks.slack.com/services/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'
webhook = WebhookClient(url)
@app.route('/', methods=['GET','POST'])
def echo():
    if request.method == 'GET':
        sc = 200
        msg = ' to this endpoint to echo cloud events'
        message = {
            'status': sc,
            'message': msg,
        }
        resp = jsonify(message)
        resp.status_code = sc
        return resp

    if request.method == 'POST':
        try:
            event = from_http(request.headers, request.get_data(),None)
            
            data = event.data
            
            e = {
                "attributes": event._attributes,
                "data": data
            }
         
            payload = { "text": f"*CLOUDEVENT_ID*:\n{e['attributes']['id']}\n\n Source:  {e['attributes']['source']}\n Type:  {e['attributes']['type']}\n *Subject*:  *{e['attributes']['subject']}*\n Time:  {e['attributes']['time']}\n\n *EVENT DATA*:\n key:  {e['data']['Key']}\n user:  {e['data']['UserName']}\n datacenter:  {e['data']['Datacenter']['Name']}\n Host:  {e['data']['Host']['Name']}\n VM:  {e['data']['Vm']['Name']}\n\n Message: {e['data']['FullFormattedMessage']}" }  
                       
            requests.post(url=url, json=payload)
                        
            # app.logger.info(f'"***cloud event*** {json.dumps(e)}')
            return {}, 204
        
        except Exception as e:
            sc = 404
            msg = f'could not decode cloud event: {e}'
            # app.logger.error(msg)
            message = {
                'status': sc,
                'error': msg,
            }
            resp = jsonify(message)
            resp.status_code = sc
            return resp

# hint: run with FLASK_ENV=development FLASK_APP=handler.py flask run
if __name__ == "__main__":
    app.run()