import { useState, useRef, useEffect, type FormEvent, type KeyboardEvent } from 'react';
import { fetchModes } from '../api/solver';
import type { ModeInfo, SolveMode } from '../types';

interface SearchPanelProps {
  onSearch: (letters: string, mode: SolveMode) => void;
  loading: boolean;
}

export default function SearchPanel({ onSearch, loading }: SearchPanelProps) {
  const [input, setInput] = useState('');
  const [modes, setModes] = useState<ModeInfo[]>([]);
  const [selectedMode, setSelectedMode] = useState<SolveMode>('strict');
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.focus();
    fetchModes()
      .then((data) => {
        setModes(data);
        if (data.length > 0 && !data.find(m => m.mode === 'strict')) {
          setSelectedMode(data[0].mode);
        }
      })
      .catch((err) => console.error('Failed to fetch modes:', err));
  }, []);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    const trimmed = input.trim();
    if (trimmed && !loading) {
      onSearch(trimmed, selectedMode);
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSubmit(e);
    }
  };

  const handleClear = () => {
    setInput('');
    inputRef.current?.focus();
  };

  const charCount = input.trim().length;

  return (
    <div className="glass-card p-6 sm:p-8 max-w-2xl mx-auto animate-fade-in-up">
      <form onSubmit={handleSubmit}>
        <div className="flex justify-between items-center mb-3">
          <label
            htmlFor="letters-input"
            className="block text-sm font-semibold text-white/70 dark:text-white/70 tracking-wide"
          >
            Enter your letters
          </label>
          
          {modes.length > 0 && (
            <div className="relative">
              <select
                value={selectedMode}
                onChange={(e) => setSelectedMode(e.target.value as SolveMode)}
                disabled={loading}
                className="appearance-none bg-white/5 dark:bg-white/5 border border-white/10 dark:border-white/10
                           text-white/80 dark:text-white/80 text-xs py-1.5 pl-3 pr-8 rounded-lg
                           focus:outline-none focus:border-primary-400/50 focus:ring-1 focus:ring-primary-500/30
                           transition-colors disabled:opacity-50 cursor-pointer"
              >
                {modes.map((mode) => (
                  <option key={mode.mode} value={mode.mode} className="bg-surface-900 text-white">
                    {mode.mode.charAt(0).toUpperCase() + mode.mode.slice(1)} Mode
                  </option>
                ))}
              </select>
              <svg className="absolute right-2 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-white/40 pointer-events-none" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
              </svg>
            </div>
          )}
        </div>

        <div className="relative">
          <input
            ref={inputRef}
            id="letters-input"
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value.replace(/[^a-zA-Z]/g, ''))}
            onKeyDown={handleKeyDown}
            placeholder="e.g., dog"
            disabled={loading}
            autoComplete="off"
            spellCheck={false}
            className="w-full px-5 py-4 text-lg sm:text-xl font-medium tracking-[0.15em] uppercase
                       rounded-xl border border-white/10 dark:border-white/10
                       bg-white/5 dark:bg-white/5
                       text-white dark:text-white placeholder-white/20 dark:placeholder-white/20
                       focus:outline-none focus:border-primary-400/50 focus:ring-2 focus:ring-primary-500/20
                       disabled:opacity-50
                       transition-all duration-300"
          />

          {/* Clear button */}
          {input.length > 0 && !loading && (
            <button
              type="button"
              onClick={handleClear}
              className="absolute right-4 top-1/2 -translate-y-1/2 w-7 h-7 rounded-lg
                         bg-white/10 hover:bg-white/20 flex items-center justify-center
                         transition-all duration-200 cursor-pointer"
              aria-label="Clear input"
            >
              <svg className="w-4 h-4 text-white/50" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>

        {/* Character count & mode description */}
        <div className="flex items-center justify-between mt-3">
          <span className="text-xs text-white/30 dark:text-white/30">
            {charCount > 0 ? `${charCount} letter${charCount !== 1 ? 's' : ''}` : 'Letters only (a–z)'}
          </span>
          {modes.length > 0 && (
            <span className="text-xs text-white/40 italic">
              {modes.find(m => m.mode === selectedMode)?.description}
            </span>
          )}
        </div>

        {/* Submit button */}
        <button
          type="submit"
          disabled={loading || charCount === 0}
          className={`w-full mt-5 py-3.5 px-6 rounded-xl text-sm font-semibold text-white
                     gradient-btn flex items-center justify-center gap-2.5 cursor-pointer
                     ${!loading && charCount > 0 ? 'animate-pulse-glow' : ''}`}
        >
          {loading ? (
            <>
              <svg className="w-4 h-4 animate-spin-slow" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182" />
              </svg>
              <span>Solving...</span>
            </>
          ) : (
            <>
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
              </svg>
              <span>Find Matches</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
}
