import { useState } from "react";
import { API_BASE, getJsonHeaders } from "../apiConfig";

function Chat() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([
    { sender: "AI", text: "Hello! How can I assist you today?" }
  ]);

  async function sendMessage(e) {
    e.preventDefault();
    if (!message.trim()) return;
    const userMessage = message;
    setMessages((prev) => [...prev, { sender: "You", text: userMessage }]);
    setMessage("");

    try {
      const response = await fetch(`${API_BASE}/api/ai/chat/`, {
        method: "POST",
        headers: getJsonHeaders(),
        body: JSON.stringify({ message: userMessage }),
      });

      const data = await response.json();
      if (!response.ok) {
        const errorText = data.detail || data.message || "Unable to send chat message.";
        setMessages((prev) => [...prev, { sender: "AI", text: errorText }]);
        return;
      }

      setMessages((prev) => [...prev, { sender: "AI", text: data.reply }]);
    } catch {
      setMessages((prev) => [...prev, { sender: "AI", text: "Unable to connect to the server." }]);
    }
  }

  return (
    <div className="bg-white min-h-screen">
      <div className="bg-gray-950 py-16">
        <div className="max-w-2xl mx-auto px-6">
          <p className="text-indigo-400 font-semibold text-sm uppercase tracking-wide mb-2">Support</p>
          <h1 className="text-4xl font-bold text-white">AI Shopping Assistant</h1>
        </div>
      </div>

      <div className="max-w-2xl mx-auto px-6 py-16">
        <div className="border border-gray-100 rounded-3xl shadow-sm h-96 overflow-y-auto p-6 mb-4 space-y-3 bg-gray-50">
          {messages.map((msg, index) => (
            <div key={index} className={`flex ${msg.sender === "You" ? "justify-end" : "justify-start"}`}>
              <div
                className={`max-w-[75%] px-4 py-2.5 rounded-2xl text-sm ${
                  msg.sender === "You"
                    ? "bg-indigo-600 text-white rounded-br-sm"
                    : "bg-white border border-gray-200 text-gray-800 rounded-bl-sm"
                }`}
              >
                {msg.text}
              </div>
            </div>
          ))}
        </div>

        <form onSubmit={sendMessage} className="flex gap-3">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 border border-gray-200 rounded-full px-5 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition"
          />
          <button type="submit" className="bg-gray-950 text-white px-6 py-3 rounded-full font-semibold hover:bg-indigo-600 transition">
            Send
          </button>
        </form>
      </div>
    </div>
  );
}

export default Chat;