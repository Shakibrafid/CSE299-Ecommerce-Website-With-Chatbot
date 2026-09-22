import { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import { API_BASE, getAuthHeaders, getJsonHeaders } from "../apiConfig";

function Checkout() {
  const [cart, setCart] = useState([]);
  const [shippingAddress, setShippingAddress] = useState("");
  const [billingAddress, setBillingAddress] = useState("");
  const [paymentMethod, setPaymentMethod] = useState('credit_card');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetch(`${API_BASE}/api/cart/cart-items/`, {
      headers: getAuthHeaders(),
    })
      .then((response) => response.json())
      .then((data) => setCart(data))
      .catch((error) => {
        console.error("Error fetching cart:", error);
        setCart([]);
      });
  }, []);

  function calculateShippingCost() {
    return 120;
  }

  const subtotal = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const shippingCost = calculateShippingCost();
  const total = subtotal + shippingCost;

  async function handleSubmit(e) {
    e.preventDefault();
    const token = localStorage.getItem("accessToken");
    try {
      const response = await fetch(`${API_BASE}/api/orders/orders/`, {
        method: "POST",
        headers: getJsonHeaders(),
        body: JSON.stringify({
          shipping_address: shippingAddress,
          billing_address: billingAddress,
          payment_method: paymentMethod,
        }),
      });
      if (response.ok) {
        navigate("/orders");
      } else {
        console.error("Order failed:", await response.text());
      }
    } catch (error) {
      console.error("Error placing order:", error);
    }
  }

  const inputClass = "w-full border border-gray-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition";
  const labelClass = "block text-sm font-semibold text-gray-700 mb-1.5";

  return (
    <div className="bg-white min-h-screen">
      <div className="bg-gray-950 py-16">
        <div className="max-w-4xl mx-auto px-6">
          <p className="text-indigo-400 font-semibold text-sm uppercase tracking-wide mb-2">Almost there</p>
          <h1 className="text-4xl font-bold text-white">Checkout</h1>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-6 py-16 grid md:grid-cols-5 gap-12">
        <div className="md:col-span-2 order-2 md:order-1">
          <h2 className="text-lg font-bold text-gray-900 mb-4">Order Summary</h2>
          <div className="bg-gray-50 rounded-2xl p-6 space-y-3">
            {cart.map((item) => (
              <div key={item.id} className="flex justify-between text-sm text-gray-700">
                <span>{item.name} × {item.quantity}</span>
                <span className="font-medium">৳{(item.price * item.quantity).toFixed(2)}</span>
              </div>
            ))}
            <div className="border-t border-gray-200 pt-3 space-y-3">
              <div className="flex justify-between text-sm text-gray-700">
                <span>Subtotal</span>
                <span className="font-medium">৳{subtotal.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-sm text-gray-700">
                <span>Shipping</span>
                <span className="font-medium">৳{shippingCost.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="font-semibold text-gray-900">Total</span>
                <span className="font-bold text-gray-900 text-lg">৳{total.toFixed(2)}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="md:col-span-3 order-1 md:order-2">
          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className={labelClass}>Shipping Address</label>
              <input type="text" value={shippingAddress} onChange={(e) => setShippingAddress(e.target.value)} className={inputClass} required />
            </div>
            <div>
              <label className={labelClass}>Billing Address</label>
              <input type="text" value={billingAddress} onChange={(e) => setBillingAddress(e.target.value)} className={inputClass} required />
            </div>
            <div>
              <label className={labelClass}>Payment Method</label>
              <select value={paymentMethod} onChange={(e) => setPaymentMethod(e.target.value)} className={inputClass} required>
                <option value="credit_card">Credit Card</option>
                <option value="paypal">PayPal</option>
                <option value="bank_transfer">Bank Transfer</option>
              </select>
            </div>
            <button type="submit" className="w-full bg-gray-950 text-white py-4 rounded-full font-semibold hover:bg-indigo-600 transition mt-2">
              Place Order — ৳{total.toFixed(2)}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Checkout;