import { useState, useEffect } from "react";
import { Link, useParams } from "react-router-dom";
import { API_BASE, getImageUrl } from "../apiConfig";

function ProductDetail() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE}/api/store/products/${id}/`)
      .then((response) => response.json())
      .then((data) => setProduct(data))
      .catch((error) => console.error("Error fetching product:", error));
  }, [id]);

  function addToCart() {
    const token = localStorage.getItem("accessToken");
    fetch(`${API_BASE}/api/cart/cart-items/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ product: id, quantity: 1 }),
    })
      .then((response) => response.json())
      .then(() => alert("Added to cart!"))
      .catch((error) => console.error("Error adding to cart:", error));
  }

  if (!product) return <p className="max-w-2xl mx-auto px-4 py-12 text-gray-600">Loading...</p>;

  const placeholderImage = `https://via.placeholder.com/960x720?text=${encodeURIComponent(product.name)}`;

  function getProductImage(productData) {
    return (
      getImageUrl(productData.images?.[0]?.image) ||
      getImageUrl(productData.image) ||
      placeholderImage
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-12">
      <Link to="/products" className="text-indigo-600 text-sm font-semibold hover:underline mb-6 inline-block">
        ← Back to Products
      </Link>
      <div className="grid grid-cols-1 lg:grid-cols-[1.3fr_0.9fr] gap-10 items-start">
        <div>
          <div className="w-full h-[28rem] rounded-3xl overflow-hidden bg-gray-100 mb-6">
            <img
              src={getProductImage(product)}
              alt={product.name}
              className="w-full h-full object-cover"
            />
          </div>
        </div>

        <div className="space-y-6">
          <div>
            <h1 className="text-4xl font-bold text-gray-900 mb-4">{product.name}</h1>
            <p className="text-3xl font-semibold text-indigo-600">৳{product.price}</p>
            {product.compare_price && product.compare_price > product.price && (
              <p className="text-sm text-gray-500 line-through mt-2">৳{product.compare_price}</p>
            )}
          </div>

          <div className="rounded-3xl border border-gray-200 bg-white p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Product Details</h2>
            <p className="text-gray-700 whitespace-pre-line">{product.description || "No description available."}</p>
          </div>

          <div className="flex flex-col gap-4">
            <button
              onClick={addToCart}
              className="w-full bg-indigo-600 text-white px-6 py-4 rounded-3xl font-semibold hover:bg-indigo-700 transition"
            >
              Add to Cart
            </button>
            <div className="rounded-3xl border border-gray-200 bg-gray-50 p-4">
              <p className="text-sm text-gray-600">Stock: {product.stock ?? "N/A"}</p>
              <p className="text-sm text-gray-600">Category ID: {product.category || "N/A"}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProductDetail;
