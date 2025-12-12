import { useState, useCallback } from "react";

/**
 * Hook for managing dialog/modal state.
 * Returns the open state and helper functions to open/close the dialog.
 */
export function useDialog(initialState = false) {
  const [isOpen, setIsOpen] = useState(initialState);

  const open = useCallback(() => setIsOpen(true), []);
  const close = useCallback(() => setIsOpen(false), []);
  const toggle = useCallback(() => setIsOpen((prev) => !prev), []);

  return {
    isOpen,
    open,
    close,
    toggle,
    setIsOpen,
  };
}
