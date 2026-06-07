import { useState } from 'react';
import { solveJumble } from '../api/solver';
import type { SolveMode, SolveResponse } from '../types';

export function useSolver(onSuccess?: (letters: string, totalMatches: number, mode: SolveMode) => void) {
  const [results, setResults] = useState<SolveResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const solve = async (letters: string, mode?: SolveMode) => {
    if (!letters.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const data = await solveJumble(letters.trim(), mode);
      setResults(data);
      if (onSuccess) {
        onSuccess(letters.trim(), data.total_matches, data.mode);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
      setResults(null);
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setResults(null);
    setError(null);
  };

  return { results, loading, error, solve, reset } as const;
}
