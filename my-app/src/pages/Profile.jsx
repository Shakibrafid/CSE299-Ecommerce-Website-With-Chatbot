import { useState } from "react";

function Profile() {
  const [addressLine1, setAddressLine1] = useState("");
  const [addressLine2, setAddressLine2] = useState("");
  const [city, setCity] = useState("");
  const [state, setState] = useState("");
  const [postalCode, setPostalCode] = useState("");
  const [country, setCountry] = useState("");
  const inputClass = "w-full border border-gray-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition";
  const labelClass = "block text-sm font-semibold text-gray-700 mb-1.5";

  function handleSubmit(e) {
    e.preventDefault();
    console.log("Profile saved:", { addressLine1, addressLine2, city, state, postalCode, country });
  }

  return (
    <div className="bg-white min-h-screen">
      <div className="bg-gray-950 py-16">
        <div className="max-w-2xl mx-auto px-6">
          <p className="text-indigo-400 font-semibold text-sm uppercase tracking-wide mb-2">Your Account</p>
          <h1 className="text-4xl font-bold text-white">Profile</h1>
        </div>
      </div>

      <div className="max-w-2xl mx-auto px-6 py-16">
        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className={labelClass}>Address Line 1</label>
            <input type="text" value={addressLine1} onChange={(e) => setAddressLine1(e.target.value)} className={inputClass} required />
          </div>
          <div>
            <label className={labelClass}>Address Line 2</label>
            <input type="text" value={addressLine2} onChange={(e) => setAddressLine2(e.target.value)} className={inputClass} />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className={labelClass}>City</label>
              <input type="text" value={city} onChange={(e) => setCity(e.target.value)} className={inputClass} required />
            </div>
            <div>
              <label className={labelClass}>State</label>
              <input type="text" value={state} onChange={(e) => setState(e.target.value)} className={inputClass} required />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className={labelClass}>Postal Code</label>
              <input type="text" value={postalCode} onChange={(e) => setPostalCode(e.target.value)} className={inputClass} required />
            </div>
            <div>
              <label className={labelClass}>Country</label>
              <input type="text" value={country} onChange={(e) => setCountry(e.target.value)} className={inputClass} required />
            </div>
          </div>
          <button type="submit" className="w-full bg-gray-950 text-white py-4 rounded-full font-semibold hover:bg-indigo-600 transition mt-2">
            Save Profile
          </button>
        </form>
      </div>
    </div>
  );
}

export default Profile;