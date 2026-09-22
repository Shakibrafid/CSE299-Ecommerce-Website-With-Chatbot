import { useState, useEffect } from "react";
import { API_BASE, getImageUrl } from "../apiConfig";

function Home() {
  const [featuredProducts, setFeaturedProducts] = useState([
   
  ]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/api/store/products/`)
      .then((response) => response.json())
      .then((data) => {
        const products = Array.isArray(data) ? data : [];
        const featured = products.filter((product) => product.is_featured);
        setFeaturedProducts(featured.length ? featured : products.slice(0, 3));
      })
      .catch((error) => {
        console.error("Error fetching featured products:", error);
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="bg-white">
      {/* Hero */}
      <div className="relative overflow-hidden bg-gray-950">
        <div className="absolute top-[-150px] right-[-100px] w-[500px] h-[500px] bg-indigo-600 rounded-full blur-3xl opacity-30"></div>
        <div className="absolute bottom-[-150px] left-[-150px] w-[400px] h-[400px] bg-purple-600 rounded-full blur-3xl opacity-20"></div>

        <div className="relative max-w-6xl mx-auto px-6 py-32 grid md:grid-cols-2 gap-12 items-center">
          <div>
            <span className="inline-flex items-center gap-2 bg-white/10 text-indigo-300 text-xs font-semibold tracking-wide uppercase px-4 py-1.5 rounded-full mb-8 border border-white/10">
              ✦ New arrivals every week
            </span>
            <h1 className="text-6xl font-bold text-white leading-[1.05] mb-6 tracking-tight">
              Shop smarter.
              <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">
                Live better.
              </span>
            </h1>
            <p className="text-lg text-gray-400 max-w-md mb-10 leading-relaxed">
              Curated picks, honest prices, and fast delivery — everything you need, nothing you don't.
            </p>
            <div className="flex gap-4">
              <a href="/products" className="bg-white text-gray-950 px-8 py-3.5 rounded-full font-semibold hover:bg-gray-100 transition">
                Shop Now
              </a>
              <a href="/categories" className="border border-white/20 text-white px-8 py-3.5 rounded-full font-semibold hover:bg-white/10 transition">
                Browse Categories
              </a>
            </div>
          </div>
          <div className="hidden md:grid grid-cols-2 gap-4">
            <div className="h-48 bg-white/5 border border-white/10 rounded-3xl mt-8 backdrop-blur-sm"></div>
            <div className="h-48 bg-gradient-to-br from-indigo-500/30 to-purple-500/30 border border-white/10 rounded-3xl backdrop-blur-sm"></div>
            <div className="h-48 bg-gradient-to-br from-purple-500/30 to-pink-500/30 border border-white/10 rounded-3xl backdrop-blur-sm"></div>
            <div className="h-48 bg-white/5 border border-white/10 rounded-3xl mt-8 backdrop-blur-sm"></div>
          </div>
        </div>
      </div>

      {/* Featured products */}
      <div className="max-w-6xl mx-auto px-6 py-24">
        <div className="flex items-end justify-between mb-12">
          <div>
            <p className="text-indigo-600 font-semibold text-sm uppercase tracking-wide mb-2">Handpicked</p>
            <h2 className="text-3xl font-bold text-gray-900">Featured Products</h2>
          </div>
          <a href="/products" className="text-sm font-semibold text-gray-600 hover:text-indigo-600 transition">
            View all →
          </a>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-8">
          {featuredProducts.map((product) => (
            <div key={product.id} className="group cursor-pointer bg-white rounded-3xl border border-gray-200 shadow-sm overflow-hidden">
              <div className="w-full h-56 rounded-3xl mb-4 overflow-hidden bg-gray-100 relative">
                {product.images?.[0]?.image ? (
                  <img
                    src={getImageUrl(product.images[0].image)}
                    alt={product.name}
                    className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
                  />
                ) : product.image ? (
                  <img
                    src={getImageUrl(product.image)}
                    alt={product.name}
                    className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
                  />
                ) : (
                  <div className="absolute inset-0 bg-gradient-to-br from-indigo-600 to-violet-600" />
                )}
              </div>
              <div className="p-4">
                <h3 className="font-semibold text-gray-900 group-hover:text-indigo-600 transition mb-2">{product.name}</h3>
                <p className="text-sm text-gray-600 mb-4">{product.description || "No description available."}</p>
                <div className="flex items-center justify-between">
                  <p className="text-gray-900 font-bold">৳{Number(product.price).toFixed(2)}</p>
                  <a href={`/products/${product.id}`} className="text-sm font-semibold text-indigo-600 hover:text-indigo-700 transition">
                    View
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Home;