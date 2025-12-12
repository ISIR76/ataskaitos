import React, { useState, useEffect } from "react";
import { Loader2, ChevronDown, ChevronUp, CheckSquare, Square } from "lucide-react";
import { client } from "../api/client";
import type { components } from "../api/schema";
import { runEvaluation } from "@/api/projects";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Card } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";

type EvaluatorInfo = components["schemas"]["EvaluatorInfo"];

interface RunEvaluationModalProps {
  isOpen: boolean;
  onClose: () => void;
  projectType: string;  // "straipsnis" or "ataskaita"
  versionId: number;
  projectId: number;
  onEvaluationComplete: (evaluationId: string) => void;
}

export function RunEvaluationModal({
  isOpen,
  onClose,
  projectType,
  versionId,
  projectId,
  onEvaluationComplete,
}: RunEvaluationModalProps) {
  // Map project types to document types
  const documentType = projectType === "straipsnis" ? "article" : "report";

  const [evaluationType, setEvaluationType] = useState<"scoring" | "agent">("scoring");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [availableEvaluators, setAvailableEvaluators] = useState<EvaluatorInfo[]>([]);
  const [selectedEvaluators, setSelectedEvaluators] = useState<string[]>([]);
  const [loadingEvaluators, setLoadingEvaluators] = useState(false);
  const [expandedEvaluators, setExpandedEvaluators] = useState<Set<string>>(new Set());

  // Fetch evaluators/agents when evaluation type changes
  useEffect(() => {
    if (!isOpen) return;

    const fetchOptions = async () => {
      setLoadingEvaluators(true);
      try {
        if (evaluationType === "scoring") {
          // Fetch evaluators
          const result = await client.GET("/api/v1/evaluators");
          if (result.data) {
            const evaluators = result.data.evaluators[documentType] || [];
            setAvailableEvaluators(evaluators);
            // Select all by default
            setSelectedEvaluators(evaluators.map((e) => e.name));
          }
        } else {
          // Fetch agents
          const result = await client.GET("/api/v1/agents");
          if (result.data) {
            const agents = (result.data as any).agents[documentType] || [];
            // Convert to EvaluatorInfo format for reuse
            const agentEvaluators = agents.map((a: any) => ({
              name: a.name,
              source: null,
              has_assertion: false,
              rubric: a.description || null,
              metadata: a
            }));
            setAvailableEvaluators(agentEvaluators);
            // Select all by default
            setSelectedEvaluators(agentEvaluators.map((e: any) => e.name));
          }
        }
      } catch (err) {
        console.error("Failed to fetch options:", err);
        setError("Nepavyko įkelti vertintojų");
      } finally {
        setLoadingEvaluators(false);
      }
    };

    fetchOptions();
  }, [isOpen, evaluationType, documentType]);

  const toggleEvaluator = (name: string) => {
    setSelectedEvaluators((prev) =>
      prev.includes(name) ? prev.filter((n) => n !== name) : [...prev, name]
    );
  };

  const toggleExpanded = (name: string) => {
    setExpandedEvaluators((prev) => {
      const next = new Set(prev);
      if (next.has(name)) {
        next.delete(name);
      } else {
        next.add(name);
      }
      return next;
    });
  };

  const toggleAll = () => {
    if (selectedEvaluators.length === availableEvaluators.length) {
      setSelectedEvaluators([]);
    } else {
      setSelectedEvaluators(availableEvaluators.map((e) => e.name));
    }
  };

  const getFirstLine = (text: string | null | undefined): string => {
    if (!text) return "";
    const firstLine = text.trim().split("\n")[0];
    return firstLine.length > 120 ? firstLine.substring(0, 120) + "..." : firstLine;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Require at least one evaluator/agent selected
    if (selectedEvaluators.length === 0) {
      setError(`Pasirinkite bent vieną ${evaluationType === "scoring" ? "vertintoją" : "agentą"}`);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const evaluationId = await runEvaluation(projectId, versionId, evaluationType, selectedEvaluators);
      onEvaluationComplete(evaluationId);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Paleisti vertinimą</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Evaluation Type */}
          <div className="space-y-2">
            <Label className="text-sm font-medium">Vertinimo metodas</Label>
            <div className="grid grid-cols-2 gap-2">
              <Button
                type="button"
                variant={evaluationType === "scoring" ? "default" : "outline"}
                onClick={() => setEvaluationType("scoring")}
                disabled={loading}
                className="w-full"
              >
                Įvertinimas
              </Button>
              <Button
                type="button"
                variant={evaluationType === "agent" ? "default" : "outline"}
                onClick={() => setEvaluationType("agent")}
                disabled={loading}
                className="w-full"
              >
                Agentas
              </Button>
            </div>
          </div>

          {/* Evaluator/Agent Selection */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <Label className="text-sm font-medium">
                Pasirinkite {evaluationType === "scoring" ? "vertintojus" : "agentus"} ({selectedEvaluators.length}/{availableEvaluators.length})
              </Label>
              <Button
                type="button"
                variant="link"
                onClick={toggleAll}
                disabled={loading}
                className="h-auto p-0 text-sm"
              >
                {selectedEvaluators.length === availableEvaluators.length
                  ? "Atžymėti viską"
                  : "Pasirinkti viską"}
              </Button>
            </div>

            {loadingEvaluators ? (
              <div className="flex items-center justify-center p-4 text-sm text-muted-foreground">
                <Loader2 className="h-4 w-4 animate-spin mr-2" />
                Įkeliami {evaluationType === "scoring" ? "vertintojai" : "agentai"}...
              </div>
            ) : availableEvaluators.length === 0 ? (
              <Alert>
                <AlertDescription>
                  Nėra sukonfigūruotų {evaluationType === "scoring" ? "vertintojų" : "agentų"} {documentType}s.
                </AlertDescription>
              </Alert>
            ) : (
              <Card className="max-h-96 overflow-y-auto">
                <div className="divide-y">
                  {availableEvaluators.map((evaluator) => {
                    const isExpanded = expandedEvaluators.has(evaluator.name);
                    return (
                      <div key={evaluator.name} className="p-3">
                        <div className="flex items-start gap-3">
                          <input
                            type="checkbox"
                            checked={selectedEvaluators.includes(evaluator.name)}
                            onChange={() => toggleEvaluator(evaluator.name)}
                            disabled={loading}
                            className="hidden"
                            id={`eval-${evaluator.name}`}
                          />
                          <label
                            htmlFor={`eval-${evaluator.name}`}
                            className="cursor-pointer"
                          >
                            {selectedEvaluators.includes(evaluator.name) ? (
                              <CheckSquare className="h-5 w-5 text-blue-600 shrink-0 mt-0.5" />
                            ) : (
                              <Square className="h-5 w-5 text-gray-400 shrink-0 mt-0.5" />
                            )}
                          </label>
                          <div className="flex-1 min-w-0">
                            <div className="flex items-start gap-2">
                              <label
                                htmlFor={`eval-${evaluator.name}`}
                                className="flex-1 cursor-pointer"
                              >
                                <span className="text-sm font-medium capitalize block">
                                  {evaluator.name.replace(/_/g, " ")}
                                </span>
                                {evaluator.rubric && (
                                  <span className="text-xs text-gray-600 block mt-1">
                                    {getFirstLine(evaluator.rubric)}
                                  </span>
                                )}
                              </label>
                              {evaluator.rubric && (
                                <button
                                  type="button"
                                  onClick={() => toggleExpanded(evaluator.name)}
                                  disabled={loading}
                                  className="text-gray-400 hover:text-gray-600 transition-colors shrink-0 mt-0.5"
                                  aria-label={isExpanded ? "Suskleisti" : "Išskleisti"}
                                >
                                  {isExpanded ? (
                                    <ChevronUp className="h-4 w-4" />
                                  ) : (
                                    <ChevronDown className="h-4 w-4" />
                                  )}
                                </button>
                              )}
                            </div>
                            {isExpanded && evaluator.rubric && (
                              <div className="mt-3 pt-3 border-t">
                                <h4 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
                                  Pilna rubrika
                                </h4>
                                <pre className="whitespace-pre-wrap text-xs text-gray-600 bg-gray-50 rounded-md p-3 overflow-auto max-h-64">
                                  {evaluator.rubric}
                                </pre>
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </Card>
            )}
          </div>

          {/* Error Display */}
          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={onClose}
              disabled={loading}
            >
              Atšaukti
            </Button>
            <Button
              type="submit"
              disabled={loading || selectedEvaluators.length === 0}
            >
              {loading ? (
                <>
                  <Loader2 className="h-5 w-5 animate-spin mr-2" />
                  Vertinama...
                </>
              ) : (
                "Paleisti vertinimą"
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
