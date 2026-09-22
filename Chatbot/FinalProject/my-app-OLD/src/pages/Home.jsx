function Home() {
  const featuredProducts = [
    { id: 1, name: "Product 1", price: 10.99 },
    { id: 2, name: "Product 2", price: 15.99 },
    { id: 3, name: "Product 3", price: 20.99 },
  ];

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
            <div key={product.id} className="group cursor-pointer">
              <div className="w-full h-56 bg-gradient-to-br from-gray-100 to-gray-200 rounded-3xl mb-4 overflow-hidden relative">
                <div className="absolute inset-0 bg-gray-900/0 group-hover:bg-gray-900/5 transition"></div>
              </div>
              <div className="flex items-center justify-between">
                <h3 className="font-semibold text-gray-900 group-hover:text-indigo-600 transition">{product.name}</h3>
                <p className="text-gray-900 font-bold">৳{product.price.toFixed(2)}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Home;