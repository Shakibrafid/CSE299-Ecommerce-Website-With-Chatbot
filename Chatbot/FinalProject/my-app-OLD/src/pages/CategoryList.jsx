import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { API_BASE, getImageUrl } from "../apiConfig";

function CategoryList() {
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    fetch(`${API_BASE}/api/store/categories/`)
      .then((response) => response.json())
      .then((data) => setCategories(data))
      .catch((error) => {
        console.error("Error fetching categories:", error);
        setCategories([
          { id: 1, name: "Clothing", description: "Fashion and apparel." },
          { id: 2, name: "Electronics", description: "Latest devices and gadgets." },
          { id: 3, name: "Home Goods", description: "Essentials for every room." },
        ]);
      });
  }, []);

  return (
    <div className="bg-white min-h-screen">
      <div className="bg-gray-950 py-16">
        <div className="max-w-6xl mx-auto px-6">
          <p className="text-indigo-400 font-semibold text-sm uppercase tracking-wide mb-2">Browse</p>
          <h1 className="text-4xl font-bold text-white">Categories</h1>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-16">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-8">
          {categories.map((category) => (
            <Link
              key={category.id}
              to={`/categories/${category.id}`}
              className="group overflow-hidden rounded-3xl border border-gray-200 shadow-sm bg-white transition hover:-translate-y-1"
            >
              <div className="w-full h-56 overflow-hidden bg-gray-100">
                {category.image ? (
                  <img
                    src={getImageUrl(category.image)}
                    alt={category.name}
                    className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
                  />
                ) : (
                  <div className="w-full h-full bg-gradient-to-br from-indigo-600 to-violet-600" />
                )}
              </div>
              <div className="p-6">
                <h3 className="text-2xl font-semibold text-gray-900 mb-2">{category.name}</h3>
                <p className="text-sm text-gray-600">
                  {category.description || "Explore products from this category."}
                </p>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}

export default CategoryList;
