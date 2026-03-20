import { useEffect, useState } from "react";

export default function Debug() {
  const [apiUrl, setApiUrl] = useState("");

  useEffect(() => {
    const url = import.meta.env.VITE_API_URL || "http://localhost:5000";
    setApiUrl(url);
  }, []);

  return (
    <div style={{ padding: "20px", fontFamily: "monospace" }}>
      <h1>Debug Page</h1>
      <p>API Base URL: <strong>{apiUrl}</strong></p>
      <p>Environment variables:</p>
      <pre>
        {JSON.stringify(
          {
            VITE_API_URL: import.meta.env.VITE_API_URL,
            MODE: import.meta.env.MODE,
            DEV: import.meta.env.DEV,
            PROD: import.meta.env.PROD,
          },
          null,
          2
        )}
      </pre>
    </div>
  );
}
