import { useState, useCallback, useEffect } from 'react';
import type { HistoryEntry } from '../types';

const STORAGE_KEY = 'jumble-solver-history';
const MAX_ENTRIES = 20;

function loadHistory(): HistoryEntry[] {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) return [];
    const parsed = JSON.parse(stored) as HistoryEntry[];
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function saveHistory(entries: HistoryEntry[]): void {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(entries));
}

export function useHistory() {
  const [history, setHistory] = useState<HistoryEntry[]>(loadHistory);

  useEffect(() => {
    saveHistory(history);
  }, [history]);

  const addEntry = useCallback((letters: string, totalMatches: number, mode?: import('../types').SolveMode) => {
    setHistory((prev) => {
      const filtered = prev.filter(
        (entry) => entry.letters.toLowerCase() !== letters.toLowerCase()
      );
      const newEntry: HistoryEntry = {
        letters: letters.toUpperCase(),
        total_matches: totalMatches,
        timestamp: Date.now(),
        mode,
      };
      return [newEntry, ...filtered].slice(0, MAX_ENTRIES);
    });
  }, []);

  const clearHistory = useCallback(() => {
    setHistory([]);
  }, []);

  return { history, addEntry, clearHistory } as const;
}
