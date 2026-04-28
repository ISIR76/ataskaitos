import { Link } from "@tanstack/react-router";
import {
  CheckCircle,
  Clock,
  ChevronDown,
  ChevronUp,
  Play,
  Sparkles,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import type { DocumentVersion, EvaluationItem } from "../api/projects";

interface VersionsListProps {
  projectId: number;
  versions: DocumentVersion[];
  versionEvaluations: Record<number, EvaluationItem[]>;
  onSetActive: (versionId: number) => void;
  onRunEvaluation: (versionId: number) => void;
  onRunLlmDetection?: (versionId: number) => void;
  llmDetectionRunningId?: number | null;
  onToggleExpand: (versionId: number) => void;
  expandedVersionId: number | null;
  showLlmDetector?: boolean;
}

export function VersionsList({
  projectId,
  versions,
  versionEvaluations,
  onSetActive,
  onRunEvaluation,
  onRunLlmDetection,
  llmDetectionRunningId = null,
  onToggleExpand,
  expandedVersionId,
  showLlmDetector = false,
}: VersionsListProps) {
  return (
    <div className="space-y-4">
      {versions.map((version) => (
        <div key={version.id} className="border rounded-lg p-6">
          <div className="flex justify-between items-start">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-2">
                <h3 className="font-semibold">Versija {version.version_number}</h3>
                {version.is_active && (
                  <Badge>
                    <CheckCircle className="w-3 h-3 mr-1" />
                    Aktyvi
                  </Badge>
                )}
              </div>
              <p className="text-sm mb-1">
                {version.original_filename}
              </p>
              <div className="flex gap-4 text-sm text-muted-foreground">
                <span>
                  {version.character_count.toLocaleString()} simboliai
                </span>
                <span>{version.evaluation_count} vertinimai</span>
                <span>
                  Įkelta {new Date(version.created_at).toLocaleString()}
                </span>
              </div>
            </div>
            <div className="flex gap-2">
              {!version.is_active && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => onSetActive(version.id)}
                >
                  Nustatyti aktyvią
                </Button>
              )}
              <Button
                onClick={() => onRunEvaluation(version.id)}
              >
                <Play className="w-4 h-4 mr-2" />
                Paleisti vertinimą
              </Button>
              {showLlmDetector && onRunLlmDetection && (
                <Button
                  variant="outline"
                  onClick={() => onRunLlmDetection(version.id)}
                  disabled={llmDetectionRunningId === version.id}
                >
                  <Sparkles className="w-4 h-4 mr-2" />
                  {llmDetectionRunningId === version.id
                    ? "Tikrinama..."
                    : "Tikrinti AI"}
                </Button>
              )}
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onToggleExpand(version.id)}
              >
                {expandedVersionId === version.id ? (
                  <ChevronUp className="w-5 h-5" />
                ) : (
                  <ChevronDown className="w-5 h-5" />
                )}
              </Button>
            </div>
          </div>

          {expandedVersionId === version.id && (
            <div className="border-t mt-6 pt-6">
              <h4 className="font-semibold mb-3">Vertinimo istorija</h4>
              {versionEvaluations[version.id]?.length > 0 ? (
                <div className="space-y-2">
                  {versionEvaluations[version.id].map((evaluation) => (
                    <div
                      key={evaluation.id}
                      className="bg-muted p-4 rounded border"
                    >
                      <div className="flex justify-between items-start">
                        <div>
                          <div className="flex items-center gap-2 mb-1">
                            <span className="font-medium">
                              {evaluation.evaluation_type}
                            </span>
                            <span className="text-xs text-muted-foreground">
                              {evaluation.evaluators_used.length} vertintojai
                            </span>
                          </div>
                          <div className="text-sm text-muted-foreground">
                            <Clock className="w-3 h-3 inline mr-1" />
                            {evaluation.duration_seconds.toFixed(2)}s •{" "}
                            {new Date(evaluation.created_at).toLocaleString()}
                          </div>
                        </div>
                        <Link
                          to="/projects/$projectId/evaluations/$evaluationId"
                          params={{
                            projectId: projectId.toString(),
                            evaluationId: evaluation.evaluation_id,
                          }}
                          className="text-sm"
                          onClick={() => {
                            console.log("🔗 Clicking evaluation link:", {
                              projectId,
                              evaluationId: evaluation.evaluation_id,
                              to: `/projects/${projectId}/evaluations/${evaluation.evaluation_id}`
                            });
                          }}
                        >
                          Peržiūrėti rezultatus →
                        </Link>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-muted-foreground text-sm">Dar nėra vertinimų</p>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
