import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAuth } from "@/contexts/AuthContext";
import { Loader2 } from "lucide-react";

interface RegisterFormProps {
  onSwitchToLogin?: () => void;
}

export function RegisterForm({ onSwitchToLogin }: RegisterFormProps) {
  const { register, error, isLoading } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [localError, setLocalError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLocalError(null);

    if (!email || !password || !confirmPassword) {
      setLocalError("Visi laukai yra privalomi");
      return;
    }

    if (password !== confirmPassword) {
      setLocalError("Slaptažodžiai nesutampa");
      return;
    }

    if (password.length < 8) {
      setLocalError("Slaptažodis turi būti bent 8 simbolių");
      return;
    }

    try {
      await register(email, password);
    } catch (err) {
      // Error is handled by AuthContext
      console.error("Registration failed:", err);
    }
  };

  const displayError = localError || error;

  return (
    <div className="w-full max-w-md space-y-6">
      <div className="space-y-2 text-center">
        <h1 className="text-3xl font-bold">Registracija</h1>
        <p className="text-muted-foreground">
          Sukurkite naują paskyrą
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="reg-email">El. paštas</Label>
          <Input
            id="reg-email"
            type="email"
            placeholder="vardas@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={isLoading}
            required
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="reg-password">Slaptažodis</Label>
          <Input
            id="reg-password"
            type="password"
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={isLoading}
            required
            minLength={8}
          />
          <p className="text-xs text-muted-foreground">
            Bent 8 simboliai
          </p>
        </div>

        <div className="space-y-2">
          <Label htmlFor="reg-confirm-password">Pakartokite slaptažodį</Label>
          <Input
            id="reg-confirm-password"
            type="password"
            placeholder="••••••••"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            disabled={isLoading}
            required
          />
        </div>

        {displayError && (
          <div className="rounded-lg border border-destructive bg-destructive/10 p-3">
            <p className="text-sm text-destructive">{displayError}</p>
          </div>
        )}

        <Button
          type="submit"
          className="w-full"
          disabled={isLoading}
        >
          {isLoading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Registruojama...
            </>
          ) : (
            "Registruotis"
          )}
        </Button>
      </form>

      {onSwitchToLogin && (
        <div className="text-center text-sm">
          <span className="text-muted-foreground">Jau turite paskyrą? </span>
          <button
            type="button"
            onClick={onSwitchToLogin}
            className="text-primary hover:underline"
          >
            Prisijungti
          </button>
        </div>
      )}
    </div>
  );
}
