const API_URL = "http://127.0.0.1:8000/products";

async function apiRequest(url, method, data = null) {
  const options = {
    method,
    headers: { "Content-Type": "application/json" }
  };

  if (data) options.body = JSON.stringify(data);

  const res = await fetch(url, options);
  const result = await res.json();

  if (!res.ok) throw result;
  return result;
}
