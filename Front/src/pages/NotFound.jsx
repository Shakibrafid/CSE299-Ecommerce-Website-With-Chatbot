import { Link } from "react-router-dom";

function NotFound() {
  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center px-6">
      <div className="text-center">
        <p className="text-indigo-400 font-semibold text-sm uppercase tracking-wide mb-4">Error</p>
        <h1 className="text-8xl font-bold text-white mb-4">404</h1>
        <p className="text-gray-400 mb-8">The page you're looking for doesn't exist.</p>
        <Link to="/" className="inline-block bg-white text-gray-950 px-8 py-3 rounded-full font-semibold hover:bg-gray-100 transition">
          Go back home
        </Link>
      </div>
    </div>
  );
}

export default NotFound;