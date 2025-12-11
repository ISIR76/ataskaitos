import { Link, Outlet, createRootRoute } from "@tanstack/react-router";
import { Home, FolderOpen } from "lucide-react";

export const Route = createRootRoute({
  component: RootLayout,
});

function RootLayout() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Navigation */}
      <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-8">
              <Link to="/" className="text-xl font-bold">
                Ataskaitos
              </Link>
              <div className="flex items-center gap-1">
                <Link
                  to="/"
                  className="px-3 py-2 rounded-md text-sm font-medium hover:bg-muted transition-colors flex items-center gap-2"
                  activeProps={{
                    className: "bg-muted",
                  }}
                >
                  <Home className="h-4 w-4" />
                  Pagrindinis
                </Link>
                <Link
                  to="/projects"
                  className="px-3 py-2 rounded-md text-sm font-medium hover:bg-muted transition-colors flex items-center gap-2"
                  activeProps={{
                    className: "bg-muted",
                  }}
                >
                  <FolderOpen className="h-4 w-4" />
                  Projektai
                </Link>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="border-t py-6 mt-12">
        <div className="container mx-auto px-6">
          <p className="text-center text-sm text-muted-foreground">
            Dirbtinio intelekto valdoma platforma mokslinių dokumentų vertinimui
          </p>
        </div>
      </footer>
    </div>
  );
}
