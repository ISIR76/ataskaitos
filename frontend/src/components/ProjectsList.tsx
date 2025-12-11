import { Link } from "@tanstack/react-router";
import { FileText, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
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
      <Card className="text-center py-12">
        <FileText className="w-16 h-16 mx-auto text-gray-400 mb-4" />
        <p className="text-gray-600 mb-4">Dar nėra projektų</p>
        <Button onClick={onCreateClick}>
          Sukurkite savo pirmąjį projektą
        </Button>
      </Card>
    );
  }

  return (
    <Card>
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
                <Link
                  to="/projects/$projectId"
                  params={{ projectId: String(project.id) }}
                  className="text-blue-600 hover:text-blue-800 font-medium"
                >
                  {project.name}
                </Link>
              </TableCell>
              <TableCell>
                <Badge variant="secondary">{project.project_type}</Badge>
              </TableCell>
              <TableCell className="text-sm text-gray-500">
                {project.active_version_number
                  ? `v${project.active_version_number}`
                  : "Nėra"}
              </TableCell>
              <TableCell className="text-sm text-gray-500">
                {project.total_versions}
              </TableCell>
              <TableCell className="text-sm text-gray-500">
                {new Date(project.created_at).toLocaleDateString()}
              </TableCell>
              <TableCell>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => onDeleteClick(project.id, project.name)}
                  className="text-red-600 hover:text-red-800"
                >
                  <Trash2 className="w-5 h-5" />
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Card>
  );
}
