import { useRouter } from "@tanstack/react-router";
import { useCallback } from "react";

/**
 * Hook that wraps a mutation function and automatically invalidates the router after completion.
 * Useful for operations that modify data and need to trigger a route reload.
 */
export function useRouterMutation<TArgs extends unknown[], TReturn>(
  mutationFn: (...args: TArgs) => Promise<TReturn>
) {
  const router = useRouter();

  return useCallback(
    async (...args: TArgs): Promise<TReturn> => {
      const result = await mutationFn(...args);
      await router.invalidate();
      return result;
    },
    [mutationFn, router]
  );
}
