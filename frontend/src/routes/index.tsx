import { createFileRoute, Link } from "@tanstack/react-router";
import { FileText, FileSearch, ArrowRight } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";

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
            Sveiki atvykę į Ataskaitas
          </h1>
          <p className="text-xl text-muted-foreground">
            Dirbtinio intelekto valdoma platforma mokslinių dokumentų vertinimui
          </p>
        </div>

        {/* Document Type Cards */}
        <div className="grid md:grid-cols-2 gap-6">
          {/* Articles Card */}
          <Link to="/articles" className="group h-full">
            <Card className="hover:shadow-lg transition-all cursor-pointer h-full">
              <CardHeader>
                <div className="flex items-center gap-3">
                  <div className="p-3 rounded-lg bg-primary/10 text-primary">
                    <FileText className="h-6 w-6" />
                  </div>
                  <CardTitle className="text-2xl">Moksliniai straipsniai</CardTitle>
                </div>
                <CardDescription>
                  Įvertinkite mokslinius straipsnius pagal MOKSM publikavimo standartus.
                  Gaukite išsamius balus apie mokslinį aparatą, naujumą, struktūrą
                  ir akademinį griežtumą.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-2 text-primary font-medium group-hover:gap-3 transition-all">
                  <span>Vertinti straipsnį</span>
                  <ArrowRight className="h-4 w-4" />
                </div>
              </CardContent>
            </Card>
          </Link>

          {/* Reports Card */}
          <Link to="/reports" className="group h-full">
            <Card className="hover:shadow-lg transition-all cursor-pointer h-full">
              <CardHeader>
                <div className="flex items-center gap-3">
                  <div className="p-3 rounded-lg bg-primary/10 text-primary">
                    <FileSearch className="h-6 w-6" />
                  </div>
                  <CardTitle className="text-2xl">M&T ataskaitos</CardTitle>
                </div>
                <CardDescription>
                  Įvertinkite M&T veiklos ataskaitas pagal Frascati vadovo standartus.
                  Įvertinkite naujumą, kūrybiškumą, netikrumą ir sistemingą planavimą.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-2 text-primary font-medium group-hover:gap-3 transition-all">
                  <span>Vertinti ataskaitą</span>
                  <ArrowRight className="h-4 w-4" />
                </div>
              </CardContent>
            </Card>
          </Link>
        </div>

        {/* Features */}
        <Card className="bg-muted/50">
          <CardHeader>
            <CardTitle>Funkcijos</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-4 text-sm">
              <div>
                <div className="font-medium mb-1">Keletas vertintojų</div>
                <p className="text-muted-foreground">
                  Išsamus vertinimas pagal kelis kriterijus
                </p>
              </div>
              <div>
                <div className="font-medium mb-1">Detalus pagrindimas</div>
                <p className="text-muted-foreground">
                  Gaukite paaiškinimus kiekvienam vertinimo balui
                </p>
              </div>
              <div>
                <div className="font-medium mb-1">Keli formatai</div>
                <p className="text-muted-foreground">
                  Palaikomi DOCX, PDF, MD ir TXT failai
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
