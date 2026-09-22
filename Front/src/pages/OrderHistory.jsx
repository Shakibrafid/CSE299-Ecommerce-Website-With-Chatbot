import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { API_BASE, getAuthHeaders } from "../apiConfig";

function OrderHistory() {
  const [orders, setOrders] = useState([]);
  const token = localStorage.getItem("accessToken");

  useEffect(() => {
    if (!token) return;

    fetch(`${API_BASE}/api/orders/orders/`, {
      headers: getAuthHeaders(),
    })
      .then((response) => response.json())
      .then((data) => setOrders(Array.isArray(data) ? data : []))
      .catch((error) => {
        console.error("Error fetching orders:", error);
        setOrders([]);
      });
  }, [token]);

  return (
    <div className="bg-white min-h-screen">
      <div className="bg-gray-950 py-16">
        <div className="max-w-4xl mx-auto px-6">
          <p className="text-indigo-400 font-semibold text-sm uppercase tracking-wide mb-2">Your Account</p>
          <h1 className="text-4xl font-bold text-white">Order History</h1>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-6 py-16">
        {!token ? (
          <div className="text-center py-16">
            <p className="text-gray-500 mb-6">Please log in to view your order history.</p>
            <Link
              to="/login"
              className="inline-block bg-gray-900 text-white px-8 py-3 rounded-full font-semibold hover:bg-indigo-600 transition"
            >
              Go to Login
            </Link>
          </div>
        ) : orders.length === 0 ? (
          <div className="text-center py-16">
            <p className="text-gray-500 mb-6">No orders placed yet.</p>
            <Link to="/products" className="inline-block bg-gray-900 text-white px-8 py-3 rounded-full font-semibold hover:bg-indigo-600 transition">
              Start Shopping
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {orders.map((order) => (
              <Link
                key={order.id}
                to={`/orders/${order.id}`}
                className="group flex justify-between items-center bg-white border border-gray-100 rounded-2xl p-6 shadow-sm hover:shadow-md hover:border-indigo-200 transition"
              >
                <div>
                  <p className="font-semibold text-gray-900 group-hover:text-indigo-600 transition">
                    Order #{order.order_number || order.id}
                  </p>
                  <p className="text-sm text-gray-500">{order.created_at}</p>
                </div>
                <div className="text-right">
                  <p className="font-bold text-gray-900">৳{order.total_amount}</p>
                  <p className="text-sm text-gray-400">Includes shipping ৳{order.shipping_cost}</p>
                  <p className="text-sm text-gray-400">View details →</p>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default OrderHistory;