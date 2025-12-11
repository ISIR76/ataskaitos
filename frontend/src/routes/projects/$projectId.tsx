import { createFileRoute, Link, useRouter, Outlet, useMatches } from "@tanstack/react-router";
import { useState } from "react";
import { Upload, FileText } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
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
      <div className="text-center text-red-600">
        Klaida įkeliant projektą: {error.message}
      </div>
    </div>
  ),
});

function ProjectDetailPage() {
  const { project, versions, projectId } = Route.useLoaderData();
  const router = useRouter();
  const matches = useMatches();

  // Check if we're on a child route (e.g., evaluation results page)
  const isOnChildRoute = matches.some(match =>
    match.id.includes('/evaluations/')
  );
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [showEvaluationModal, setShowEvaluationModal] = useState(false);
  const [evaluatingVersionId, setEvaluatingVersionId] = useState<number | null>(
    null
  );
  const [expandedVersion, setExpandedVersion] = useState<number | null>(null);
  const [versionEvaluations, setVersionEvaluations] = useState<
    Record<number, EvaluationItem[]>
  >({});

  const handleUploadVersion = async (file: File) => {
    await uploadVersion(projectId, file);
    // Reload the route data
    await router.invalidate();
  };

  const handleSetActive = async (versionId: number) => {
    await setActiveVersion(projectId, versionId);
    // Reload the route data
    await router.invalidate();
  };

  const handleToggleExpand = async (versionId: number) => {
    if (expandedVersion === versionId) {
      setExpandedVersion(null);
    } else {
      setExpandedVersion(versionId);
      // Load evaluations if not already loaded
      if (!versionEvaluations[versionId]) {
        try {
          const evaluations = await fetchVersionEvaluations(
            projectId,
            versionId
          );
          setVersionEvaluations((prev) => ({
            ...prev,
            [versionId]: evaluations,
          }));
        } catch (err) {
          console.error("Failed to load evaluations:", err);
        }
      }
    }
  };

  const handleRunEvaluation = (versionId: number) => {
    setEvaluatingVersionId(versionId);
    setShowEvaluationModal(true);
  };

  const handleEvaluationComplete = async () => {
    // Reload project data
    await router.invalidate();
    // Auto-expand the version's evaluation history
    if (evaluatingVersionId) {
      setExpandedVersion(evaluatingVersionId);
    }
    // Close modal
    setShowEvaluationModal(false);
    setEvaluatingVersionId(null);
  };

  // If on child route, only render the child (Outlet)
  if (isOnChildRoute) {
    return <Outlet />;
  }

  // Otherwise, render the project detail page
  return (
    <div className="container mx-auto p-8">
      <div className="mb-6">
        <Link
          to="/projects"
          className="text-blue-600 hover:text-blue-800 mb-4 inline-block"
        >
          ← Atgal į projektus
        </Link>
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold mb-2">{project.name}</h1>
            <Badge variant="secondary">{project.project_type}</Badge>
          </div>
          <Button onClick={() => setShowUploadModal(true)}>
            <Upload className="w-5 h-5 mr-2" />
            Įkelti naują versiją
          </Button>
        </div>
      </div>

      {versions.length === 0 ? (
        <Card className="text-center py-12">
          <CardContent className="pt-6">
            <FileText className="w-16 h-16 mx-auto text-gray-400 mb-4" />
            <p className="text-gray-600 mb-4">Dar nėra dokumento versijų</p>
            <Button onClick={() => setShowUploadModal(true)}>
              Įkelti pirmąją versiją
            </Button>
          </CardContent>
        </Card>
      ) : (
        <VersionsList
          projectId={projectId}
          versions={versions}
          versionEvaluations={versionEvaluations}
          onSetActive={handleSetActive}
          onRunEvaluation={handleRunEvaluation}
          onToggleExpand={handleToggleExpand}
          expandedVersionId={expandedVersion}
        />
      )}

      <UploadVersionDialog
        open={showUploadModal}
        onOpenChange={setShowUploadModal}
        onSubmit={handleUploadVersion}
      />

      {showEvaluationModal && evaluatingVersionId && (
        <RunEvaluationModal
          isOpen={showEvaluationModal}
          onClose={() => {
            setShowEvaluationModal(false);
            setEvaluatingVersionId(null);
          }}
          projectType={project.project_type}
          versionId={evaluatingVersionId}
          projectId={project.id}
          onEvaluationComplete={handleEvaluationComplete}
        />
      )}
    </div>
  );
}
