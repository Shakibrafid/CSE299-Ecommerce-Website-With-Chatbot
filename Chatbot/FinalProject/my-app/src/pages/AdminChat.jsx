import { useState } from "react";
import { Link } from "react-router-dom";
import { API_BASE, getJsonHeaders } from "../apiConfig";

function AdminChat() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([
    {
      sender: "AI",
      text: "Admin assistant ready. Ask about products, stock, users or orders.",
    },
  ]);

  const [isLoading, setIsLoading] = useState(false);

  const accessToken = localStorage.getItem("accessToken");

  async function sendMessage(e) {
    e.preventDefault();

    const adminMessage = message.trim();

    if (!adminMessage || isLoading) return;

    if (!accessToken) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "AI",
          text: "You must log in with an administrator account first.",
        },
      ]);
      return;
    }

    setMessages((prev) => [
      ...prev,
      {
        sender: "You",
        text: adminMessage,
      },
    ]);

    setMessage("");
    setIsLoading(true);

    try {
      const response = await fetch(
        `${API_BASE}/api/ai/admin-chat/`,
        {
          method: "POST",
          headers: getJsonHeaders(),
          body: JSON.stringify({
            message: adminMessage,
          }),
        }
      );

      const data = await response.json();

      if (response.status === 401) {
        throw new Error("Your login has expired. Log in again.");
      }

      if (response.status === 403) {
        throw new Error(
          "Access denied. This account is not an administrator."
        );
      }

      if (!response.ok) {
        throw new Error(
          data.details ||
            data.error ||
            data.detail ||
            "The admin chatbot request failed."
        );
      }

      if (!data.reply) {
        throw new Error("The admin chatbot returned an empty reply.");
      }

      setMessages((prev) => [
        ...prev,
        {
          sender: "AI",
          text: data.reply,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "AI",
          text:
            error.message ||
            "Unable to connect to the admin chatbot.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  }

  if (!accessToken) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center px-6">
        <div className="max-w-md w-full bg-white rounded-3xl p-8 text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-3">
            Administrator Login Required
          </h1>

          <p className="text-gray-500 mb-6">
            Log in with a staff or administrator account to access
            the admin chatbot.
          </p>

          <Link
            to="/login"
            className="inline-block bg-indigo-600 text-white px-6 py-3 rounded-full font-semibold"
          >
            Go to Login
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white min-h-screen">
      <div className="bg-gray-950 py-14">
        <div className="max-w-3xl mx-auto px-6">
          <p className="text-amber-400 font-semibold text-sm uppercase tracking-wide mb-2">
            Administrator Only
          </p>

          <h1 className="text-4xl font-bold text-white">
            AI Business Assistant
          </h1>

          <p className="text-gray-400 mt-3">
            Read-only access to products, stock, users and order
            information.
          </p>
        </div>
      </div>

      <div className="max-w-3xl mx-auto px-6 py-12">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
          {[
            "How many products are active?",
            "Which products are low in stock?",
            "How many orders are there?",
            "Show the latest orders.",
          ].map((question) => (
            <button
              key={question}
              type="button"
              disabled={isLoading}
              onClick={() => setMessage(question)}
              className="text-left border border-gray-200 rounded-2xl p-3 text-sm text-gray-700 hover:border-indigo-500 hover:text-indigo-600 transition"
            >
              {question}
            </button>
          ))}
        </div>

        <div className="border border-gray-100 rounded-3xl shadow-sm h-96 overflow-y-auto p-6 mb-4 space-y-3 bg-gray-50">
          {messages.map((chatMessage, index) => (
            <div
              key={index}
              className={`flex ${
                chatMessage.sender === "You"
                  ? "justify-end"
                  : "justify-start"
              }`}
            >
              <div
                className={`max-w-[80%] px-4 py-3 rounded-2xl text-sm whitespace-pre-wrap ${
                  chatMessage.sender === "You"
                    ? "bg-indigo-600 text-white rounded-br-sm"
                    : "bg-white border border-gray-200 text-gray-800 rounded-bl-sm"
                }`}
              >
                {chatMessage.text}
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-white border border-gray-200 text-gray-500 px-4 py-3 rounded-2xl text-sm">
                Reading the database...
              </div>
            </div>
          )}
        </div>

        <form onSubmit={sendMessage} className="flex gap-3">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Ask about stock, products or orders..."
            disabled={isLoading}
            className="flex-1 border border-gray-200 rounded-full px-5 py-3"
          />

          <button
            type="submit"
            disabled={isLoading || !message.trim()}
            className="bg-gray-950 text-white px-6 py-3 rounded-full font-semibold disabled:bg-gray-400"
          >
            {isLoading ? "Checking..." : "Ask"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default AdminChat;