const THIRD_PARTY_API = "https://dummyjson.com/products?limit=3&select=id,title,price,category,thumbnail";

export async function getExternalProducts() {
  const response = await fetch(THIRD_PARTY_API, { headers: { Accept: "application/json" } });
  if (!response.ok) throw new Error(`API externa respondió HTTP ${response.status}.`);
  const data = await response.json();
  return data.products || [];
}
