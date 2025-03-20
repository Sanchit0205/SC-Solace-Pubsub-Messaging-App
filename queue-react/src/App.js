import React from "react";
import MessageSender from "./components/MessageSender";
import MessageReceiver from "./components/MessageReceiver";
import "./App.css"; 

function App() {
  return (
    <div>
      <h1>Solace Messaging App</h1>
      <MessageSender />
      <MessageReceiver />
    </div>
  );
}

export default App;
