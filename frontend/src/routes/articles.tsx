import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { ProtectedRoute } from "@/components/ProtectedRoute";

export const Route = createFileRoute("/articles")({
  component: DeprecatedPage,
});

function DeprecatedPage() {
  const navigate = useNavigate();
  return (
    <ProtectedRoute>
      <div className="container mx-auto p-8">
        <Alert>
          <AlertDescription>
            Ši funkcija perkelta. Dabar visi vertinimai atliekami per projektus.
          </AlertDescription>
        </Alert>
        <div className="mt-4">
          <Button onClick={() => navigate({ to: "/projects" })}>
            Eiti į projektus
          </Button>
        </div>
      </div>
    </ProtectedRoute>
  );
}
