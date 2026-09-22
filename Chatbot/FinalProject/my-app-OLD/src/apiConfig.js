export const API_BASE = import.meta.env.VITE_API_BASE || "";

export function getAuthHeaders() {
  const token = localStorage.getItem("accessToken");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export function getJsonHeaders() {
  return {
    "Content-Type": "application/json",
    ...getAuthHeaders(),
  };
}

export function getImageUrl(image) {
  if (!image || typeof image !== "string") return "";

  if (image.startsWith("http://") || image.startsWith("https://") || image.startsWith("data:")) {
    return image;
  }

  const normalizedPath = image.startsWith("/") ? image.slice(1) : image;
  const base = API_BASE ? API_BASE.replace(/\/$/, "") : "";

  if (normalizedPath.startsWith("media/")) {
    return base ? `${base}/${normalizedPath}` : `/${normalizedPath}`;
  }

  return base ? `${base}/media/${normalizedPath}` : `/media/${normalizedPath}`;
}
