import { Link, Outlet, createRootRoute, useNavigate } from "@tanstack/react-router";
import { Home, FolderOpen, LogOut, User, Grid3x3 } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";

export const Route = createRootRoute({
  component: RootLayout,
});

function RootLayout() {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate({ to: "/auth" });
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Navigation */}
      <nav className="bg-background sticky top-0 z-50 border-b">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-8">
              <Link to="/" className="text-xl font-bold">
                Ataskaitos
              </Link>
              {isAuthenticated && (
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
                  <Link
                    to="/scores"
                    className="px-3 py-2 rounded-md text-sm font-medium hover:bg-muted transition-colors flex items-center gap-2"
                    activeProps={{
                      className: "bg-muted",
                    }}
                  >
                    <Grid3x3 className="h-4 w-4" />
                    Vertinimų lentelė
                  </Link>
                </div>
              )}
            </div>

            {isAuthenticated && user && (
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <User className="h-4 w-4" />
                  <span>{user.email}</span>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleLogout}
                  className="flex items-center gap-2"
                >
                  <LogOut className="h-4 w-4" />
                  Atsijungti
                </Button>
              </div>
            )}
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
