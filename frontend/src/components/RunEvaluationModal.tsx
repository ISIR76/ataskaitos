import React, { useState, useEffect } from "react";
import { Loader2, ChevronDown, ChevronUp } from "lucide-react";
import { client } from "../api/client";
import type { components } from "../api/schema";
import { runEvaluation } from "@/api/projects";
import { Button } from "@/components/ui/button";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetFooter,
} from "@/components/ui/sheet";
import { Label } from "@/components/ui/label";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Checkbox } from "@/components/ui/checkbox";

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
    <Sheet open={isOpen} onOpenChange={onClose}>
      <SheetContent side="right" className="w-full sm:w-[600px] lg:w-[800px] overflow-y-auto p-6">
        <SheetHeader className="mb-6">
          <SheetTitle className="text-xl">Paleisti vertinimą</SheetTitle>
        </SheetHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Evaluation Type */}
          <div className="space-y-2">
            <Label className="text-sm">Vertinimo metodas</Label>
            <div className="grid grid-cols-2 gap-3">
              <Button
                type="button"
                variant={evaluationType === "scoring" ? "default" : "outline"}
                onClick={() => setEvaluationType("scoring")}
                disabled={loading}
                className="h-9"
              >
                Įvertinimas
              </Button>
              <Button
                type="button"
                variant={evaluationType === "agent" ? "default" : "outline"}
                onClick={() => setEvaluationType("agent")}
                disabled={loading}
                className="h-9"
              >
                Agentas
              </Button>
            </div>
          </div>

          {/* Evaluator/Agent Selection */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-baseline gap-3">
                <Label className="text-sm">
                  {evaluationType === "scoring" ? "Vertintojai" : "Agentai"}
                </Label>
                <span className="text-xs text-muted-foreground">
                  Pasirinkta: {selectedEvaluators.length}/{availableEvaluators.length}
                </span>
              </div>
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={toggleAll}
                disabled={loading}
              >
                {selectedEvaluators.length === availableEvaluators.length
                  ? "Atžymėti viską"
                  : "Pasirinkti viską"}
              </Button>
            </div>

            {loadingEvaluators ? (
              <div className="flex items-center justify-center p-6 text-sm text-muted-foreground">
                <Loader2 className="h-4 w-4 animate-spin mr-2" />
                Įkeliami {evaluationType === "scoring" ? "vertintojai" : "agentai"}...
              </div>
            ) : availableEvaluators.length === 0 ? (
              <Alert>
                <AlertDescription className="text-sm">
                  Nėra sukonfigūruotų {evaluationType === "scoring" ? "vertintojų" : "agentų"} {documentType}s.
                </AlertDescription>
              </Alert>
            ) : (
              <div className="divide-y">
                {availableEvaluators.map((evaluator) => {
                    const isExpanded = expandedEvaluators.has(evaluator.name);
                    return (
                      <div key={evaluator.name} className="py-3 px-2 hover:bg-muted/50 transition-colors">
                        <div className="flex items-center gap-4">
                          <Checkbox
                            checked={selectedEvaluators.includes(evaluator.name)}
                            onCheckedChange={() => toggleEvaluator(evaluator.name)}
                            disabled={loading}
                          />
                          <div className="flex-1 min-w-0">
                            <div className="font-medium text-sm capitalize">
                              {evaluator.name.replace(/_/g, " ")}
                            </div>
                          </div>
                          {evaluator.rubric && (
                            <Button
                              type="button"
                              variant="ghost"
                              size="sm"
                              onClick={() => toggleExpanded(evaluator.name)}
                              disabled={loading}
                              className="shrink-0 h-7 w-7 p-0"
                            >
                              {isExpanded ? (
                                <ChevronUp className="h-3 w-3" />
                              ) : (
                                <ChevronDown className="h-3 w-3" />
                              )}
                            </Button>
                          )}
                        </div>
                        {isExpanded && evaluator.rubric && (
                          <div className="mt-3 ml-8 pt-3 border-t">
                            <div className="text-xs bg-muted rounded-md p-3 max-h-64 overflow-auto">
                              <pre className="whitespace-pre-wrap font-sans text-xs leading-relaxed">
                                {evaluator.rubric}
                              </pre>
                            </div>
                          </div>
                        )}
                      </div>
                    );
                  })}
              </div>
            )}
          </div>

          {/* Error Display */}
          {error && (
            <Alert variant="destructive">
              <AlertDescription className="text-sm">{error}</AlertDescription>
            </Alert>
          )}

          <SheetFooter className="gap-2 mt-6">
            <Button
              type="button"
              variant="outline"
              onClick={onClose}
              disabled={loading}
              className="h-9"
            >
              Atšaukti
            </Button>
            <Button
              type="submit"
              disabled={loading || selectedEvaluators.length === 0}
              className="h-9"
            >
              {loading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin mr-2" />
                  Vertinama...
                </>
              ) : (
                "Paleisti vertinimą"
              )}
            </Button>
          </SheetFooter>
        </form>
      </SheetContent>
    </Sheet>
  );
}
