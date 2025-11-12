import React, { useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";
import type { components } from "../api/schema";

type EvaluatorInfo = components["schemas"]["EvaluatorInfo"];

interface EvaluatorsListProps {
  evaluators: EvaluatorInfo[];
  documentType: string;
}

export function EvaluatorsList({ evaluators, documentType }: EvaluatorsListProps) {
  const [expandedRows, setExpandedRows] = useState<Set<string>>(new Set());

  const toggleRow = (key: string) => {
    setExpandedRows((prev) => {
      const next = new Set(prev);
      if (next.has(key)) {
        next.delete(key);
      } else {
        next.add(key);
      }
      return next;
    });
  };

  const getFirstLine = (text: string | null | undefined): string => {
    if (!text) return "No description available";
    const firstLine = text.trim().split("\n")[0];
    return firstLine.length > 100 ? firstLine.substring(0, 100) + "..." : firstLine;
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Available Evaluators</h2>
        <span className="text-sm text-muted-foreground">
          {evaluators.length} evaluators
        </span>
      </div>

      <div className="rounded-md border">
        <table className="w-full">
          <thead>
            <tr className="border-b bg-muted/50">
              <th className="h-12 w-12 px-4 text-left align-middle font-medium text-muted-foreground"></th>
              <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">
                Name
              </th>
              <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">
                Description
              </th>
            </tr>
          </thead>
          <tbody>
            {evaluators.map((evaluator, idx) => {
              const rowKey = `${documentType}-${idx}`;
              const isExpanded = expandedRows.has(rowKey);

              return (
                <React.Fragment key={rowKey}>
                  <tr
                    className="border-b transition-colors hover:bg-muted/50 cursor-pointer"
                    onClick={() => toggleRow(rowKey)}
                  >
                    <td className="p-4 align-middle">
                      <button
                        className="text-muted-foreground hover:text-foreground"
                        onClick={(e) => {
                          e.stopPropagation();
                          toggleRow(rowKey);
                        }}
                      >
                        {isExpanded ? (
                          <ChevronUp className="h-4 w-4" />
                        ) : (
                          <ChevronDown className="h-4 w-4" />
                        )}
                      </button>
                    </td>
                    <td className="p-4 align-middle font-medium">
                      <span className="capitalize">
                        {evaluator.name.replace(/_/g, " ")}
                      </span>
                      {evaluator.has_assertion && (
                        <span className="ml-2 inline-flex items-center rounded-full px-2 py-0.5 text-xs font-semibold bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400">
                          Has Assertion
                        </span>
                      )}
                    </td>
                    <td className="p-4 align-middle text-sm text-muted-foreground">
                      {getFirstLine(evaluator.rubric)}
                    </td>
                  </tr>
                  {isExpanded && evaluator.rubric && (
                    <tr className="border-b bg-muted/20">
                      <td colSpan={3} className="p-6">
                        <div className="space-y-2">
                          <h4 className="font-semibold text-sm text-muted-foreground uppercase tracking-wide">
                            Complete Rubric
                          </h4>
                          <pre className="whitespace-pre-wrap text-sm bg-background rounded-md p-4 border overflow-auto max-h-96">
                            {evaluator.rubric}
                          </pre>
                        </div>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
