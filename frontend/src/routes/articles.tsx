import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { DocumentUpload } from "../components/DocumentUpload";
import { EvaluationResults } from "../components/EvaluationResults";
import type { components } from "../api/schema";

type EvaluationResponse = components["schemas"]["UnifiedEvaluationResponse"];

export const Route = createFileRoute("/articles")({
  component: ArticlesPage,
});

function ArticlesPage() {
  const [evaluationResult, setEvaluationResult] =
    useState<EvaluationResponse | null>(null);

  return (
    <div className="container mx-auto px-6 py-8 max-w-6xl">
      <div className="space-y-12">
        {/* Header */}
        <div className="space-y-2">
          <h1 className="text-3xl font-bold tracking-tight">
            Scientific Article Evaluation
          </h1>
          <p className="text-muted-foreground">
            Upload a scientific article to evaluate it against SMSM publication
            standards. Get detailed scores on scientific apparatus, novelty,
            structure, and academic rigor.
          </p>
        </div>

        {/* Upload Section */}
        <DocumentUpload
          onEvaluationComplete={setEvaluationResult}
          documentType="article"
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
