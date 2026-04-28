import { client } from "./client";
import type { components } from "./schema";

export type EvaluatorRecord = components["schemas"]["EvaluatorRecord"];
export type EvaluatorCreate = components["schemas"]["EvaluatorCreate"];
export type EvaluatorUpdate = components["schemas"]["EvaluatorUpdate"];

export type DocumentType = "article" | "report";

export async function fetchEvaluators(
  documentType?: DocumentType,
  onlyActive = false
): Promise<EvaluatorRecord[]> {
  const response = await client.GET("/api/v1/evaluators-admin", {
    params: {
      query: {
        document_type: documentType,
        only_active: onlyActive,
      },
    },
  });
  if (!response.data) {
    throw new Error("Nepavyko įkelti vertintojų");
  }
  return response.data as EvaluatorRecord[];
}

export async function createEvaluator(
  payload: EvaluatorCreate
): Promise<EvaluatorRecord> {
  const response = await client.POST("/api/v1/evaluators-admin", {
    body: payload,
  });
  if (!response.data) {
    const detail =
      (response.error as { detail?: string } | undefined)?.detail ??
      "Nepavyko sukurti vertintojo";
    throw new Error(detail);
  }
  return response.data as EvaluatorRecord;
}

export async function updateEvaluator(
  evaluatorId: number,
  payload: EvaluatorUpdate
): Promise<EvaluatorRecord> {
  const response = await client.PATCH("/api/v1/evaluators-admin/{evaluator_id}", {
    params: { path: { evaluator_id: evaluatorId } },
    body: payload,
  });
  if (!response.data) {
    const detail =
      (response.error as { detail?: string } | undefined)?.detail ??
      "Nepavyko atnaujinti vertintojo";
    throw new Error(detail);
  }
  return response.data as EvaluatorRecord;
}

export async function setEvaluatorActive(
  evaluatorId: number,
  isActive: boolean
): Promise<EvaluatorRecord> {
  const response = await client.PATCH(
    "/api/v1/evaluators-admin/{evaluator_id}/active",
    {
      params: { path: { evaluator_id: evaluatorId } },
      body: { is_active: isActive },
    }
  );
  if (!response.data) {
    throw new Error("Nepavyko pakeisti būsenos");
  }
  return response.data as EvaluatorRecord;
}

export async function deleteEvaluator(evaluatorId: number): Promise<void> {
  const response = await client.DELETE(
    "/api/v1/evaluators-admin/{evaluator_id}",
    {
      params: { path: { evaluator_id: evaluatorId } },
    }
  );
  if (response.error) {
    const detail =
      (response.error as { detail?: string } | undefined)?.detail ??
      "Nepavyko ištrinti vertintojo";
    throw new Error(detail);
  }
}
