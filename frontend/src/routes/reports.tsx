import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { DocumentUpload } from "../components/DocumentUpload";
import { EvaluationResults } from "../components/EvaluationResults";
import type { components } from "../api/schema";

type EvaluationResponse = components["schemas"]["UnifiedEvaluationResponse"];

export const Route = createFileRoute("/reports")({
  component: ReportsPage,
});

function ReportsPage() {
  const [evaluationResult, setEvaluationResult] =
    useState<EvaluationResponse | null>(null);

  return (
    <div className="container mx-auto px-6 py-8 max-w-6xl">
      <div className="space-y-12">
        {/* Header */}
        <div className="space-y-2">
          <h1 className="text-3xl font-bold tracking-tight">
            R&D Activity Report Evaluation
          </h1>
          <p className="text-muted-foreground">
            Upload an R&D activity report to evaluate it against Frascati Manual
            standards. Assess novelty, creativity, uncertainty, systematic planning,
            and transferability.
          </p>
        </div>

        {/* Upload Section */}
        <DocumentUpload
          onEvaluationComplete={setEvaluationResult}
          documentType="report"
          hideDocumentTypeSelector
        />

        {/* Results Section */}
        {evaluationResult && (
          <div className="pt-8 border-t">
            <EvaluationResults result={evaluationResult} />
          </div>
        )}
      </div>
    </div>
  );
}
