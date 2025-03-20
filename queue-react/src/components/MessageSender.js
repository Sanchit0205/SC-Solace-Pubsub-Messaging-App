import React, { useState } from "react";
import axios from "axios";
import "./MessageSender.css"; // Import CSS file

const MessageSender = () => {
  const [message, setMessage] = useState("");

  const sendMessage = async () => {
    if (!message.trim()) return; // Prevent empty messages

    try {
      await axios.post("http://localhost:5001/send", { message });
      setMessage(""); // Clear input after sending
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  return (
    <div className="sender-container">
      <div className="box sender-box">
        <h2>Message Sender</h2>
        <textarea
          className="message-input" 
          rows="3"
          placeholder="Type your message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        ></textarea>
        <button className="button send-button" onClick={sendMessage}>
          Send Message
        </button>
      </div>
    </div>
  );
};

export default MessageSender;
