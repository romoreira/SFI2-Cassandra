from flask import (
    Flask, jsonify, render_template, request, send_file
)
import subprocess, sys
from subprocess import run
import json


app = Flask(__name__)
import threading

predictions = []


class ThreadPredictions(threading.Thread):
    def __init__(self):
        super(ThreadPredictions, self).__init__()

    def run(self):
        # run some code here
        print('Threaded task has been completed')


class ThreadedTCPDump(threading.Thread):
    amount = 0

    def __init__(self, amount):
        super(ThreadedTCPDump, self).__init__()
        self.amout = amount

    def run(self):
        print("Running TCPDump with amout: " + str(self.amout))
        process = subprocess.run(['tcpdump', '-c', '10', '-i', 'eth0', '-vvv'], check=True, stdout=subprocess.PIPE,
                                 universal_newlines=True)
        output = process.stdout.read()
        print(str(output))
        return str(output)


class ThreadedFlowMeter(threading.Thread):
    predictor_ip = ""
    interface = ""
    process = ""

    def __init__(self, predictor_ip, interface):
        super(ThreadedFlowMeter, self).__init__()
        self.predictor_ip = predictor_ip
        self.interface = interface

    def run(self):
        # command cicflowmeter -i enp2s0 -c flows.csv -u http://192.168.0.212:8080/prediction
        cmd = 'cicflowmeter -i ' + str(self.interface) + ' -c flows.csv -u http://' + str(
            self.predictor_ip) + ':8080/prediction'
        self.process = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

    def kill(self):
        self.process.kill()


class ThreadedFlowMeterAlone(threading.Thread):
    def __init__(self):
        super(ThreadedFlowMeterAlone, self).__init__()

    def run(self):
        # command cicflowmeter -i enp2s0 -c flows.csv -u http://192.168.0.212:8080/prediction
        cmd = 'cicflowmeter -i eth0 -c /home/flows.csv'
        p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)


@app.route('/predictions_list', methods=['GET'])
def get_predictions_list():
    return {'predictions': predictions}, 200


@app.route('/predictions', methods=['POST'])
def predition_task():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json_string = request.get_json()
        print("JSON Recebido pelo prediction: " + str(json_string))
        # json_string = json.dumps(json_string, sort_keys=True)
        predictions.append(json_string)
        return {'result': 'ok'}
    elif request.data:
        print('JSON RECEIVED:' + str(request.data))
        return {"src_ip": "SOURCE_IP", "src_port": "SOURCE_PORT", "dst_ip": "DST_IP", "dst_port": "DST_PORT",
                "result": [0], "probability": [[0]]}
    else:
        return 'Content-Type not supported!'

@app.route('/start_flowmeter', methods=['GET'])
def start_flowmeter_alone():
    flow_meter = ThreadedFlowMeterAlone()
    flow_meter.start()
    # flow_meter.join()
    return {'status': 'ok', 'result': str("FlowMeter is Running")}, 200

@app.route('/stop_flowmeter', methods=['GET'])
def stop_flowmeter():
    command = f"ps aux | grep cicflowmeter | grep -v grep | awk '{{print $2}}' | xargs kill -9"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    command = f"rm -rf /home/flows.csv"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return {'status': 'ok', 'result': str("FlowMeter is not Running")}, 200

@app.route('/download', methods=['GET'])
def download():
    directory = "/home"
    filepath =  directory+'/'+"flows.csv"
    return send_file(filepath, as_attachment=True)

@app.route('/start/<predictor_ip>/<interface>', methods=['GET'])
def start_flowmeter(predictor_ip, interface):
    flow_meter = ThreadedFlowMeter(predictor_ip, interface)
    flow_meter.start()
    # flow_meter.join()
    return {'status': 'ok', 'result': str("FlowMeter is Running")}, 200

@app.route('/read/<amount>', methods=['GET'])
def read(amount):
    tcpdump = ThreadedTCPDump(amount)
    result = tcpdump.run()
    return {'status': 'ok', 'result': result}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
