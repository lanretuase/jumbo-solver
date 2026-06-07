import { useState, useMemo } from 'react';
import type { MatchResult, SortOption, FilterOption } from '../types';

interface ResultsTableProps {
  matches: MatchResult[];
  fullAnagramCount: number;
  subAnagramCount: number;
}

const FILTERS: { key: FilterOption; label: string }[] = [
  { key: 'all', label: 'All' },
  { key: 'full_anagram', label: 'Full Anagrams' },
  { key: 'sub_anagram', label: 'Sub-Anagrams' },
];

const SORTS: { key: SortOption; label: string }[] = [
  { key: 'confidence_desc', label: 'Confidence ↓' },
  { key: 'length_desc', label: 'Length ↓' },
  { key: 'length_asc', label: 'Length ↑' },
  { key: 'alphabetical', label: 'A–Z' },
];

function getCount(filter: FilterOption, total: number, full: number, sub: number): number {
  if (filter === 'all') return total;
  if (filter === 'full_anagram') return full;
  return sub;
}

export default function ResultsTable({ matches, fullAnagramCount, subAnagramCount }: ResultsTableProps) {
  const [filter, setFilter] = useState<FilterOption>('all');
  const [sort, setSort] = useState<SortOption>('confidence_desc');

  const processedMatches = useMemo(() => {
    let filtered = matches;
    if (filter !== 'all') {
      filtered = matches.filter((m) => m.type === filter);
    }

    const sorted = [...filtered];
    switch (sort) {
      case 'confidence_desc':
        sorted.sort((a, b) => b.confidence - a.confidence || b.length - a.length || a.word.localeCompare(b.word));
        break;
      case 'length_desc':
        sorted.sort((a, b) => b.length - a.length || a.word.localeCompare(b.word));
        break;
      case 'length_asc':
        sorted.sort((a, b) => a.length - b.length || a.word.localeCompare(b.word));
        break;
      case 'alphabetical':
        sorted.sort((a, b) => a.word.localeCompare(b.word));
        break;
    }
    return sorted;
  }, [matches, filter, sort]);

  const totalCount = matches.length;

  return (
    <div className="glass-card p-5 sm:p-6 animate-fade-in-up">
      {/* ── Controls Row ──────────────────────────────────────────── */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-5">
        {/* Filter tabs */}
        <div className="flex rounded-xl bg-white/5 dark:bg-white/5 p-1 gap-0.5">
          {FILTERS.map(({ key, label }) => {
            const count = getCount(key, totalCount, fullAnagramCount, subAnagramCount);
            const isActive = filter === key;
            return (
              <button
                key={key}
                onClick={() => setFilter(key)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 cursor-pointer
                  ${isActive
                    ? 'bg-primary-500/20 text-primary-300 shadow-sm'
                    : 'text-white/40 hover:text-white/60 hover:bg-white/5'
                  }`}
              >
                {label}
                <span className={`ml-1.5 text-[10px] ${isActive ? 'text-primary-400/70' : 'text-white/25'}`}>
                  {count}
                </span>
              </button>
            );
          })}
        </div>

        {/* Sort dropdown */}
        <div className="relative">
          <select
            value={sort}
            onChange={(e) => setSort(e.target.value as SortOption)}
            className="appearance-none px-3 py-1.5 pr-8 rounded-lg text-xs font-medium
                       bg-white/5 dark:bg-white/5 border border-white/10 dark:border-white/10
                       text-white/60 dark:text-white/60
                       focus:outline-none focus:border-primary-400/40
                       transition-all duration-200 cursor-pointer"
          >
            {SORTS.map(({ key, label }) => (
              <option key={key} value={key} className="bg-surface-900 text-white">
                {label}
              </option>
            ))}
          </select>
          <svg
            className="absolute right-2 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-white/30 pointer-events-none"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={2}
            stroke="currentColor"
          >
            <path strokeLinecap="round" strokeLinejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
          </svg>
        </div>
      </div>

      {/* ── Empty filter state ────────────────────────────────────── */}
      {processedMatches.length === 0 && (
        <div className="text-center py-10">
          <p className="text-sm text-white/30">No matches for this filter</p>
        </div>
      )}

      {/* ── Desktop Table ─────────────────────────────────────────── */}
      {processedMatches.length > 0 && (
        <>
          <div className="hidden sm:block overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-white/8">
                  <th className="text-left py-2.5 px-3 text-xs font-semibold text-white/30 uppercase tracking-wider w-14">#</th>
                  <th className="text-left py-2.5 px-3 text-xs font-semibold text-white/30 uppercase tracking-wider">Word</th>
                  <th className="text-left py-2.5 px-3 text-xs font-semibold text-white/30 uppercase tracking-wider w-20">Length</th>
                  <th className="text-left py-2.5 px-3 text-xs font-semibold text-white/30 uppercase tracking-wider w-36">Type</th>
                  <th className="text-left py-2.5 px-3 text-xs font-semibold text-white/30 uppercase tracking-wider w-32">Confidence</th>
                  <th className="text-left py-2.5 px-3 text-xs font-semibold text-white/30 uppercase tracking-wider w-32">Category</th>
                </tr>
              </thead>
              <tbody>
                {processedMatches.map((match, idx) => (
                  <tr
                    key={`${match.word}-${match.type}`}
                    className={`animate-fade-in-left border-b border-white/4 hover:bg-white/3 transition-colors
                      ${idx % 2 === 0 ? 'bg-white/[0.01]' : ''}`}
                    style={{ animationDelay: `${Math.min(idx * 30, 600)}ms` }}
                  >
                    <td className="py-2.5 px-3 text-xs text-white/20 tabular-nums">{idx + 1}</td>
                    <td className="py-2.5 px-3 font-semibold text-white/90 tracking-wide">{match.word}</td>
                    <td className="py-2.5 px-3 text-white/50 tabular-nums">{match.length}</td>
                    <td className="py-2.5 px-3">
                      <span className={`badge ${match.type === 'full_anagram' ? 'badge-indigo' : 'badge-emerald'}`}>
                        {match.type === 'full_anagram' ? 'Full Anagram' : 'Sub-Anagram'}
                      </span>
                    </td>
                    <td className="py-2.5 px-3">
                      <div className="flex items-center gap-2">
                        <div className="flex-1 h-1.5 bg-white/10 rounded-full overflow-hidden">
                          <div 
                            className={`h-full rounded-full ${match.confidence > 0.6 ? 'bg-emerald-400' : match.confidence > 0.3 ? 'bg-amber-400' : 'bg-rose-400'}`}
                            style={{ width: `${Math.max(5, match.confidence * 100)}%` }}
                          />
                        </div>
                        <span className="text-[10px] text-white/50 w-7">{Math.round(match.confidence * 100)}%</span>
                      </div>
                    </td>
                    <td className="py-2.5 px-3">
                      <span className="text-[10px] uppercase tracking-widest text-white/40 px-2 py-0.5 rounded border border-white/10 bg-white/5">
                        {match.category.replace('_', ' ')}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* ── Mobile Card Layout ──────────────────────────────────── */}
          <div className="sm:hidden space-y-2">
            {processedMatches.map((match, idx) => (
              <div
                key={`${match.word}-${match.type}-m`}
                className="animate-fade-in-left p-3 rounded-lg bg-white/[0.02] border border-white/5
                           flex items-center justify-between"
                style={{ animationDelay: `${Math.min(idx * 30, 600)}ms` }}
              >
                <div className="flex items-center gap-3">
                  <span className="text-xs text-white/20 w-6 tabular-nums">{idx + 1}</span>
                  <div>
                    <p className="font-semibold text-white/90 tracking-wide text-sm">{match.word}</p>
                    <p className="text-xs text-white/35 mt-0.5">{match.length} letters</p>
                  </div>
                </div>
                <span className={`badge ${match.type === 'full_anagram' ? 'badge-indigo' : 'badge-emerald'}`}>
                  {match.type === 'full_anagram' ? 'Full' : 'Sub'}
                </span>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
