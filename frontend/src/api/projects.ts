import { client, baseUrl } from "./client";
import type { components } from "./schema";

// Use generated schema types instead of custom types
export type Project = components["schemas"]["ProjectResponse"];
export type ProjectDetail = components["schemas"]["ProjectResponse"];
export type DocumentVersion = components["schemas"]["DocumentVersionResponse"];
export type EvaluationItem = components["schemas"]["EvaluationHistoryItem"];
export type EvaluationDetail = components["schemas"]["EvaluationDetailResponse"];
export type ScoresGrid = components["schemas"]["ScoresGridResponse"];
export type ScoresGridRow = components["schemas"]["ScoresGridRow"];

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
export async function fetchProjectVersions(projectId: number): Promise<DocumentVersion[]> {
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
export async function fetchVersionEvaluations(projectId: number, versionId: number): Promise<EvaluationItem[]> {
  const response = await client.GET("/api/v1/projects/{project_id}/versions/{version_id}/evaluations", {
    params: { path: { project_id: projectId, version_id: versionId } },
  });
  if (!response.data) {
    throw new Error("Nepavyko įkelti vertinimų");
  }
  return response.data as EvaluationItem[];
}

/**
 * Create a new project
 */
export async function createProject(name: string, projectType: "straipsnis" | "ataskaita"): Promise<void> {
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
 * Fetch the cross-project scoring grid for a given document type.
 */
export async function fetchScoresGrid(
  documentType: "article" | "report" = "article"
): Promise<ScoresGrid> {
  const response = await client.GET("/api/v1/projects/scores-grid", {
    params: { query: { document_type: documentType } },
  });
  if (!response.data) {
    throw new Error("Nepavyko įkelti vertinimų lentelės");
  }
  return response.data as ScoresGrid;
}

/**
 * Toggle the manual quality-verified flag on a project.
 */
export async function setProjectMarkedGood(projectId: number, value: boolean): Promise<Project> {
  const response = await client.PATCH("/api/v1/projects/{project_id}/marked-good", {
    params: { path: { project_id: projectId } },
    body: { value },
  });
  if (!response.data) {
    throw new Error("Nepavyko atnaujinti projekto žymėjimo");
  }
  return response.data as Project;
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
export async function setActiveVersion(projectId: number, versionId: number): Promise<void> {
  const response = await client.POST("/api/v1/projects/{project_id}/versions/{version_id}/set-active", {
    params: { path: { project_id: projectId, version_id: versionId } },
  });

  if (response.error) {
    throw new Error("Nepavyko nustatyti aktyvios versijos");
  }
}

/**
 * Upload a new version
 */
export async function uploadVersion(projectId: number, file: File): Promise<void> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${baseUrl}/api/v1/projects/${projectId}/versions`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Nepavyko įkelti versijos: ${response.statusText}`);
  }
}

/**
 * Run evaluation on a version
 * Returns the evaluation ID for navigation to results
 */
export async function runEvaluation(
  projectId: number,
  versionId: number,
  evaluationType: "scoring" | "agent",
  evaluators: string[]
): Promise<string> {
  const formData = new FormData();
  formData.append("evaluation_type", evaluationType);

  // Pass evaluators for scoring mode, agents for agent mode
  if (evaluationType === "scoring") {
    formData.append("evaluators", evaluators.join(","));
  } else {
    formData.append("agents", evaluators.join(","));
  }

  const response = await fetch(`${baseUrl}/api/v1/projects/${projectId}/versions/${versionId}/evaluate`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Nepavyko paleisti vertinimo: ${response.statusText}`);
  }

  const data = await response.json();
  return data.evaluation_id;
}

/**
 * Run the dedicated LLM-detection agent on a version.
 * Returns the evaluation ID for navigation to results.
 */
export async function runLlmDetection(
  projectId: number,
  versionId: number
): Promise<string> {
  const headers: Record<string, string> = {};
  const token = localStorage.getItem("ataskaitos_auth_token");
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  const response = await fetch(
    `${baseUrl}/api/v1/projects/${projectId}/versions/${versionId}/llm-detect`,
    { method: "POST", headers }
  );
  if (!response.ok) {
    const text = await response.text();
    throw new Error(`AI tikrinimas nepavyko: ${text || response.statusText}`);
  }
  const data = await response.json();
  return data.evaluation_id;
}

/**
 * Fetch evaluation details by UUID
 */
export async function fetchEvaluation(projectId: number, evaluationId: string): Promise<EvaluationDetail> {
  const response = await client.GET("/api/v1/projects/{project_id}/evaluations/{evaluation_id}", {
    params: { path: { project_id: projectId, evaluation_id: evaluationId } },
  });
  if (!response.data) {
    throw new Error("Vertinimas nerastas");
  }
  return response.data as EvaluationDetail;
}
