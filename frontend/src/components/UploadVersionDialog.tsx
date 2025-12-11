import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface UploadVersionDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSubmit: (file: File) => Promise<void>;
}

export function UploadVersionDialog({
  open,
  onOpenChange,
  onSubmit,
}: UploadVersionDialogProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) return;

    setUploading(true);
    try {
      await onSubmit(selectedFile);
      onOpenChange(false);
      setSelectedFile(null);
    } catch (err) {
      alert(
        `Nepavyko įkelti versijos: ${
          err instanceof Error ? err.message : "Nežinoma klaida"
        }`
      );
    } finally {
      setUploading(false);
    }
  };

  return (
    <Dialog
      open={open}
      onOpenChange={(open) => {
        onOpenChange(open);
        if (!open) setSelectedFile(null);
      }}
    >
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Įkelti naują versiją</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="document-file">Dokumento failas</Label>
            <Input
              id="document-file"
              type="file"
              onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
              accept=".docx,.pdf,.doc,.txt,.md"
              required
            />
            <p className="text-xs text-muted-foreground">
              Palaikomi formatai: DOCX, PDF, DOC, TXT, MD
            </p>
          </div>
          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => {
                onOpenChange(false);
                setSelectedFile(null);
              }}
              disabled={uploading}
            >
              Atšaukti
            </Button>
            <Button type="submit" disabled={uploading || !selectedFile}>
              {uploading ? "Įkeliama..." : "Įkelti"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
