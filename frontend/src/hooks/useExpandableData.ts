import { useState, useCallback } from "react";

/**
 * Hook for managing expandable items with lazy-loaded data.
 * Handles expand/collapse state, data loading, and caching.
 */
export function useExpandableData<TId extends string | number, TData>() {
  const [expandedId, setExpandedId] = useState<TId | null>(null);
  const [dataCache, setDataCache] = useState<Record<string, TData>>({});

  const toggle = useCallback(
    async (id: TId, loadData?: () => Promise<TData>) => {
      if (expandedId === id) {
        // Collapse if already expanded
        setExpandedId(null);
      } else {
        // Expand the item
        setExpandedId(id);

        // Load data if not cached and loader is provided
        const cacheKey = String(id);
        if (loadData && !dataCache[cacheKey]) {
          try {
            const data = await loadData();
            setDataCache((prev) => ({
              ...prev,
              [cacheKey]: data,
            }));
          } catch (err) {
            console.error("Failed to load data:", err);
          }
        }
      }
    },
    [expandedId, dataCache]
  );

  const getData = useCallback(
    (id: TId): TData | undefined => {
      return dataCache[String(id)];
    },
    [dataCache]
  );

  const isExpanded = useCallback(
    (id: TId): boolean => {
      return expandedId === id;
    },
    [expandedId]
  );

  return {
    expandedId,
    toggle,
    getData,
    isExpanded,
    setExpandedId,
  };
}
