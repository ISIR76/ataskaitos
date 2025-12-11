import { createFileRoute, Link } from "@tanstack/react-router";
import { fetchProject, fetchEvaluation } from "../api/projects";
import { EvaluationResults } from "../components/EvaluationResults";
import type { components } from "../api/schema";

type UnifiedEvaluationResponse =
  components["schemas"]["UnifiedEvaluationResponse"];

export const Route = createFileRoute(
  "/projects/$projectId/evaluations/$evaluationId"
)({
  loader: async ({ params }) => {
    console.log("🔄 Evaluation loader called with params:", params);
    const projectId = parseInt(params.projectId);
    const evaluationId = params.evaluationId;

    console.log("📡 Fetching project and evaluation...", { projectId, evaluationId });

    // Fetch project and evaluation in parallel
    const [project, evaluation] = await Promise.all([
      fetchProject(projectId),
      fetchEvaluation(projectId, evaluationId),
    ]);

    console.log("✅ Fetched data:", { project, evaluation });

    // Transform EvaluationDetailResponse to UnifiedEvaluationResponse
    const unifiedResult: UnifiedEvaluationResponse = {
      evaluation_id: evaluation.evaluation_id,
      document_type:
        project.project_type === "straipsnis" ? "article" : "report",
      evaluation_type: evaluation.evaluation_type,
      status: evaluation.status,
      results: evaluation.results,
      metadata: {
        evaluators_used: evaluation.evaluators_used,
        duration_seconds: evaluation.duration_seconds,
        created_at: evaluation.created_at,
      },
    };

    console.log("🎯 Transformed result:", unifiedResult);

    return { project, unifiedResult };
  },
  component: EvaluationResultsPage,
  pendingComponent: () => (
    <div className="container mx-auto p-8">
      <div className="text-center">Įkeliami vertinimo rezultatai...</div>
    </div>
  ),
  errorComponent: ({ error }) => {
    console.error("❌ Error in evaluation route:", error);
    return (
      <div className="container mx-auto p-8">
        <div className="text-center text-red-600">
          Klaida įkeliant vertinimą: {error.message}
        </div>
        <pre className="mt-4 text-xs">{error.stack}</pre>
      </div>
    );
  },
});

function EvaluationResultsPage() {
  const { project, unifiedResult } = Route.useLoaderData();

  console.log("🎨 Rendering EvaluationResultsPage with:", { project, unifiedResult });

  return (
    <div className="container mx-auto p-8">
      <div className="mb-6">
        <Link
          to="/projects/$projectId"
          params={{ projectId: String(project.id) }}
          className="text-blue-600 hover:text-blue-800 mb-4 inline-block"
        >
          ← Atgal į projektą
        </Link>
        <h1 className="text-3xl font-bold mb-2">{project.name}</h1>
        <p className="text-muted-foreground">
          Vertinimo rezultatai - {project.project_type}
        </p>
      </div>

      <EvaluationResults result={unifiedResult} />
    </div>
  );
}
