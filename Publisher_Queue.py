import os
import json
import datetime
from flask_cors import CORS
from flask import Flask, request, jsonify
from solace.messaging.messaging_service import MessagingService, RetryStrategy
from solace.messaging.resources.topic import Topic
from solace.messaging.publisher.persistent_message_publisher import PersistentMessagePublisher
from solace.messaging.config.transport_security_strategy import TLS

app = Flask(__name__)
CORS(app)

# Solace Configuration 
SOLACE_HOST = os.getenv("SOLACE_HOST")
SOLACE_VPN = os.getenv("SOLACE_VPN")
SOLACE_USERNAME = os.getenv("SOLACE_USERNAME")
SOLACE_PASSWORD = os.getenv("SOLACE_PASSWORD")

TOPIC_NAME = "solace/messages/input"  # Topic name

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

try:
    messaging_service.connect()
    print("✅ Connected to Solace successfully")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    exit(1)

# Publisher Setup
publisher: PersistentMessagePublisher = messaging_service.create_persistent_message_publisher_builder().build()
publisher.start()
message_builder = messaging_service.message_builder()

@app.route('/send', methods=['POST'])
def send_message():
    try:
        data = request.json
        message = data.get('message', '')
        if not message:
            return jsonify({"error": "Message cannot be empty"}), 400
        sent_at = datetime.datetime.now().isoformat()
        received_at = None
        payload = json.dumps({
            "text": message,
            "sent_at": sent_at,
            "received_at": received_at
        })

        outbound_message = message_builder.build(payload)
        publisher.publish(destination=Topic.of(TOPIC_NAME), message=outbound_message)
        print(f"🚀 Sent message: {payload}")
        return jsonify({"status": "Message sent", "message": payload})
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5001) 
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        publisher.terminate()
        messaging_service.disconnect()
        print("✅ Messaging service disconnected.")
