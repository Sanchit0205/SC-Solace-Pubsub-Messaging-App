import os
import json
import datetime
from flask_cors import CORS
from flask import Flask, jsonify
from solace.messaging.messaging_service import MessagingService, RetryStrategy
from solace.messaging.resources.queue import Queue
from solace.messaging.receiver.persistent_message_receiver import PersistentMessageReceiver
from solace.messaging.receiver.message_receiver import MessageHandler
from solace.messaging.receiver.inbound_message import InboundMessage
from solace.messaging.config.transport_security_strategy import TLS

app = Flask(__name__)
CORS(app)

# Solace Configuration
SOLACE_HOST = os.getenv("SOLACE_HOST")
SOLACE_VPN = os.getenv("SOLACE_VPN")
SOLACE_USERNAME = os.getenv("SOLACE_USERNAME")
SOLACE_PASSWORD = os.getenv("SOLACE_PASSWORD")
QUEUE_NAME = "persistent-message-queue"  # Queue name

# Broker Properties
broker_props = {
    "solace.messaging.transport.host": SOLACE_HOST,
    "solace.messaging.service.vpn-name": SOLACE_VPN,
    "solace.messaging.authentication.scheme.basic.username": SOLACE_USERNAME,
    "solace.messaging.authentication.scheme.basic.password": SOLACE_PASSWORD
}

# Transport Security
transport_security = TLS.create().with_certificate_validation(True, False, r"\TrustStore")

# Initialize Messaging Service
messaging_service = MessagingService.builder().from_properties(broker_props) \
    .with_transport_security_strategy(transport_security) \
    .with_reconnection_retry_strategy(RetryStrategy.parametrized_retry(20, 3)) \
    .build()

received_messages = []
receiver = None
is_receiver_active = False  


class QueueMessageHandler(MessageHandler):
    def on_message(self, message: InboundMessage):
        try:
            payload = message.get_payload_as_string() or message.get_payload_as_bytes().decode()
            data = json.loads(payload)
            data["received_at"] = datetime.datetime.now().isoformat()
            print(f"📩 Received message: {data['text']}")
            received_messages.append(data)
        except Exception as e:
            print(f"⚠️ Error processing message: {e}")



@app.route('/start_receiver', methods=['POST'])
def start_receiver():
    global receiver, is_receiver_active
    if is_receiver_active:
        return jsonify({"status": "Receiver already running"}), 400

    try:
        messaging_service.connect()
        queue = Queue.durable_exclusive_queue(QUEUE_NAME)
        receiver = messaging_service.create_persistent_message_receiver_builder().with_message_auto_acknowledgement().build(queue)
        receiver.start()
        receiver.receive_async(QueueMessageHandler())
        is_receiver_active = True
        print(f"🎧 Listening on queue: {QUEUE_NAME}")
        return jsonify({"status": "Receiver started"}), 200
    except Exception as e:
        print(f"❌ Error starting receiver: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/stop_receiver', methods=['POST'])
def stop_receiver():
    global receiver, is_receiver_active
    if not is_receiver_active:
        return jsonify({"status": "Receiver is not running"}), 400

    try:
        receiver.terminate()
        receiver = None
        is_receiver_active = False
        print("🛑 Receiver stopped")
        return jsonify({"status": "Receiver stopped"}), 200
    except Exception as e:
        print(f"❌ Error stopping receiver: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/receive', methods=['GET'])
def receive_message():
    return jsonify({"messages": received_messages if received_messages else "No new messages"})

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5002)  # Running on port 5002
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        if receiver:
            receiver.terminate()
        messaging_service.disconnect()
        print("✅ Messaging service disconnected.")
