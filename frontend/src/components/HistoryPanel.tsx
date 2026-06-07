import type { HistoryEntry } from '../types';

interface HistoryPanelProps {
  history: HistoryEntry[];
  onSelect: (letters: string) => void;
  onClear: () => void;
}

function timeAgo(timestamp: number): string {
  const seconds = Math.floor((Date.now() - timestamp) / 1000);
  if (seconds < 60) return 'just now';
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

export default function HistoryPanel({ history, onSelect, onClear }: HistoryPanelProps) {
  if (history.length === 0) {
    return (
      <div className="glass-card p-5 sm:p-6 animate-fade-in-up">
        <h3 className="text-sm font-semibold text-white/70 dark:text-white/70 mb-4 flex items-center gap-2">
          <svg className="w-4 h-4 text-primary-400" fill="none" viewBox="0 0 24 24" strokeWidth={1.8} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
          </svg>
          Search History
        </h3>
        <p className="text-xs text-white/25 text-center py-4">No searches yet</p>
      </div>
    );
  }

  return (
    <div className="glass-card p-5 sm:p-6 animate-fade-in-up">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-semibold text-white/70 dark:text-white/70 flex items-center gap-2">
          <svg className="w-4 h-4 text-primary-400" fill="none" viewBox="0 0 24 24" strokeWidth={1.8} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
          </svg>
          Search History
        </h3>
        <button
          onClick={onClear}
          className="text-[10px] font-medium text-white/25 hover:text-red-400/70 transition-colors duration-200 cursor-pointer"
        >
          Clear All
        </button>
      </div>

      <div className="space-y-1.5 max-h-64 overflow-y-auto pr-1">
        {history.map((entry, idx) => (
          <button
            key={`${entry.letters}-${entry.timestamp}`}
            onClick={() => onSelect(entry.letters)}
            className="w-full text-left px-3 py-2.5 rounded-lg
                       bg-white/[0.02] hover:bg-white/[0.06] border border-transparent hover:border-white/8
                       transition-all duration-200 group animate-fade-in-left cursor-pointer"
            style={{ animationDelay: `${idx * 40}ms` }}
          >
            <div className="flex items-center justify-between">
              <span className="text-sm font-semibold text-white/75 tracking-widest uppercase group-hover:text-primary-300 transition-colors">
                {entry.letters}
              </span>
              <span className="text-[10px] text-white/20">{timeAgo(entry.timestamp)}</span>
            </div>
            <p className="text-[10px] text-white/30 mt-0.5">
              {entry.total_matches} match{entry.total_matches !== 1 ? 'es' : ''}
            </p>
          </button>
        ))}
      </div>
    </div>
  );
}
