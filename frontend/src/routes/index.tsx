import { createFileRoute, Link } from "@tanstack/react-router";
import { FileText, FileSearch, ArrowRight } from "lucide-react";

export const Route = createFileRoute("/")({
  component: HomePage,
});

function HomePage() {
  return (
    <div className="container mx-auto px-6 py-12">
      <div className="max-w-4xl mx-auto space-y-12">
        {/* Hero Section */}
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold tracking-tight">
            Welcome to Ataskaitos
          </h1>
          <p className="text-xl text-muted-foreground">
            AI-powered evaluation platform for scientific documents
          </p>
        </div>

        {/* Document Type Cards */}
        <div className="grid md:grid-cols-2 gap-6">
          {/* Articles Card */}
          <Link to="/articles">
            <div className="group rounded-lg border bg-card p-6 hover:shadow-lg transition-all cursor-pointer h-full">
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <div className="p-3 rounded-lg bg-primary/10 text-primary">
                    <FileText className="h-6 w-6" />
                  </div>
                  <h2 className="text-2xl font-semibold">Scientific Articles</h2>
                </div>
                <p className="text-muted-foreground">
                  Evaluate scientific articles against SMSM publication standards.
                  Get detailed scores on scientific apparatus, novelty, structure,
                  and academic rigor.
                </p>
                <div className="flex items-center gap-2 text-primary font-medium group-hover:gap-3 transition-all">
                  <span>Evaluate Article</span>
                  <ArrowRight className="h-4 w-4" />
                </div>
              </div>
            </div>
          </Link>

          {/* Reports Card */}
          <Link to="/reports">
            <div className="group rounded-lg border bg-card p-6 hover:shadow-lg transition-all cursor-pointer h-full">
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <div className="p-3 rounded-lg bg-primary/10 text-primary">
                    <FileSearch className="h-6 w-6" />
                  </div>
                  <h2 className="text-2xl font-semibold">R&D Reports</h2>
                </div>
                <p className="text-muted-foreground">
                  Evaluate R&D activity reports against Frascati Manual standards.
                  Assess novelty, creativity, uncertainty, and systematic planning.
                </p>
                <div className="flex items-center gap-2 text-primary font-medium group-hover:gap-3 transition-all">
                  <span>Evaluate Report</span>
                  <ArrowRight className="h-4 w-4" />
                </div>
              </div>
            </div>
          </Link>
        </div>

        {/* Features */}
        <div className="rounded-lg border bg-muted/50 p-6">
          <h3 className="text-lg font-semibold mb-4">Features</h3>
          <div className="grid md:grid-cols-3 gap-4 text-sm">
            <div>
              <div className="font-medium mb-1">Multiple Evaluators</div>
              <p className="text-muted-foreground">
                Comprehensive scoring across multiple criteria
              </p>
            </div>
            <div>
              <div className="font-medium mb-1">Detailed Reasoning</div>
              <p className="text-muted-foreground">
                Get explanations for each evaluation score
              </p>
            </div>
            <div>
              <div className="font-medium mb-1">Multiple Formats</div>
              <p className="text-muted-foreground">
                Support for DOCX, PDF, MD, and TXT files
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
