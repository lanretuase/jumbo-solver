import type { MatchResult, SolveResponse } from '../types';

function triggerDownload(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();
  document.body.removeChild(anchor);
  URL.revokeObjectURL(url);
}

export function exportCSV(matches: MatchResult[], filename: string): void {
  const header = 'Word,Length,Type\n';
  const rows = matches
    .map((m) => `"${m.word}",${m.length},"${m.type === 'full_anagram' ? 'Full Anagram' : 'Sub-Anagram'}"`)
    .join('\n');
  const csv = header + rows;
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  triggerDownload(blob, filename.endsWith('.csv') ? filename : `${filename}.csv`);
}

export function exportJSON(response: SolveResponse, filename: string): void {
  const json = JSON.stringify(response, null, 2);
  const blob = new Blob([json], { type: 'application/json;charset=utf-8;' });
  triggerDownload(blob, filename.endsWith('.json') ? filename : `${filename}.json`);
}
