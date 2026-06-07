import { useCallback, useEffect, useRef } from 'react';
import { useTheme } from './hooks/useTheme';
import { useSolver } from './hooks/useSolver';
import { useHistory } from './hooks/useHistory';

import Layout from './components/Layout';
import SearchPanel from './components/SearchPanel';
import StatsPanel from './components/StatsPanel';
import ResultsTable from './components/ResultsTable';
import ChartPanel from './components/ChartPanel';
import TopMatches from './components/TopMatches';
import HistoryPanel from './components/HistoryPanel';
import ExportButtons from './components/ExportButtons';
import EmptyState from './components/EmptyState';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';

export default function App() {
  const { isDark, toggleTheme } = useTheme();
  const { results, loading, error, solve } = useSolver();
  const { history, addEntry, clearHistory } = useHistory();
  const lastRecordedInput = useRef<string | null>(null);

  // Record search results to history whenever new results arrive
  useEffect(() => {
    if (results && !loading && results.input !== lastRecordedInput.current) {
      lastRecordedInput.current = results.input;
      addEntry(results.input, results.total_matches, results.mode);
    }
  }, [results, loading, addEntry]);

  const handleSearch = useCallback(
    (letters: string, mode?: import('./types').SolveMode) => {
      solve(letters, mode);
    },
    [solve]
  );

  const handleHistorySelect = useCallback(
    (letters: string, mode?: import('./types').SolveMode) => {
      solve(letters, mode);
    },
    [solve]
  );

  return (
    <Layout isDark={isDark} onToggleTheme={toggleTheme}>
      <div className="space-y-6">
        {/* ── Search Panel ──────────────────────────────────────────── */}
        <SearchPanel onSearch={handleSearch} loading={loading} />

        {/* ── Loading State ────────────────────────────────────────── */}
        {loading && (
          <div className="flex justify-center py-12">
            <LoadingSpinner />
          </div>
        )}

        {/* ── Error State ──────────────────────────────────────────── */}
        {error && !loading && (
          <ErrorMessage
            message={error}
            onRetry={() => {
              if (results?.input) {
                solve(results.input);
              }
            }}
          />
        )}

        {/* ── Empty State ──────────────────────────────────────────── */}
        {!results && !loading && !error && <EmptyState />}

        {/* ── Results ──────────────────────────────────────────────── */}
        {results && !loading && (
          <div className="space-y-6">
            {/* Stats */}
            <StatsPanel
              totalMatches={results.total_matches}
              fullAnagramCount={results.full_anagram_count}
              subAnagramCount={results.sub_anagram_count}
              longestWord={results.longest_word}
              executionMs={results.execution_ms}
            />

            {/* Export + Results Table */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
              <h2 className="text-sm font-semibold text-white/50 dark:text-white/50 tracking-wide">
                Results for{' '}
                <span className="text-primary-300 font-bold tracking-[0.15em] uppercase">
                  {results.input}
                </span>
              </h2>
              <ExportButtons
                matches={results.matches}
                response={results}
                inputLetters={results.input}
              />
            </div>

            <ResultsTable
              matches={results.matches}
              fullAnagramCount={results.full_anagram_count}
              subAnagramCount={results.sub_anagram_count}
            />

            {/* Charts + Top Matches */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <ChartPanel matches={results.matches} />
              <TopMatches matches={results.matches} />
            </div>
          </div>
        )}

        {/* ── History Panel ─────────────────────────────────────────── */}
        <HistoryPanel
          history={history}
          onSelect={handleHistorySelect}
          onClear={clearHistory}
        />
      </div>
    </Layout>
  );
}
