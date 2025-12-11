import React from "react";
import { CheckCircle2, XCircle, AlertCircle, ChevronDown, ChevronUp } from "lucide-react";
import type { components } from "../api/schema";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";

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
    let color = "text-red-600 dark:text-red-400";
    let bgColor = "bg-red-100 dark:bg-red-900/30";

    if (score >= 0.75) {
      color = "text-green-600 dark:text-green-400";
      bgColor = "bg-green-100 dark:bg-green-900/30";
    } else if (score >= 0.5) {
      color = "text-yellow-600 dark:text-yellow-400";
      bgColor = "bg-yellow-100 dark:bg-yellow-900/30";
    }

    return (
      <div className="flex items-center gap-2">
        <span className={`text-2xl font-bold ${color}`}>{percentage}%</span>
        <div className="flex-1 h-2 bg-muted rounded-full overflow-hidden">
          <div
            className={`h-full ${bgColor} transition-all`}
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
            <Card key={key}>
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
                <CardContent className="pt-2 border-t">
                  <p className="text-sm text-muted-foreground whitespace-pre-wrap">
                    {reason}
                  </p>
                </CardContent>
              )}
            </Card>
          );
        })}
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
          {agentNames.map((agentName) => (
            <Card key={agentName}>
              <CardHeader>
                <CardTitle className="capitalize">
                  {agentName.replace(/_/g, " ")}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="prose prose-sm dark:prose-invert max-w-none">
                  <pre className="whitespace-pre-wrap text-sm bg-muted/50 p-4 rounded-md overflow-auto">
                    {JSON.stringify(evaluations[agentName], null, 2)}
                  </pre>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      );
    }

    // Fallback for legacy single agent output
    return (
      <Card>
        <CardHeader>
          <CardTitle>Agento analizė</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="prose prose-sm dark:prose-invert max-w-none">
            <pre className="whitespace-pre-wrap text-sm bg-muted p-4 rounded-md overflow-auto">
              {JSON.stringify(agentOutput, null, 2)}
            </pre>
          </div>
        </CardContent>
      </Card>
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
        <div
          className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium ${
            result.status === "success"
              ? "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400"
              : result.status === "error"
              ? "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400"
              : "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400"
          }`}
        >
          {result.status === "success" && <CheckCircle2 className="h-4 w-4" />}
          {result.status === "error" && <XCircle className="h-4 w-4" />}
          {result.status !== "success" && result.status !== "error" && (
            <AlertCircle className="h-4 w-4" />
          )}
          {result.status}
        </div>
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
