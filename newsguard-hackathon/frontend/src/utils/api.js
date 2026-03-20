import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

/**
 * Analyze news for multiple independent checks:
 * - Fake/Real news classification (MAIN - always performed)
 * - URL domain credibility (optional)
 * 
 * @param {string} text - Article text to analyze
 * @param {string} mode - Analysis mode: "transformer" | "ensemble" | "hybrid"
 * @param {string} url - Optional URL for domain verification
 * @param {boolean} checkUrl - Whether to verify URL credibility
 * @returns {object} Analysis results with separate sections for each feature
 */
export async function analyzeNews(text, mode, url = "", checkUrl = false) {
  try {
    console.log("DEBUG: API_BASE_URL =", API_BASE_URL);
    console.log("📤 Analyzing news article...");
    console.log("   - Features: fake_news=✓, url=" + (checkUrl ? "✓" : "✗"));
    
    const response = await client.post("/api/analyze", { 
      text, 
      mode, 
      url, 
      check_url: checkUrl
    });
    
    console.log("✅ Analysis complete");
    return response.data;
  } catch (error) {
    console.error("❌ Analysis failed");
    console.error("   Error type:", error.constructor.name);
    console.error("   Error message:", error.message);
    console.error("   Error stack:", error.stack);
    console.error("   Response status:", error?.response?.status);
    console.error("   Response data:", error?.response?.data);
    console.error("   Error config:", { 
      url: error?.config?.url,
      method: error?.config?.method,
      baseURL: error?.config?.baseURL
    });
    const message =
      error?.response?.data?.error ||
      "Unable to analyze the news right now. Please try again.";
    throw new Error(message);
  }
}

export async function fetchModels() {
  try {
    const response = await client.get("/api/models");
    return response.data?.models || [];
  } catch (error) {
    console.error("❌ Error fetching models:", error.message);
    return [];
  }
}
