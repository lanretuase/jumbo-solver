import { useMemo } from 'react';
import type { MatchResult } from '../types';

interface ChartPanelProps {
  matches: MatchResult[];
}

export default function ChartPanel({ matches }: ChartPanelProps) {
  const distribution = useMemo(() => {
    const counts: Record<number, number> = {};
    for (const m of matches) {
      counts[m.length] = (counts[m.length] || 0) + 1;
    }
    const entries = Object.entries(counts)
      .map(([len, count]) => ({ length: Number(len), count }))
      .sort((a, b) => a.length - b.length);
    return entries;
  }, [matches]);

  if (distribution.length === 0) return null;

  const maxCount = Math.max(...distribution.map((d) => d.count));

  return (
    <div className="glass-card p-5 sm:p-6 animate-fade-in-up">
      <h3 className="text-sm font-semibold text-white/70 dark:text-white/70 mb-5 flex items-center gap-2">
        <svg className="w-4 h-4 text-primary-400" fill="none" viewBox="0 0 24 24" strokeWidth={1.8} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z" />
        </svg>
        Word Length Distribution
      </h3>

      {/* Bar chart */}
      <div className="flex items-end gap-1.5 sm:gap-2 h-40 sm:h-48 px-1">
        {distribution.map((entry, idx) => {
          const heightPercent = maxCount > 0 ? (entry.count / maxCount) * 100 : 0;
          return (
            <div
              key={entry.length}
              className="flex-1 flex flex-col items-center gap-1.5 group"
            >
              {/* Count label */}
              <span className="text-[10px] font-semibold text-white/40 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                {entry.count}
              </span>

              {/* Bar */}
              <div className="w-full flex items-end" style={{ height: '100%' }}>
                <div
                  className="w-full rounded-t-md animate-grow-bar cursor-pointer
                             bg-gradient-to-t from-primary-600 to-primary-400
                             hover:from-primary-500 hover:to-primary-300
                             transition-all duration-300
                             shadow-sm shadow-primary-500/10
                             relative"
                  style={{
                    height: `${Math.max(heightPercent, 4)}%`,
                    animationDelay: `${idx * 80}ms`,
                  }}
                >
                  {/* Tooltip */}
                  <div className="absolute -top-8 left-1/2 -translate-x-1/2 
                                  bg-surface-800 text-white text-[10px] px-2 py-0.5 rounded-md
                                  opacity-0 group-hover:opacity-100 transition-opacity duration-200
                                  pointer-events-none whitespace-nowrap border border-white/10
                                  shadow-lg z-10">
                    {entry.count} word{entry.count !== 1 ? 's' : ''}
                  </div>
                </div>
              </div>

              {/* Length label */}
              <span className="text-[10px] font-medium text-white/35 tabular-nums">
                {entry.length}
              </span>
            </div>
          );
        })}
      </div>

      {/* X-axis label */}
      <p className="text-center text-[10px] text-white/20 mt-3 tracking-wide uppercase">
        Word Length
      </p>
    </div>
  );
}
