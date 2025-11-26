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
