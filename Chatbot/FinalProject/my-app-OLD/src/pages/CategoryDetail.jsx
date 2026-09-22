import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { API_BASE, getImageUrl } from "../apiConfig";

function CategoryDetail() {
  const { id } = useParams();
  const [category, setCategory] = useState(null);
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetch(`${API_BASE}/api/store/categories/${id}/`)
      .then((response) => response.json())
      .then((data) => setCategory(data))
      .catch((error) => {
        console.error("Error fetching category:", error);
        setCategory(null);
      });
  }, [id]);

  useEffect(() => {
    fetch(`${API_BASE}/api/store/products/?category=${id}`)
      .then((response) => response.json())
      .then((data) => setProducts(data))
      .catch((error) => {
        console.error("Error fetching category products:", error);
        setProducts([]);
      });
  }, [id]);

  function getProductImage(product) {
    return (
      getImageUrl(product.image) ||
      getImageUrl(product.images?.[0]?.image) ||
      `https://via.placeholder.com/640x480?text=${encodeURIComponent(product.name)}`
    );
  }

  function addToCart(product) {
    const token = localStorage.getItem("accessToken");
    fetch(`${API_BASE}/api/cart/cart-items/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ product: product.id, quantity: 1 }),
    })
      .then((response) => response.json())
      .then(() => alert(`${product.name} added to cart!`))
      .catch((error) => console.error("Error adding to cart:", error));
  }

  return (
    <div className="bg-white min-h-screen">
      <div className="bg-gray-950 py-16">
        <div className="max-w-6xl mx-auto px-6">
          <Link to="/categories" className="text-indigo-400 text-sm font-semibold hover:underline mb-2 inline-block">
            ← Back to Categories
          </Link>
          <h1 className="text-4xl font-bold text-white">{category?.name || "Category Products"}</h1>
          {category?.description && (
            <p className="mt-4 max-w-3xl text-gray-300">{category.description}</p>
          )}
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-16">
        {products.length === 0 ? (
          <p className="text-gray-500 text-center py-16">No products in this category.</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-8">
            {products.map((product) => (
              <div key={product.id} className="group bg-white rounded-3xl border border-gray-200 shadow-sm overflow-hidden">
                <Link to={`/products/${product.id}`}>
                  <div className="w-full h-56 overflow-hidden bg-gray-100">
                    <img
                      src={getProductImage(product)}
                      alt={product.name}
                      className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
                    />
                  </div>
                </Link>
                <div className="p-6">
                  <Link to={`/products/${product.id}`}>
                    <h3 className="font-semibold text-gray-900 group-hover:text-indigo-600 transition mb-2">
                      {product.name}
                    </h3>
                  </Link>
                  <p className="text-sm text-gray-600 mb-4 min-h-[3rem]">
                    {product.description || "No description available."}
                  </p>
                  <div className="flex items-center justify-between gap-4">
                    <p className="text-gray-900 font-bold">৳{product.price}</p>
                    <button
                      onClick={() => addToCart(product)}
                      className="text-sm font-semibold bg-gray-900 text-white px-4 py-2 rounded-full hover:bg-indigo-600 transition"
                    >
                      Add to Cart
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default CategoryDetail;
