import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { API_BASE, getAuthHeaders } from "../apiConfig";

function Cart() {
  const [cart, setCart] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("accessToken");
    if (!token) {
      setLoading(false);
      setCart([]);
      return;
    }

    fetch(`${API_BASE}/api/cart/cart-items/`, {
      headers: getAuthHeaders(),
    })
      .then(async (response) => {
        if (!response.ok) {
          throw new Error(response.status === 401 ? "Please log in to view your cart." : "Unable to load your cart.");
        }

        const data = await response.json();
        const items = Array.isArray(data) ? data : data.items || [];
        setCart(items);
      })
      .catch((error) => {
        console.error("Error fetching cart:", error);
        setError(error.message || "Unable to load your cart.");
        setCart([]);
      })
      .finally(() => setLoading(false));
  }, []);

  function removeFromCart(id) {
    fetch(`${API_BASE}/api/cart/cart-items/${id}/`, {
      method: "DELETE",
      headers: getAuthHeaders(),
    })
      .then(() => setCart((prev) => prev.filter((item) => item.id !== id)))
      .catch((error) => {
        console.error("Error removing item:", error);
        setError("Unable to remove this item right now.");
      });
  }

  function updateQuantity(id, delta) {
    const item = cart.find((entry) => entry.id === id);
    if (!item) return;

    const nextQuantity = Number(item.quantity ?? 1) + delta;
    if (nextQuantity <= 0) {
      removeFromCart(id);
      return;
    }

    fetch(`${API_BASE}/api/cart/cart-items/${id}/`, {
      method: "PATCH",
      headers: {
        ...getAuthHeaders(),
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ quantity: nextQuantity }),
    })
      .then(async (response) => {
        if (!response.ok) {
          throw new Error("Unable to update quantity.");
        }

        const updatedItem = await response.json();
        setCart((prev) => prev.map((entry) => (entry.id === id ? { ...entry, ...updatedItem, quantity: nextQuantity } : entry)));
      })
      .catch((error) => {
        console.error("Error updating quantity:", error);
        setError("Unable to update quantity right now.");
      });
  }

  const total = cart.reduce((sum, item) => {
    const unitPrice = Number(item.price ?? item.price_at_add ?? item.product_detail?.price ?? 0);
    return sum + unitPrice * Number(item.quantity ?? 1);
  }, 0);

  if (loading) {
    return (
      <div className="bg-white min-h-screen flex items-center justify-center">
        <p className="text-gray-600">Loading your cart...</p>
      </div>
    );
  }

  return (
    <div className="bg-white min-h-screen">
      <div className="bg-gray-950 py-16">
        <div className="max-w-4xl mx-auto px-6">
          <p className="text-indigo-400 font-semibold text-sm uppercase tracking-wide mb-2">Your Selection</p>
          <h1 className="text-4xl font-bold text-white">Cart</h1>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-6 py-16">
        {error && <p className="text-red-600 mb-6">{error}</p>}
        {!localStorage.getItem("accessToken") ? (
          <div className="text-center py-16">
            <p className="text-gray-500 mb-6">Please log in to view your cart.</p>
            <Link to="/login" className="inline-block bg-gray-900 text-white px-8 py-3 rounded-full font-semibold hover:bg-indigo-600 transition">
              Go to Login
            </Link>
          </div>
        ) : cart.length === 0 ? (
          <div className="text-center py-16">
            <p className="text-gray-500 mb-6">Your cart is empty.</p>
            <Link to="/products" className="inline-block bg-gray-900 text-white px-8 py-3 rounded-full font-semibold hover:bg-indigo-600 transition">
              Browse Products
            </Link>
          </div>
        ) : (
          <>
            <div className="space-y-4 mb-10">
              {cart.map((item) => {
                const itemName = item.product_detail?.name || item.name || "Product";
                const itemPrice = Number(item.price ?? item.price_at_add ?? item.product_detail?.price ?? 0);
                return (
                  <div key={item.id} className="flex justify-between items-center bg-white border border-gray-100 rounded-2xl p-5 shadow-sm hover:shadow-md transition">
                    <div>
                      <h3 className="font-semibold text-gray-900">{itemName}</h3>
                      <p className="text-gray-500 text-sm">৳{itemPrice.toFixed(2)} × {item.quantity}</p>
                    </div>
                    <div className="flex items-center gap-3">
                      <button
                        onClick={() => updateQuantity(item.id, -1)}
                        className="h-8 w-8 rounded-full border border-gray-300 text-lg font-semibold text-gray-700 hover:border-indigo-500 hover:text-indigo-600 transition"
                      >
                        −
                      </button>
                      <span className="min-w-6 text-center font-semibold text-gray-900">{item.quantity}</span>
                      <button
                        onClick={() => updateQuantity(item.id, 1)}
                        className="h-8 w-8 rounded-full border border-gray-300 text-lg font-semibold text-gray-700 hover:border-indigo-500 hover:text-indigo-600 transition"
                      >
                        +
                      </button>
                      <button onClick={() => removeFromCart(item.id)} className="ml-2 text-sm font-semibold text-red-500 hover:text-red-700 transition">
                        Remove
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
            <div className="flex justify-between items-center border-t border-gray-200 pt-6">
              <span className="text-lg font-semibold text-gray-900">Total</span>
              <span className="text-2xl font-bold text-gray-900">৳{total.toFixed(2)}</span>
            </div>
            <Link to="/checkout" className="mt-8 block text-center bg-gray-950 text-white py-4 rounded-full font-semibold hover:bg-indigo-600 transition">
              Proceed to Checkout
            </Link>
          </>
        )}
      </div>
    </div>
  );
}

export default Cart;