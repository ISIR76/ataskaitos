import { client } from "./client";
import type { components } from "./schema";

export type Project = {
  id: number;
  name: string;
  project_type: string;
  active_version_number: number | null;
  total_versions: number;
  created_at: string;
};

export type ProjectDetail = {
  id: number;
  name: string;
  project_type: string;
  active_version_id: number | null;
  total_versions: number;
};

export type DocumentVersion = {
  id: number;
  version_number: number;
  original_filename: string;
  character_count: number;
  evaluation_count: number;
  is_active: boolean;
  created_at: string;
};

export type EvaluationItem = {
  id: number;
  evaluation_id: string;
  evaluation_type: string;
  evaluators_used: string[];
  status: string;
  duration_seconds: number;
  created_at: string;
};

export type EvaluationDetail = components["schemas"]["EvaluationDetailResponse"];

/**
 * Fetch all projects
 */
export async function fetchProjects(): Promise<Project[]> {
  const response = await client.GET("/api/v1/projects");
  if (!response.data) {
    throw new Error("Nepavyko įkelti projektų");
  }
  return response.data.projects as Project[];
}

/**
 * Fetch a single project by ID
 */
export async function fetchProject(projectId: number): Promise<ProjectDetail> {
  const response = await client.GET("/api/v1/projects/{project_id}", {
    params: { path: { project_id: projectId } },
  });
  if (!response.data) {
    throw new Error("Projektas nerastas");
  }
  return response.data as ProjectDetail;
}

/**
 * Fetch project versions
 */
export async function fetchProjectVersions(
  projectId: number
): Promise<DocumentVersion[]> {
  const response = await client.GET("/api/v1/projects/{project_id}/versions", {
    params: { path: { project_id: projectId } },
  });
  if (!response.data) {
    throw new Error("Nepavyko įkelti versijų");
  }
  return response.data as DocumentVersion[];
}

/**
 * Fetch evaluations for a specific version
 */
export async function fetchVersionEvaluations(
  projectId: number,
  versionId: number
): Promise<EvaluationItem[]> {
  const response = await client.GET(
    "/api/v1/projects/{project_id}/versions/{version_id}/evaluations",
    {
      params: { path: { project_id: projectId, version_id: versionId } },
    }
  );
  if (!response.data) {
    throw new Error("Nepavyko įkelti vertinimų");
  }
  return response.data as EvaluationItem[];
}

/**
 * Create a new project
 */
export async function createProject(
  name: string,
  projectType: "straipsnis" | "ataskaita"
): Promise<void> {
  const response = await client.POST("/api/v1/projects", {
    body: {
      name,
      project_type: projectType,
    },
  });

  if (!response.data) {
    throw new Error("Nepavyko sukurti projekto. Pavadinimas gali jau egzistuoti.");
  }
}

/**
 * Delete a project
 */
export async function deleteProject(projectId: number): Promise<void> {
  const response = await client.DELETE("/api/v1/projects/{project_id}", {
    params: { path: { project_id: projectId } },
  });

  if (response.error) {
    throw new Error("Nepavyko ištrinti projekto");
  }
}

/**
 * Set a version as active
 */
export async function setActiveVersion(
  projectId: number,
  versionId: number
): Promise<void> {
  const response = await client.POST(
    "/api/v1/projects/{project_id}/versions/{version_id}/set-active",
    {
      params: { path: { project_id: projectId, version_id: versionId } },
    }
  );

  if (response.error) {
    throw new Error("Nepavyko nustatyti aktyvios versijos");
  }
}

/**
 * Upload a new version
 */
export async function uploadVersion(
  projectId: number,
  file: File
): Promise<void> {
  const formData = new FormData();
  formData.append("file", file);

  // Use same URL logic as client.ts: relative URL in production, localhost in dev
  const baseUrl = import.meta.env.VITE_API_BASE_URL ||
    (import.meta.env.PROD ? "" : "http://localhost:8000");
  const response = await fetch(
    `${baseUrl}/api/v1/projects/${projectId}/versions`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {
    throw new Error(`Nepavyko įkelti versijos: ${response.statusText}`);
  }
}

/**
 * Fetch evaluation details by UUID
 */
export async function fetchEvaluation(
  projectId: number,
  evaluationId: string
): Promise<EvaluationDetail> {
  const response = await client.GET(
    "/api/v1/projects/{project_id}/evaluations/{evaluation_id}",
    {
      params: { path: { project_id: projectId, evaluation_id: evaluationId } },
    }
  );
  if (!response.data) {
    throw new Error("Vertinimas nerastas");
  }
  return response.data as EvaluationDetail;
}
