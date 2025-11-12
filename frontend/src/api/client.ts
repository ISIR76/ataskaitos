import createClient from "openapi-fetch";
import type { paths } from "./schema";

const baseUrl = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

console.log("API Base URL:", baseUrl);

// Create API client with base URL
export const client = createClient<paths>({
  baseUrl,
});

// Helper functions for common operations
export const api = {
  // Get all evaluators
  getEvaluators: async (params?: { evaluation_name?: string }) => {
    return client.GET("/api/v1/evaluators",
      params ? { params: { query: params } } : undefined
    );
  },

  // Evaluate document
  evaluateDocument: async (
    file: File,
    documentType: "report" | "article",
    evaluationType: "scoring" | "agent" = "scoring"
  ) => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("document_type", documentType);
    formData.append("evaluation_type", evaluationType);

    return client.POST("/api/v1/evaluate", {
      body: formData,
      bodySerializer: (body) => body as FormData,
    });
  },

  // Get health status
  getHealth: async () => {
    return client.GET("/health");
  },

  // Get root info
  getRoot: async () => {
    return client.GET("/");
  },
};
