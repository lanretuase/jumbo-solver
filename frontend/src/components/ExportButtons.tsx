import type { MatchResult, SolveResponse } from '../types';
import { exportCSV, exportJSON } from '../utils/export';

interface ExportButtonsProps {
  matches: MatchResult[];
  response: SolveResponse;
  inputLetters: string;
}

export default function ExportButtons({ matches, response, inputLetters }: ExportButtonsProps) {
  if (matches.length === 0) return null;

  const filename = `jumble-${inputLetters.toLowerCase()}`;

  return (
    <div className="flex items-center gap-2 animate-fade-in-up">
      <button
        onClick={() => exportCSV(matches, filename)}
        className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-xs font-medium
                   bg-white/5 dark:bg-white/5 border border-white/10 dark:border-white/10
                   text-white/60 dark:text-white/60
                   hover:bg-white/10 hover:text-white/80 hover:border-white/15
                   transition-all duration-200 cursor-pointer"
        aria-label="Export results as CSV"
      >
        <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
        </svg>
        CSV
      </button>

      <button
        onClick={() => exportJSON(response, filename)}
        className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-xs font-medium
                   bg-white/5 dark:bg-white/5 border border-white/10 dark:border-white/10
                   text-white/60 dark:text-white/60
                   hover:bg-white/10 hover:text-white/80 hover:border-white/15
                   transition-all duration-200 cursor-pointer"
        aria-label="Export results as JSON"
      >
        <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
        </svg>
        JSON
      </button>
    </div>
  );
}
