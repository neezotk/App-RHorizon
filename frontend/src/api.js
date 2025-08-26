export function apiBaseUrl() {
  const url = import.meta.env.VITE_API_BASE_URL || window.location.origin;
  return url.replace(/\/$/, "");
}
export async function getHello() {
  const res = await fetch(`${apiBaseUrl()}/api`);
  return res.json();
}
export async function getHealth() {
  const res = await fetch(`${apiBaseUrl()}/api/health`);
  return res.json();
}
