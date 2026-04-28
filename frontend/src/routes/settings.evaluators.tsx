import { createFileRoute } from "@tanstack/react-router";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { EvaluatorsManager } from "@/components/EvaluatorsManager";

export const Route = createFileRoute("/settings/evaluators")({
  component: EvaluatorsSettingsPage,
});

function EvaluatorsSettingsPage() {
  return (
    <ProtectedRoute>
      <div className="container mx-auto p-8 space-y-6">
        <div>
          <h1 className="text-3xl font-bold mb-2">Vertintojų valdymas</h1>
          <p className="text-muted-foreground">
            Redaguokite vertinimo kriterijus, įjunkite ar išjunkite numatytuosius
            vertintojus, pridėkite savo. Pakeitimai įsigalioja kitam vertinimui.
          </p>
        </div>
        <EvaluatorsManager />
      </div>
    </ProtectedRoute>
  );
}
