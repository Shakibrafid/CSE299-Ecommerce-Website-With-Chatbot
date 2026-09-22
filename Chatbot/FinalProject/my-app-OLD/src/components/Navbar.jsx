import { Link, useNavigate } from "react-router-dom";

function Navbar() {
    const navigate = useNavigate();
    const isLoggedIn = !!localStorage.getItem("accessToken");

    function handleLogout() {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        navigate("/login");
    }

    return (
        <nav className="sticky top-0 z-50 backdrop-blur-md bg-white/80 border-b border-gray-200">
            <div className="max-w-6xl mx-auto flex items-center justify-between px-6 py-4">
                <Link to="/" className="text-xl font-bold text-gray-900">
                    Shop<span className="text-indigo-600">Sphere</span>
                </Link>
                <div className="flex items-center gap-6 text-sm font-medium text-gray-600">
                    <Link to="/products" className="hover:text-indigo-600 transition">Products</Link>
                    <Link to="/categories" className="hover:text-indigo-600 transition">Categories</Link>
                    <Link to="/orders" className="hover:text-indigo-600 transition">Orders</Link>
                    <Link to="/chat" className="hover:text-indigo-600 transition">Chat</Link>
                    <Link to="/cart" className="hover:text-indigo-600 transition">Cart</Link>
                    <Link to="/profile" className="hover:text-indigo-600 transition">Profile</Link>
                </div>
                <div className="flex items-center gap-3">
                    {isLoggedIn ? (
                        <button onClick={handleLogout} className="text-sm font-semibold text-gray-600 hover:text-red-600 transition">
                            Logout
                        </button>
                    ) : (
                        <>
                            <Link to="/login" className="text-sm font-medium text-gray-600 hover:text-indigo-600 transition">Login</Link>
                            <Link to="/register" className="text-sm font-semibold bg-indigo-600 text-white px-4 py-2 rounded-full hover:bg-indigo-700 transition">
                                Register
                            </Link>
                        </>
                    )}
                </div>
            </div>
        </nav>
    )
}

export default Navbar