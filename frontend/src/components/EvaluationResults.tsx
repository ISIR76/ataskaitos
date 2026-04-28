import React from "react";
import {
  CheckCircle2,
  XCircle,
  AlertCircle,
  ChevronDown,
  ChevronUp,
  Sparkles,
} from "lucide-react";
import type { components } from "../api/schema";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

type EvaluationResponse = components["schemas"]["UnifiedEvaluationResponse"];

interface EvaluationResultsProps {
  result: EvaluationResponse;
}

export function EvaluationResults({ result }: EvaluationResultsProps) {
  const [expandedSections, setExpandedSections] = React.useState<Set<string>>(
    new Set()
  );

  const toggleSection = (key: string) => {
    setExpandedSections((prev) => {
      const next = new Set(prev);
      if (next.has(key)) {
        next.delete(key);
      } else {
        next.add(key);
      }
      return next;
    });
  };

  const renderScore = (score: number) => {
    const percentage = Math.round(score * 100);

    return (
      <div className="flex items-center gap-2">
        <span className="text-2xl font-bold">{percentage}%</span>
        <div className="flex-1 h-2 bg-muted rounded-full overflow-hidden">
          <div
            className="h-full bg-primary transition-all"
            style={{ width: `${percentage}%` }}
          />
        </div>
      </div>
    );
  };

  const renderScoringResults = () => {
    const resultData = result.results as any;

    console.log("📊 Rendering scoring results:", {
      resultData,
      hasCases: resultData?.cases,
      casesLength: resultData?.cases?.length,
      firstCase: resultData?.cases?.[0],
    });

    // Check if we have cases with scores
    if (!resultData?.cases || resultData.cases.length === 0) {
      return (
        <Alert variant="destructive">
          <AlertDescription>
            Nėra prieinamų vertinimo balų. Dokumentas galėjo nepavykti apdoroti.
          </AlertDescription>
        </Alert>
      );
    }

    // Get scores from the first case (our uploaded document)
    const caseData = resultData.cases[0];
    const scores = caseData?.scores || {};

    console.log("📈 Scores object:", {
      scores,
      scoreKeys: Object.keys(scores),
      scoreEntries: Object.entries(scores),
    });

    if (Object.keys(scores).length === 0) {
      return (
        <Alert variant="destructive">
          <AlertDescription>
            Vertinimo rezultatuose balų nerasta. Vertinimas galbūt buvo paleistas su klaida arba balai nebuvo išsaugoti duomenų bazėje.
            <br />
            <br />
            <strong>Sprendimas:</strong> Paleiskite naują vertinimą šiai versijai.
          </AlertDescription>
        </Alert>
      );
    }

    return (
      <div className="space-y-4">
        {Object.entries(scores).map(([key, scoreData]: [string, any]) => {
          const isExpanded = expandedSections.has(key);
          const score = scoreData?.value || 0;
          const reason = scoreData?.reason || "";

          return (
            <div key={key} className="border rounded-lg">
              <Button
                variant="ghost"
                onClick={() => toggleSection(key)}
                className="w-full p-4 flex items-center justify-between h-auto"
              >
                <div className="flex-1 text-left">
                  <h4 className="font-semibold capitalize">
                    {key.replace(/_/g, " ")}
                  </h4>
                  <div className="mt-2">{renderScore(score)}</div>
                </div>
                {reason && (
                  <div className="ml-4">
                    {isExpanded ? (
                      <ChevronUp className="h-5 w-5 text-muted-foreground" />
                    ) : (
                      <ChevronDown className="h-5 w-5 text-muted-foreground" />
                    )}
                  </div>
                )}
              </Button>

              {isExpanded && reason && (
                <div className="px-4 pb-4 pt-2 border-t">
                  <p className="text-sm text-muted-foreground whitespace-pre-wrap">
                    {reason}
                  </p>
                </div>
              )}
            </div>
          );
        })}
      </div>
    );
  };

  const isLlmDetectionPayload = (payload: any): boolean => {
    return (
      payload &&
      typeof payload.ai_probability === "number" &&
      typeof payload.verdict === "string" &&
      Array.isArray(payload.indicators)
    );
  };

  const renderLlmDetection = (payload: any) => {
    const probability = Math.max(0, Math.min(1, payload.ai_probability));
    const percent = Math.round(probability * 100);
    const verdict: string = payload.verdict;
    const verdictLabel =
      verdict === "likely_ai"
        ? "Tikėtina AI"
        : verdict === "likely_human"
        ? "Tikėtina žmogaus"
        : "Neaišku";
    const verdictTone =
      verdict === "likely_ai"
        ? "bg-red-600"
        : verdict === "likely_human"
        ? "bg-green-600"
        : "bg-amber-500";
    const barTone =
      probability >= 0.65
        ? "bg-red-500"
        : probability >= 0.35
        ? "bg-amber-500"
        : "bg-green-500";

    return (
      <div className="border rounded-lg p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-semibold flex items-center gap-2">
            <Sparkles className="w-5 h-5" />
            AI generavimo aptikimas
          </h3>
          <Badge className={`${verdictTone} text-white`}>{verdictLabel}</Badge>
        </div>

        <div>
          <div className="flex items-baseline justify-between mb-1">
            <span className="text-sm text-muted-foreground">
              AI tikimybė
            </span>
            <span className="text-2xl font-bold">{percent}%</span>
          </div>
          <div className="h-3 bg-muted rounded-full overflow-hidden">
            <div
              className={`h-full ${barTone} transition-all`}
              style={{ width: `${percent}%` }}
            />
          </div>
        </div>

        {payload.reasoning && (
          <div>
            <h4 className="text-sm font-semibold mb-1">Pagrindimas</h4>
            <p className="text-sm text-muted-foreground whitespace-pre-wrap">
              {payload.reasoning}
            </p>
          </div>
        )}

        {payload.indicators && payload.indicators.length > 0 && (
          <div>
            <h4 className="text-sm font-semibold mb-2">Pastebėti požymiai</h4>
            <ul className="list-disc pl-5 space-y-1 text-sm text-muted-foreground">
              {payload.indicators.map((indicator: string, i: number) => (
                <li key={i}>{indicator}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  };

  const renderAgentResults = () => {
    const agentOutput = result.results as any;

    // Check if we have multiple agent evaluations
    if (agentOutput?.agent_evaluations) {
      const evaluations = agentOutput.agent_evaluations;
      const agentNames = Object.keys(evaluations);

      return (
        <div className="space-y-6">
          {agentNames.map((agentName) => {
            const payload = evaluations[agentName];
            if (isLlmDetectionPayload(payload)) {
              return (
                <React.Fragment key={agentName}>
                  {renderLlmDetection(payload)}
                </React.Fragment>
              );
            }
            return (
              <div key={agentName} className="border rounded-lg p-6">
                <h3 className="font-semibold mb-4 capitalize">
                  {agentName.replace(/_/g, " ")}
                </h3>
                <div className="prose prose-sm dark:prose-invert max-w-none">
                  <pre className="whitespace-pre-wrap text-sm bg-muted/50 p-4 rounded-md overflow-auto">
                    {JSON.stringify(payload, null, 2)}
                  </pre>
                </div>
              </div>
            );
          })}
        </div>
      );
    }

    if (isLlmDetectionPayload(agentOutput)) {
      return renderLlmDetection(agentOutput);
    }

    // Fallback for legacy single agent output
    return (
      <div className="border rounded-lg p-6">
        <h3 className="font-semibold mb-4">Agento analizė</h3>
        <div className="prose prose-sm dark:prose-invert max-w-none">
          <pre className="whitespace-pre-wrap text-sm bg-muted p-4 rounded-md overflow-auto">
            {JSON.stringify(agentOutput, null, 2)}
          </pre>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-2xl font-bold">Vertinimo rezultatai</h2>
          <div className="flex items-center gap-4 mt-2 text-sm text-muted-foreground">
            <span className="capitalize">{result.document_type}</span>
            <span>•</span>
            <span className="capitalize">{result.evaluation_type}</span>
            <span>•</span>
            <span>ID: {result.evaluation_id.slice(0, 8)}</span>
          </div>
        </div>
        <Badge
          variant={
            result.status === "success"
              ? "default"
              : result.status === "error"
              ? "destructive"
              : "secondary"
          }
          className="inline-flex items-center gap-2"
        >
          {result.status === "success" && <CheckCircle2 className="h-4 w-4" />}
          {result.status === "error" && <XCircle className="h-4 w-4" />}
          {result.status !== "success" && result.status !== "error" && (
            <AlertCircle className="h-4 w-4" />
          )}
          {result.status}
        </Badge>
      </div>

      {/* Results */}
      {result.evaluation_type === "scoring"
        ? renderScoringResults()
        : renderAgentResults()}

      {/* Metadata */}
      {result.metadata && Object.keys(result.metadata).length > 0 && (
        <div className="rounded-lg border bg-card p-4">
          <h3 className="text-sm font-semibold mb-2 text-muted-foreground uppercase tracking-wide">
            Metaduomenys
          </h3>
          <dl className="grid grid-cols-2 gap-4 text-sm">
            {Object.entries(result.metadata).map(([key, value]) => (
              <div key={key}>
                <dt className="text-muted-foreground capitalize">
                  {key.replace(/_/g, " ")}
                </dt>
                <dd className="font-medium mt-1">
                  {typeof value === "object"
                    ? JSON.stringify(value)
                    : String(value)}
                </dd>
              </div>
            ))}
          </dl>
        </div>
      )}
    </div>
  );
}
