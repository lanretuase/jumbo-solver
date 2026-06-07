import type { ModeInfo, SolveResponse } from '../types';

/**
 * Call the FastAPI backend to solve a jumble.
 */
export async function solveJumble(letters: string, mode?: string): Promise<SolveResponse> {
  const payload = mode ? { letters, mode } : { letters };
  const response = await fetch('/api/solve', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    let errorDetail = 'Failed to solve jumble';
    try {
      const errorData = await response.json();
      if (errorData.detail) {
        errorDetail = typeof errorData.detail === 'string' 
          ? errorData.detail 
          : JSON.stringify(errorData.detail);
      }
    } catch {
      // Ignore JSON parse errors
    }
    throw new Error(errorDetail);
  }

  return response.json();
}

/**
 * Fetch available solving modes from the backend.
 */
export async function fetchModes(): Promise<ModeInfo[]> {
  const response = await fetch('/api/modes');
  if (!response.ok) {
    throw new Error('Failed to fetch modes');
  }
  return response.json();
}
