const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

export async function checkBackendHealth() {
  const response = await fetch(`${API_BASE_URL}/api/v1/system/health`);

  if (!response.ok) {
    throw new Error(`Backend request failed: ${response.status}`);
  }

  return response.json();
}

export async function analyzeCareer(profile) {
  const response = await fetch(`${API_BASE_URL}/api/v1/career/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(profile),
  });

  if (!response.ok) {
    throw new Error(`Career analysis failed: ${response.status}`);
  }

  return response.json();
}
