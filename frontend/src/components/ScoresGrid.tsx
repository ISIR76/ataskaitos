import { useMemo, useState } from "react";
import { Link } from "@tanstack/react-router";
import { CheckCircle2, ArrowDown, ArrowUp } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { ScoresGrid as ScoresGridData } from "../api/projects";

type SortKey = "name" | "good" | string;
type SortDir = "asc" | "desc";

interface ScoresGridProps {
  data: ScoresGridData;
}

function scoreColor(value: number): string {
  if (value >= 0.75) return "bg-green-100 text-green-900";
  if (value >= 0.5) return "bg-amber-100 text-amber-900";
  if (value >= 0.25) return "bg-orange-100 text-orange-900";
  return "bg-red-100 text-red-900";
}

function formatHeader(name: string): string {
  return name
    .replace(/_score$/, "")
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

export function ScoresGrid({ data }: ScoresGridProps) {
  const [filter, setFilter] = useState("");
  const [sortKey, setSortKey] = useState<SortKey>("name");
  const [sortDir, setSortDir] = useState<SortDir>("asc");

  const visibleRows = useMemo(() => {
    const filtered = filter.trim()
      ? data.rows.filter((r) =>
          r.project_name.toLowerCase().includes(filter.toLowerCase())
        )
      : data.rows;

    const sorted = [...filtered].sort((a, b) => {
      let cmp = 0;
      if (sortKey === "name") {
        cmp = a.project_name.localeCompare(b.project_name);
      } else if (sortKey === "good") {
        cmp = Number(a.is_marked_good) - Number(b.is_marked_good);
      } else {
        const av = (a.scores ?? {})[sortKey];
        const bv = (b.scores ?? {})[sortKey];
        if (av == null && bv == null) cmp = 0;
        else if (av == null) cmp = 1;
        else if (bv == null) cmp = -1;
        else cmp = av - bv;
      }
      return sortDir === "asc" ? cmp : -cmp;
    });
    return sorted;
  }, [data.rows, filter, sortKey, sortDir]);

  const toggleSort = (key: SortKey) => {
    if (sortKey === key) {
      setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    } else {
      setSortKey(key);
      setSortDir(key === "name" ? "asc" : "desc");
    }
  };

  const SortIcon = ({ k }: { k: SortKey }) =>
    sortKey === k ? (
      sortDir === "asc" ? (
        <ArrowUp className="inline w-3 h-3 ml-1" />
      ) : (
        <ArrowDown className="inline w-3 h-3 ml-1" />
      )
    ) : null;

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <Input
          placeholder="Filtruoti pagal pavadinimą..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="max-w-sm"
        />
        <span className="text-sm text-muted-foreground">
          {visibleRows.length} / {data.rows.length} projektų
        </span>
      </div>

      <div className="border rounded-lg overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead
                className="sticky left-0 bg-background cursor-pointer"
                onClick={() => toggleSort("name")}
              >
                Projektas
                <SortIcon k="name" />
              </TableHead>
              <TableHead
                className="cursor-pointer"
                onClick={() => toggleSort("good")}
              >
                Žymėta
                <SortIcon k="good" />
              </TableHead>
              {data.evaluators.map((ev) => (
                <TableHead
                  key={ev}
                  className="cursor-pointer text-right"
                  onClick={() => toggleSort(ev)}
                  title={ev}
                >
                  {formatHeader(ev)}
                  <SortIcon k={ev} />
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {visibleRows.length === 0 ? (
              <TableRow>
                <TableCell
                  colSpan={2 + data.evaluators.length}
                  className="text-center text-muted-foreground py-8"
                >
                  Nėra projektų pagal filtrą
                </TableCell>
              </TableRow>
            ) : (
              visibleRows.map((row) => (
                <TableRow key={row.project_id}>
                  <TableCell className="sticky left-0 bg-background font-medium">
                    <Link
                      to="/projects/$projectId"
                      params={{ projectId: String(row.project_id) }}
                      className="hover:underline"
                    >
                      {row.project_name}
                    </Link>
                    {row.evaluation_id && (
                      <Link
                        to="/projects/$projectId/evaluations/$evaluationId"
                        params={{
                          projectId: String(row.project_id),
                          evaluationId: row.evaluation_id,
                        }}
                        className="block text-xs text-muted-foreground hover:underline"
                      >
                        Vertinimas →
                      </Link>
                    )}
                  </TableCell>
                  <TableCell>
                    {row.is_marked_good ? (
                      <Badge className="bg-green-600 hover:bg-green-700 text-white">
                        <CheckCircle2 className="w-3 h-3 mr-1" />
                        Gera
                      </Badge>
                    ) : (
                      <span className="text-muted-foreground">—</span>
                    )}
                  </TableCell>
                  {data.evaluators.map((ev) => {
                    const value = (row.scores ?? {})[ev];
                    if (value == null) {
                      return (
                        <TableCell
                          key={ev}
                          className="text-right text-muted-foreground"
                        >
                          —
                        </TableCell>
                      );
                    }
                    return (
                      <TableCell key={ev} className="text-right">
                        <span
                          className={`inline-block px-2 py-1 rounded text-sm font-medium ${scoreColor(
                            value
                          )}`}
                        >
                          {Math.round(value * 100)}%
                        </span>
                      </TableCell>
                    );
                  })}
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
