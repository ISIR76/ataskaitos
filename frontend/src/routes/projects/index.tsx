import { createFileRoute, useRouter } from "@tanstack/react-router";
import { useState } from "react";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ProjectsList } from "@/components/ProjectsList";
import { CreateProjectDialog } from "@/components/CreateProjectDialog";
import {
  fetchProjects,
  createProject,
  deleteProject,
} from "../../api/projects";

export const Route = createFileRoute("/projects/")({
  loader: async () => {
    const projects = await fetchProjects();
    return { projects };
  },
  component: ProjectsPage,
  pendingComponent: () => (
    <div className="container mx-auto p-8">
      <div className="text-center">Įkeliami projektai...</div>
    </div>
  ),
  errorComponent: ({ error }) => (
    <div className="container mx-auto p-8">
      <div className="text-center text-red-600">
        Klaida įkeliant projektus: {error.message}
      </div>
    </div>
  ),
});

function ProjectsPage() {
  const { projects } = Route.useLoaderData();
  const router = useRouter();
  const [showCreateModal, setShowCreateModal] = useState(false);

  const handleCreateProject = async (
    name: string,
    type: "straipsnis" | "ataskaita"
  ) => {
    await createProject(name, type);
    // Invalidate and reload the route data
    await router.invalidate();
  };

  const handleDeleteProject = async (
    projectId: number,
    projectName: string
  ) => {
    if (
      !confirm(
        `Ar tikrai norite ištrinti "${projectName}"? Bus ištrintos visos versijos ir vertinimai.`
      )
    ) {
      return;
    }

    try {
      await deleteProject(projectId);
      // Invalidate and reload the route data
      await router.invalidate();
    } catch {
      alert("Nepavyko ištrinti projekto");
    }
  };

  return (
    <div className="container mx-auto p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Projektai</h1>
        <Button onClick={() => setShowCreateModal(true)}>
          <Plus className="w-5 h-5 mr-2" />
          Naujas projektas
        </Button>
      </div>

      <ProjectsList
        projects={projects}
        onCreateClick={() => setShowCreateModal(true)}
        onDeleteClick={handleDeleteProject}
      />

      <CreateProjectDialog
        open={showCreateModal}
        onOpenChange={setShowCreateModal}
        onSubmit={handleCreateProject}
      />
    </div>
  );
}
