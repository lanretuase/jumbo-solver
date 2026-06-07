import { useMemo } from 'react';
import type { MatchResult } from '../types';

interface TopMatchesProps {
  matches: MatchResult[];
}

export default function TopMatches({ matches }: TopMatchesProps) {
  const top20 = useMemo(() => {
    const sorted = [...matches].sort((a, b) => b.length - a.length || a.word.localeCompare(b.word));
    return sorted.slice(0, 20);
  }, [matches]);

  if (top20.length === 0) return null;

  return (
    <div className="glass-card p-5 sm:p-6 animate-fade-in-up">
      <h3 className="text-sm font-semibold text-white/70 dark:text-white/70 mb-4 flex items-center gap-2">
        <svg className="w-4 h-4 text-accent-400" fill="none" viewBox="0 0 24 24" strokeWidth={1.8} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 18.75h-9m9 0a3 3 0 0 1 3 3h-15a3 3 0 0 1 3-3m9 0v-4.5A3.375 3.375 0 0 0 13.125 10.875h-2.25A3.375 3.375 0 0 0 7.5 14.25v4.5m6-6V6.75m0 0h3.75L12 2.25 5.25 6.75H9m3 0V2.25" />
        </svg>
        Top {Math.min(20, top20.length)} Longest Matches
      </h3>

      <div className="flex flex-wrap gap-2">
        {top20.map((match, idx) => (
          <div
            key={`${match.word}-top`}
            className="animate-fade-in-up group relative"
            style={{ animationDelay: `${idx * 40}ms` }}
          >
            <span
              className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold
                          transition-all duration-300 cursor-default
                          ${match.type === 'full_anagram'
                  ? 'bg-primary-500/10 text-primary-300 border border-primary-500/20 hover:bg-primary-500/20 hover:border-primary-400/30'
                  : 'bg-accent-500/10 text-accent-400 border border-accent-500/20 hover:bg-accent-500/20 hover:border-accent-400/30'
                }`}
            >
              <span className="tracking-wide">{match.word}</span>
              <span className="text-[9px] opacity-50 font-normal tabular-nums">
                {match.length}
              </span>
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
