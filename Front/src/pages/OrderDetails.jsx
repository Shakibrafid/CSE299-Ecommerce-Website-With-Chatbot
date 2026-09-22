import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { API_BASE, getAuthHeaders } from "../apiConfig";

function OrderDetail() {
  const { id } = useParams();
  const [order, setOrder] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE}/api/orders/orders/${id}/`, {
      headers: getAuthHeaders(),
    })
      .then((response) => response.json())
      .then((data) => setOrder(data))
      .catch((error) => console.error("Error fetching order:", error));
  }, [id]);

  if (!order) {
    return (
      <div className="max-w-2xl mx-auto px-6 py-24 text-center">
        <p className="text-gray-500 mb-6">Loading order...</p>
        <Link to="/orders" className="text-indigo-600 font-semibold hover:underline">Back to Order History</Link>
      </div>
    );
  }

  return (
    <div className="bg-white min-h-screen">
      <div className="bg-gray-950 py-16">
        <div className="max-w-4xl mx-auto px-6">
          <Link to="/orders" className="text-indigo-400 text-sm font-semibold hover:underline mb-2 inline-block">
            ← Back to Order History
          </Link>
          <h1 className="text-4xl font-bold text-white">Order #{order.order_number || order.id}</h1>
          <p className="text-gray-400 mt-1">{order.created_at}</p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-6 py-16 grid md:grid-cols-5 gap-12">
        <div className="md:col-span-2 space-y-6">
          <div>
            <p className="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-1">Shipping Address</p>
            <p className="text-gray-900">{order.shipping_address}</p>
          </div>
          <div>
            <p className="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-1">Billing Address</p>
            <p className="text-gray-900">{order.billing_address}</p>
          </div>
          <div>
            <p className="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-1">Payment Method</p>
            <p className="text-gray-900 capitalize">{order.payment_method}</p>
          </div>
        </div>

        <div className="md:col-span-3">
          <h2 className="text-lg font-bold text-gray-900 mb-4">Order summary</h2>
          <div className="bg-gray-50 rounded-2xl p-6 space-y-3">
            <div className="flex justify-between text-sm text-gray-700">
              <span>Subtotal</span>
              <span className="font-medium">৳{order.subtotal}</span>
            </div>
            <div className="flex justify-between text-sm text-gray-700">
              <span>Shipping</span>
              <span className="font-medium">৳{order.shipping_cost}</span>
            </div>
            <div className="border-t border-gray-200 pt-3 flex justify-between">
              <span className="font-semibold text-gray-900">Total</span>
              <span className="font-bold text-gray-900 text-lg">৳{order.total_amount}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default OrderDetail;