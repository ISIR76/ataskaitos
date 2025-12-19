import { createFileRoute, Link, Outlet, useMatches, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { Upload, FileText } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { RunEvaluationModal } from "../../components/RunEvaluationModal";
import { UploadVersionDialog } from "../../components/UploadVersionDialog";
import { VersionsList } from "../../components/VersionsList";
import {
  fetchProject,
  fetchProjectVersions,
  fetchVersionEvaluations,
  uploadVersion,
  setActiveVersion,
  type EvaluationItem,
} from "../../api/projects";
import { useRouterMutation, useDialog, useExpandableData } from "@/hooks";

export const Route = createFileRoute("/projects/$projectId")({
  loader: async ({ params }) => {
    const projectId = parseInt(params.projectId);
    const [project, versions] = await Promise.all([
      fetchProject(projectId),
      fetchProjectVersions(projectId),
    ]);
    return { project, versions, projectId };
  },
  component: ProjectDetailPage,
  pendingComponent: () => (
    <div className="container mx-auto p-8">
      <div className="text-center">Įkeliamas projektas...</div>
    </div>
  ),
  errorComponent: ({ error }) => (
    <div className="container mx-auto p-8">
      <div className="text-center text-destructive">
        Klaida įkeliant projektą: {error.message}
      </div>
    </div>
  ),
});

function ProjectDetailPage() {
  const { project, versions, projectId } = Route.useLoaderData();
  const matches = useMatches();
  const navigate = useNavigate();

  // Check if we're on a child route (e.g., evaluation results page)
  const isOnChildRoute = matches.some(match =>
    match.id.includes('/evaluations/')
  );

  const uploadDialog = useDialog();
  const evaluationDialog = useDialog();
  const [evaluatingVersionId, setEvaluatingVersionId] = useState<number | null>(
    null
  );
  const versionEvaluationsData = useExpandableData<number, EvaluationItem[]>();

  const handleUploadVersion = useRouterMutation(async (file: File) => {
    await uploadVersion(projectId, file);
  });

  const handleSetActive = useRouterMutation(async (versionId: number) => {
    await setActiveVersion(projectId, versionId);
  });

  const handleToggleExpand = async (versionId: number) => {
    await versionEvaluationsData.toggle(versionId, () =>
      fetchVersionEvaluations(projectId, versionId)
    );
  };

  const handleRunEvaluation = (versionId: number) => {
    setEvaluatingVersionId(versionId);
    evaluationDialog.open();
  };

  const handleEvaluationComplete = useRouterMutation(async (evaluationId: string) => {
    // Close modal first
    evaluationDialog.close();
    setEvaluatingVersionId(null);

    // Navigate to evaluation results page
    navigate({
      to: "/projects/$projectId/evaluations/$evaluationId",
      params: {
        projectId: String(projectId),
        evaluationId: evaluationId,
      },
    });
  });

  // If on child route, only render the child (Outlet)
  if (isOnChildRoute) {
    return <Outlet />;
  }

  // Otherwise, render the project detail page
  return (
    <ProtectedRoute>
      <div className="container mx-auto p-8">
        <div className="mb-6">
          <Link
            to="/projects"
            className="mb-4 inline-block"
          >
            ← Atgal į projektus
          </Link>
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl font-bold mb-2">{project.name}</h1>
              <Badge variant="secondary">{project.project_type}</Badge>
            </div>
            <Button onClick={uploadDialog.open}>
              <Upload className="w-5 h-5 mr-2" />
              Įkelti naują versiją
            </Button>
          </div>
        </div>

        {versions.length === 0 ? (
          <div className="text-center py-12">
            <FileText className="w-16 h-16 mx-auto mb-4" />
            <p className="mb-4">Dar nėra dokumento versijų</p>
            <Button onClick={uploadDialog.open}>
              Įkelti pirmąją versiją
            </Button>
          </div>
        ) : (
          <VersionsList
            projectId={projectId}
            versions={versions}
            versionEvaluations={Object.fromEntries(
              versions.map(v => [v.id, versionEvaluationsData.getData(v.id) || []])
            )}
            onSetActive={handleSetActive}
            onRunEvaluation={handleRunEvaluation}
            onToggleExpand={handleToggleExpand}
            expandedVersionId={versionEvaluationsData.expandedId}
          />
        )}

        <UploadVersionDialog
          open={uploadDialog.isOpen}
          onOpenChange={uploadDialog.setIsOpen}
          onSubmit={handleUploadVersion}
        />

        {evaluationDialog.isOpen && evaluatingVersionId && (
          <RunEvaluationModal
            isOpen={evaluationDialog.isOpen}
            onClose={() => {
              evaluationDialog.close();
              setEvaluatingVersionId(null);
            }}
            projectType={project.project_type}
            versionId={evaluatingVersionId}
            projectId={project.id}
            onEvaluationComplete={handleEvaluationComplete}
          />
        )}
      </div>
    </ProtectedRoute>
  );
}
