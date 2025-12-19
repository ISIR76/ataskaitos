import createClient from "openapi-fetch";
import type { paths } from "./schema";

// Use relative URLs in production (same origin), localhost in dev
export const baseUrl = import.meta.env.VITE_API_BASE_URL || (import.meta.env.PROD ? "" : "http://localhost:8000");

// Create API client with base URL and CORS credentials
export const client = createClient<paths>({
  baseUrl,
  // Enable CORS credentials (cookies, authorization headers, TLS client certificates)
  credentials: "include",
});

// Add middleware to include auth token in all requests
client.use({
  onRequest({ request }) {
    const token = localStorage.getItem("ataskaitos_auth_token");
    if (token) {
      request.headers.set("Authorization", `Bearer ${token}`);
    }
    return request;
  },
});

// Helper functions for common operations
export const api = {
  // Get all evaluators
  getEvaluators: async () => {
    return client.GET("/api/v1/evaluators");
  },

  // Evaluate document
  evaluateDocument: async (
    file: File,
    documentType: "report" | "article",
    evaluationType: "scoring" | "agent" = "scoring",
    evaluators?: string,
    agents?: string
  ) => {
    // For multipart/form-data, openapi-fetch accepts an object with File
    // The generated types show file: string (binary format), but runtime accepts File
    return client.POST("/api/v1/evaluate", {
      body: {
        file: file as unknown as string, // Type: string (binary), Runtime: File
        document_type: documentType,
        evaluation_type: evaluationType,
        evaluators: evaluators,
        agents: agents,
      },
    });
  },

  // Get health status
  getHealth: async () => {
    return client.GET("/api/health");
  },

  // Get root info
  getRoot: async () => {
    return client.GET("/api/");
  },
};
