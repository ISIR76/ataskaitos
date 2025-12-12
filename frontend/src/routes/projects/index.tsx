import { createFileRoute } from "@tanstack/react-router";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ProjectsList } from "@/components/ProjectsList";
import { CreateProjectDialog } from "@/components/CreateProjectDialog";
import {
  fetchProjects,
  createProject,
  deleteProject,
} from "../../api/projects";
import { useRouterMutation, useDialog } from "@/hooks";

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
      <div className="text-center text-destructive">
        Klaida įkeliant projektus: {error.message}
      </div>
    </div>
  ),
});

function ProjectsPage() {
  const { projects } = Route.useLoaderData();
  const createDialog = useDialog();

  const handleCreateProject = useRouterMutation(
    async (name: string, type: "straipsnis" | "ataskaita") => {
      await createProject(name, type);
    }
  );

  const handleDeleteProject = useRouterMutation(
    async (projectId: number, projectName: string) => {
      if (
        !confirm(
          `Ar tikrai norite ištrinti "${projectName}"? Bus ištrintos visos versijos ir vertinimai.`
        )
      ) {
        return;
      }

      try {
        await deleteProject(projectId);
      } catch {
        alert("Nepavyko ištrinti projekto");
      }
    }
  );

  return (
    <div className="container mx-auto p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Projektai</h1>
        <Button onClick={createDialog.open}>
          <Plus className="w-5 h-5 mr-2" />
          Naujas projektas
        </Button>
      </div>

      <ProjectsList
        projects={projects}
        onCreateClick={createDialog.open}
        onDeleteClick={handleDeleteProject}
      />

      <CreateProjectDialog
        open={createDialog.isOpen}
        onOpenChange={createDialog.setIsOpen}
        onSubmit={handleCreateProject}
      />
    </div>
  );
}
