import React, { useState, useEffect } from "react";
import { Upload, FileText, Loader2, ChevronDown, ChevronUp, CheckSquare, Square } from "lucide-react";
import { client } from "../api/client";
import type { components } from "../api/schema";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

type EvaluationResponse = components["schemas"]["UnifiedEvaluationResponse"];
type EvaluatorInfo = components["schemas"]["EvaluatorInfo"];

interface DocumentUploadProps {
  onEvaluationComplete?: (result: EvaluationResponse) => void;
  documentType?: "report" | "article";
  hideDocumentTypeSelector?: boolean;
}

export function DocumentUpload({
  onEvaluationComplete,
  documentType: initialDocumentType = "article",
  hideDocumentTypeSelector = false,
}: DocumentUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [documentType, setDocumentType] = useState<"report" | "article">(
    initialDocumentType
  );
  const [evaluationType, setEvaluationType] = useState<"scoring" | "agent">("scoring");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const [availableEvaluators, setAvailableEvaluators] = useState<EvaluatorInfo[]>([]);
  const [selectedEvaluators, setSelectedEvaluators] = useState<string[]>([]);
  const [loadingEvaluators, setLoadingEvaluators] = useState(false);
  const [expandedEvaluators, setExpandedEvaluators] = useState<Set<string>>(new Set());

  // Fetch evaluators/agents when document type or evaluation type changes
  useEffect(() => {
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
      } finally {
        setLoadingEvaluators(false);
      }
    };

    fetchOptions();
  }, [documentType, evaluationType]);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
      setError(null);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

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
    if (!file) {
      setError("Pasirinkite failą");
      return;
    }

    // Require at least one evaluator/agent selected
    if (selectedEvaluators.length === 0) {
      setError(`Pasirinkite bent vieną ${evaluationType === "scoring" ? "vertintoją" : "agentą"}`);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("document_type", documentType);
      formData.append("evaluation_type", evaluationType);

      // Pass evaluators for scoring mode, agents for agent mode
      if (evaluationType === "scoring") {
        formData.append("evaluators", selectedEvaluators.join(","));
      } else {
        formData.append("agents", selectedEvaluators.join(","));
      }

      const result = await client.POST("/api/v1/evaluate", {
        // @ts-expect-error - FormData is valid for multipart/form-data
        body: formData,
      });

      if (result.data) {
        onEvaluationComplete?.(result.data);
      } else {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        setError(`Evaluation failed: ${JSON.stringify((result as any).error)}`);
      }
    } catch (err) {
      setError(`Error: ${err instanceof Error ? err.message : "Unknown error"}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* File Upload Area */}
        <div
          className={`relative rounded-lg border-2 border-dashed p-8 text-center transition-colors ${
            dragActive
              ? "border-primary bg-primary/5"
              : "border-muted-foreground/25 hover:border-muted-foreground/50"
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <Input
            type="file"
            id="file-upload"
            className="hidden"
            onChange={handleFileChange}
            accept=".docx,.pdf,.doc,.txt,.md"
          />

          <Label
            htmlFor="file-upload"
            className="flex flex-col items-center cursor-pointer"
          >
            <Upload className="h-12 w-12 text-muted-foreground mb-4" />
            <p className="text-lg font-medium mb-1">
              {file ? file.name : "Tempkite dokumentą čia"}
            </p>
            <p className="text-sm text-muted-foreground">
              arba spustelėkite naršyti (DOCX, PDF, MD, TXT)
            </p>
            {file && (
              <div className="mt-4 flex items-center gap-2 text-sm text-muted-foreground">
                <FileText className="h-4 w-4" />
                <span>{(file.size / 1024).toFixed(1)} KB</span>
              </div>
            )}
          </Label>
        </div>

        {/* Options */}
        <div className={hideDocumentTypeSelector ? "" : "grid gap-6 md:grid-cols-2"}>
          {/* Document Type */}
          {!hideDocumentTypeSelector && (
            <div className="space-y-2">
              <Label className="text-sm font-medium">Dokumento tipas</Label>
              <div className="grid grid-cols-2 gap-2">
                <Button
                  type="button"
                  variant={documentType === "article" ? "default" : "outline"}
                  onClick={() => setDocumentType("article")}
                >
                  Straipsnis
                </Button>
                <Button
                  type="button"
                  variant={documentType === "report" ? "default" : "outline"}
                  onClick={() => setDocumentType("report")}
                >
                  Ataskaita
                </Button>
              </div>
            </div>
          )}

          {/* Evaluation Type */}
          <div className="space-y-2">
            <Label className="text-sm font-medium">Vertinimo metodas</Label>
            <div className="grid grid-cols-2 gap-2">
              <Button
                type="button"
                variant={evaluationType === "scoring" ? "default" : "outline"}
                onClick={() => setEvaluationType("scoring")}
              >
                Įvertinimas
              </Button>
              <Button
                type="button"
                variant={evaluationType === "agent" ? "default" : "outline"}
                onClick={() => setEvaluationType("agent")}
              >
                Agentas
              </Button>
            </div>
          </div>
        </div>

        {/* Evaluator/Agent Selection */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <label className="text-sm font-medium">
              Pasirinkite {evaluationType === "scoring" ? "vertintojus" : "agentus"} ({selectedEvaluators.length}/{availableEvaluators.length})
            </label>
            <button
              type="button"
              onClick={toggleAll}
              className="text-sm text-primary hover:underline"
            >
              {selectedEvaluators.length === availableEvaluators.length
                ? "Atžymėti viską"
                : "Pasirinkti viską"}
            </button>
          </div>

          {loadingEvaluators ? (
            <div className="flex items-center justify-center p-4 text-sm text-muted-foreground">
              <Loader2 className="h-4 w-4 animate-spin mr-2" />
              Įkeliami {evaluationType === "scoring" ? "vertintojai" : "agentai"}...
            </div>
          ) : availableEvaluators.length === 0 ? (
            <div className="rounded-lg border border-yellow-200 bg-yellow-50 dark:bg-yellow-900/20 p-4">
              <p className="text-sm text-yellow-800 dark:text-yellow-200">
                Nėra sukonfigūruotų {evaluationType === "scoring" ? "vertintojų" : "agentų"} {documentType === "article" ? "straipsniams" : "ataskaitoms"}.
              </p>
            </div>
          ) : (
            <div className="rounded-lg border bg-card max-h-96 overflow-y-auto">
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
                          className="hidden"
                          id={`eval-${evaluator.name}`}
                        />
                        <label
                          htmlFor={`eval-${evaluator.name}`}
                          className="cursor-pointer"
                        >
                          {selectedEvaluators.includes(evaluator.name) ? (
                            <CheckSquare className="h-5 w-5 text-primary shrink-0 mt-0.5" />
                          ) : (
                            <Square className="h-5 w-5 text-muted-foreground shrink-0 mt-0.5" />
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
                                <span className="text-xs text-muted-foreground block mt-1">
                                  {getFirstLine(evaluator.rubric)}
                                </span>
                              )}
                            </label>
                            {evaluator.rubric && (
                              <button
                                type="button"
                                onClick={() => toggleExpanded(evaluator.name)}
                                className="text-muted-foreground hover:text-foreground transition-colors shrink-0 mt-0.5"
                                aria-label={isExpanded ? "Collapse" : "Expand"}
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
                              <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2">
                                Pilna rubrika
                              </h4>
                              <pre className="whitespace-pre-wrap text-xs text-muted-foreground bg-muted/30 rounded-md p-3 overflow-auto max-h-64">
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
            </div>
          )}
        </div>

        {/* Error Display */}
        {error && (
          <div className="rounded-lg border border-destructive bg-destructive/10 p-4">
            <p className="text-sm text-destructive">{error}</p>
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={!file || loading}
          className="w-full px-6 py-3 bg-primary text-primary-foreground rounded-md font-medium hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <Loader2 className="h-5 w-5 animate-spin" />
              Vertinama...
            </>
          ) : (
            "Vertinti dokumentą"
          )}
        </button>
      </form>
    </div>
  );
}
