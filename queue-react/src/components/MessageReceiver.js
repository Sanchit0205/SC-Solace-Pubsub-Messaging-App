import React, { useState, useEffect } from "react";
import axios from "axios";
import "./MessageReceiver.css";

// Helper function to format date strings (date and time only)
const formatDate = (dateStr) => {
  if (!dateStr) return "";
  const date = new Date(dateStr);
  return date.toLocaleString(); // Customize as needed
};

const MessageReceiver = () => {
  const [messages, setMessages] = useState([]);
  const [receiverStatus, setReceiverStatus] = useState(false);

  const fetchMessages = async () => {
    try {
      const response = await axios.get("http://localhost:5002/receive");
      // Expected message format: { text: "Message", sent_at: "...", received_at: "..." }
      const receivedMessages = Array.isArray(response.data.messages)
        ? response.data.messages
        : [];
      setMessages(receivedMessages);
    } catch (error) {
      console.error("Error fetching messages:", error);
      setMessages([]);
    }
  };

  const startReceiver = async () => {
    try {
      await axios.post("http://localhost:5002/start_receiver");
      setReceiverStatus(true);
    } catch (error) {
      console.error("Error starting receiver:", error);
    }
  };

  const stopReceiver = async () => {
    try {
      await axios.post("http://localhost:5002/stop_receiver");
      setReceiverStatus(false);
    } catch (error) {
      console.error("Error stopping receiver:", error);
    }
  };

  // Auto-fetch messages every 5 seconds
  useEffect(() => {
    fetchMessages(); // initial fetch
    const interval = setInterval(() => {
      fetchMessages();
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="receiver-container">
      <div className="box receiver-box">
        <h2>Message Receiver</h2>
        <div className="status">
          Receiver Status:{" "}
          <span className={receiverStatus ? "active" : "inactive"}>
            {receiverStatus ? "Running" : "Stopped"}
          </span>
        </div>
        <div className="button-group">
          <button className="button start-button" onClick={startReceiver}>
            Start Receiver
          </button>
          <button className="button stop-button" onClick={stopReceiver}>
            Stop Receiver
          </button>
        </div>
        <div className="message-scroll-container">
        <ul className="message-list">
  {messages.length > 0 ? (
    messages.slice(0).reverse().map((msg, index) => (
      <li key={index} className="message-item">
        <div className="message-text">{msg.text || msg}</div>
        <div className="tooltip">
          <div>Sent at: {msg.sent_at ? formatDate(msg.sent_at) : "N/A"}</div>
          <div>Received at: {msg.received_at ? formatDate(msg.received_at) : "N/A"}</div>
        </div>
      </li>
    ))
  ) : (
    <li className="no-messages">No new messages</li>
  )}
</ul>

        </div>
      </div>
    </div>
  );
};

export default MessageReceiver;
