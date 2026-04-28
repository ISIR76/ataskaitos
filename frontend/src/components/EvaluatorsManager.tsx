import { useEffect, useState } from "react";
import { Pencil, Plus, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  createEvaluator,
  deleteEvaluator,
  fetchEvaluators,
  setEvaluatorActive,
  updateEvaluator,
  type DocumentType,
  type EvaluatorRecord,
} from "@/api/evaluators";

type DraftMode = "create" | "edit";

interface DraftState {
  mode: DraftMode;
  id?: number;
  name: string;
  document_type: DocumentType;
  rubric: string;
  has_assertion: boolean;
  source: "default" | "custom";
}

const EMPTY_DRAFT = (documentType: DocumentType): DraftState => ({
  mode: "create",
  name: "",
  document_type: documentType,
  rubric: "",
  has_assertion: false,
  source: "custom",
});

export function EvaluatorsManager() {
  const [tab, setTab] = useState<DocumentType>("article");
  const [rows, setRows] = useState<EvaluatorRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [draft, setDraft] = useState<DraftState | null>(null);
  const [saving, setSaving] = useState(false);

  const reload = async (documentType: DocumentType) => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchEvaluators(documentType);
      setRows(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Klaida įkeliant vertintojus");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void reload(tab);
  }, [tab]);

  const openCreate = () => setDraft(EMPTY_DRAFT(tab));

  const openEdit = (row: EvaluatorRecord) =>
    setDraft({
      mode: "edit",
      id: row.id,
      name: row.name,
      document_type: row.document_type,
      rubric: row.rubric,
      has_assertion: row.has_assertion,
      source: row.source,
    });

  const closeDraft = () => setDraft(null);

  const handleSave = async () => {
    if (!draft) return;
    setSaving(true);
    try {
      if (draft.mode === "create") {
        await createEvaluator({
          name: draft.name.trim(),
          document_type: draft.document_type,
          rubric: draft.rubric,
          has_assertion: draft.has_assertion,
        });
      } else if (draft.id != null) {
        await updateEvaluator(draft.id, {
          name: draft.source === "custom" ? draft.name.trim() : undefined,
          rubric: draft.rubric,
          has_assertion: draft.has_assertion,
        });
      }
      closeDraft();
      await reload(tab);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Klaida išsaugant vertintoją");
    } finally {
      setSaving(false);
    }
  };

  const handleToggleActive = async (row: EvaluatorRecord) => {
    try {
      await setEvaluatorActive(row.id, !row.is_active);
      await reload(tab);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Klaida keičiant būseną");
    }
  };

  const handleDelete = async (row: EvaluatorRecord) => {
    if (row.source === "default") return;
    if (!confirm(`Ištrinti vertintoją "${row.name}"?`)) return;
    try {
      await deleteEvaluator(row.id);
      await reload(tab);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Klaida trinant vertintoją");
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between gap-4">
        <div className="flex gap-2">
          <Button
            variant={tab === "article" ? "default" : "outline"}
            onClick={() => setTab("article")}
          >
            Straipsniai
          </Button>
          <Button
            variant={tab === "report" ? "default" : "outline"}
            onClick={() => setTab("report")}
          >
            Ataskaitos
          </Button>
        </div>
        <Button onClick={openCreate}>
          <Plus className="w-4 h-4 mr-2" />
          Naujas vertintojas
        </Button>
      </div>

      {error && (
        <div className="rounded-lg border border-destructive bg-destructive/10 p-3 text-sm text-destructive">
          {error}
        </div>
      )}

      <div className="border rounded-lg">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Pavadinimas</TableHead>
              <TableHead>Šaltinis</TableHead>
              <TableHead>Tvirtinimas</TableHead>
              <TableHead>Aktyvus</TableHead>
              <TableHead className="text-right">Veiksmai</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={5} className="text-center text-muted-foreground py-8">
                  Įkeliama...
                </TableCell>
              </TableRow>
            ) : rows.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} className="text-center text-muted-foreground py-8">
                  Nėra vertintojų
                </TableCell>
              </TableRow>
            ) : (
              rows.map((row) => (
                <TableRow key={row.id}>
                  <TableCell className="font-medium font-mono text-sm">{row.name}</TableCell>
                  <TableCell>
                    <Badge variant={row.source === "default" ? "secondary" : "default"}>
                      {row.source === "default" ? "Numatytasis" : "Vartotojo"}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    {row.has_assertion ? (
                      <Badge variant="outline">Su tvirtinimu</Badge>
                    ) : (
                      <span className="text-muted-foreground text-sm">—</span>
                    )}
                  </TableCell>
                  <TableCell>
                    <Checkbox
                      checked={row.is_active}
                      onCheckedChange={() => handleToggleActive(row)}
                    />
                  </TableCell>
                  <TableCell className="text-right">
                    <div className="flex justify-end gap-1">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => openEdit(row)}
                        title="Redaguoti"
                      >
                        <Pencil className="w-4 h-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleDelete(row)}
                        disabled={row.source === "default"}
                        title={
                          row.source === "default"
                            ? "Numatytųjų vertintojų negalima ištrinti"
                            : "Ištrinti"
                        }
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>

      <Dialog open={draft !== null} onOpenChange={(open) => !open && closeDraft()}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>
              {draft?.mode === "create" ? "Naujas vertintojas" : "Redaguoti vertintoją"}
            </DialogTitle>
          </DialogHeader>

          {draft && (
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="evaluator-name">Pavadinimas</Label>
                <Input
                  id="evaluator-name"
                  value={draft.name}
                  disabled={draft.mode === "edit" && draft.source === "default"}
                  onChange={(e) => setDraft({ ...draft, name: e.target.value })}
                  placeholder="pvz. clarity_score"
                />
                {draft.mode === "edit" && draft.source === "default" && (
                  <p className="text-xs text-muted-foreground">
                    Numatytųjų vertintojų pavadinimo keisti negalima.
                  </p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="evaluator-rubric">Vertinimo kriterijai (rubric)</Label>
                <textarea
                  id="evaluator-rubric"
                  value={draft.rubric}
                  onChange={(e) => setDraft({ ...draft, rubric: e.target.value })}
                  rows={12}
                  className="w-full font-mono text-sm rounded-md border border-input bg-background px-3 py-2 focus:outline-none focus:ring-2 focus:ring-ring"
                  placeholder="Įvertinkite..."
                />
              </div>

              <div className="flex items-center gap-2">
                <Checkbox
                  id="has-assertion"
                  checked={draft.has_assertion}
                  onCheckedChange={(v) =>
                    setDraft({ ...draft, has_assertion: Boolean(v) })
                  }
                />
                <Label htmlFor="has-assertion" className="cursor-pointer">
                  Generuoti tvirtinimą (qualified/not qualified)
                </Label>
              </div>
            </div>
          )}

          <DialogFooter>
            <Button variant="outline" onClick={closeDraft} disabled={saving}>
              Atšaukti
            </Button>
            <Button onClick={handleSave} disabled={saving || !draft?.name || !draft?.rubric}>
              {saving ? "Saugoma..." : "Išsaugoti"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
