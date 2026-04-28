import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { ScoresGrid } from "@/components/ScoresGrid";
import { Button } from "@/components/ui/button";
import { fetchScoresGrid } from "../api/projects";

export const Route = createFileRoute("/scores")({
  loader: async () => {
    const [articles, reports] = await Promise.all([
      fetchScoresGrid("article"),
      fetchScoresGrid("report"),
    ]);
    return { articles, reports };
  },
  component: ScoresPage,
  pendingComponent: () => (
    <div className="container mx-auto p-8 text-center">
      Įkeliama vertinimų lentelė...
    </div>
  ),
  errorComponent: ({ error }) => (
    <div className="container mx-auto p-8 text-center text-destructive">
      Klaida: {error.message}
    </div>
  ),
});

function ScoresPage() {
  const { articles, reports } = Route.useLoaderData();
  const [tab, setTab] = useState<"article" | "report">("article");
  const data = tab === "article" ? articles : reports;

  return (
    <ProtectedRoute>
      <div className="container mx-auto p-8 space-y-6">
        <div>
          <h1 className="text-3xl font-bold mb-2">Vertinimų lentelė</h1>
          <p className="text-muted-foreground">
            Visi projektai ir naujausi jų vertintojų balai vienoje vietoje.
          </p>
        </div>

        <div className="flex gap-2">
          <Button
            variant={tab === "article" ? "default" : "outline"}
            onClick={() => setTab("article")}
          >
            Straipsniai ({articles.rows.length})
          </Button>
          <Button
            variant={tab === "report" ? "default" : "outline"}
            onClick={() => setTab("report")}
          >
            Ataskaitos ({reports.rows.length})
          </Button>
        </div>

        {data.rows.length === 0 ? (
          <div className="border rounded-lg p-12 text-center text-muted-foreground">
            Dar nėra projektų su vertinimo balais.
          </div>
        ) : (
          <ScoresGrid data={data} />
        )}
      </div>
    </ProtectedRoute>
  );
}
