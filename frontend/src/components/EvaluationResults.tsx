import React from "react";
import { CheckCircle2, XCircle, AlertCircle, ChevronDown, ChevronUp } from "lucide-react";
import type { components } from "../api/schema";

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

    // Check if we have cases with scores
    if (!resultData?.cases || resultData.cases.length === 0) {
      return (
        <div className="rounded-lg border border-yellow-200 bg-yellow-50 dark:bg-yellow-900/20 p-4">
          <p className="text-sm text-yellow-800 dark:text-yellow-200">
            No evaluation scores available. The document may have failed to process.
          </p>
        </div>
      );
    }

    // Get scores from the first case (our uploaded document)
    const caseData = resultData.cases[0];
    const scores = caseData?.scores || {};

    if (Object.keys(scores).length === 0) {
      return (
        <div className="rounded-lg border border-yellow-200 bg-yellow-50 dark:bg-yellow-900/20 p-4">
          <p className="text-sm text-yellow-800 dark:text-yellow-200">
            No scores found in evaluation results.
          </p>
        </div>
      );
    }

    return (
      <div className="space-y-4">
        {Object.entries(scores).map(([key, scoreData]: [string, any]) => {
          const isExpanded = expandedSections.has(key);
          const score = scoreData?.value || 0;
          const reason = scoreData?.reason || "";

          return (
            <div
              key={key}
              className="rounded-lg border bg-card overflow-hidden"
            >
              <button
                onClick={() => toggleSection(key)}
                className="w-full p-4 flex items-center justify-between hover:bg-muted/50 transition-colors"
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
              </button>

              {isExpanded && reason && (
                <div className="px-4 pb-4 pt-2 border-t bg-muted/20">
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

  const renderAgentResults = () => {
    const agentOutput = result.results as any;

    // Check if we have multiple agent evaluations
    if (agentOutput?.agent_evaluations) {
      const evaluations = agentOutput.agent_evaluations;
      const agentNames = Object.keys(evaluations);

      return (
        <div className="space-y-6">
          {agentNames.map((agentName) => (
            <div key={agentName} className="rounded-lg border bg-card overflow-hidden">
              <div className="bg-muted/30 px-6 py-3 border-b">
                <h3 className="text-lg font-semibold capitalize">
                  {agentName.replace(/_/g, " ")}
                </h3>
              </div>
              <div className="p-6">
                <div className="prose prose-sm dark:prose-invert max-w-none">
                  <pre className="whitespace-pre-wrap text-sm bg-muted/50 p-4 rounded-md overflow-auto">
                    {JSON.stringify(evaluations[agentName], null, 2)}
                  </pre>
                </div>
              </div>
            </div>
          ))}
        </div>
      );
    }

    // Fallback for legacy single agent output
    return (
      <div className="rounded-lg border bg-card p-6">
        <h3 className="text-lg font-semibold mb-4">Agent Analysis</h3>
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
          <h2 className="text-2xl font-bold">Evaluation Results</h2>
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
            Metadata
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
