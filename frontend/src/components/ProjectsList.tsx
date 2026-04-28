import { Link } from "@tanstack/react-router";
import { CheckCircle2, FileText, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import type { Project } from "../api/projects";

interface ProjectsListProps {
  projects: Project[];
  onCreateClick: () => void;
  onDeleteClick: (projectId: number, projectName: string) => void;
}

export function ProjectsList({
  projects,
  onCreateClick,
  onDeleteClick,
}: ProjectsListProps) {
  if (projects.length === 0) {
    return (
      <div className="text-center py-12">
        <FileText className="w-16 h-16 mx-auto mb-4" />
        <p className="mb-4">Dar nėra projektų</p>
        <Button onClick={onCreateClick}>
          Sukurkite savo pirmąjį projektą
        </Button>
      </div>
    );
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Pavadinimas</TableHead>
          <TableHead>Tipas</TableHead>
          <TableHead>Aktyvi versija</TableHead>
          <TableHead>Iš viso versijų</TableHead>
          <TableHead>Sukurta</TableHead>
          <TableHead>Veiksmai</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {projects.map((project) => (
          <TableRow key={project.id}>
            <TableCell>
              <div className="flex items-center gap-2">
                <Link
                  to="/projects/$projectId"
                  params={{ projectId: String(project.id) }}
                >
                  {project.name}
                </Link>
                {project.is_marked_good && (
                  <CheckCircle2
                    className="w-4 h-4 text-green-600"
                    aria-label="Pažymėtas kaip geras"
                  />
                )}
              </div>
            </TableCell>
            <TableCell>
              <Badge variant="secondary">{project.project_type}</Badge>
            </TableCell>
            <TableCell>
              {project.active_version_number
                ? `v${project.active_version_number}`
                : "Nėra"}
            </TableCell>
            <TableCell>
              {project.total_versions}
            </TableCell>
            <TableCell>
              {new Date(project.created_at).toLocaleDateString()}
            </TableCell>
            <TableCell>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onDeleteClick(project.id, project.name)}
              >
                <Trash2 className="w-5 h-5" />
              </Button>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
