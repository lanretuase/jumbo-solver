import { useEffect, useState, useRef } from 'react';
import { formatMs, formatNumber } from '../utils/formatters';

interface StatsPanelProps {
  totalMatches: number;
  fullAnagramCount: number;
  subAnagramCount: number;
  longestWord: string | null;
  executionMs: number;
}

interface StatCardProps {
  icon: React.ReactNode;
  label: string;
  value: string;
  rawNumber?: number;
  delay: number;
}

function useCountUp(target: number, duration: number = 800): number {
  const [current, setCurrent] = useState(0);
  const startTimeRef = useRef<number | null>(null);
  const frameRef = useRef<number>(0);

  useEffect(() => {
    if (target === 0) {
      setCurrent(0);
      return;
    }

    startTimeRef.current = null;

    const animate = (timestamp: number) => {
      if (!startTimeRef.current) startTimeRef.current = timestamp;
      const elapsed = timestamp - startTimeRef.current;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setCurrent(Math.round(eased * target));

      if (progress < 1) {
        frameRef.current = requestAnimationFrame(animate);
      }
    };

    frameRef.current = requestAnimationFrame(animate);

    return () => {
      if (frameRef.current) cancelAnimationFrame(frameRef.current);
    };
  }, [target, duration]);

  return current;
}

function StatCard({ icon, label, value, rawNumber, delay }: StatCardProps) {
  const animatedValue = useCountUp(rawNumber ?? 0, 800);
  const displayValue = rawNumber !== undefined ? formatNumber(animatedValue) : value;

  return (
    <div
      className="glass-card glass-card-hover p-4 sm:p-5 animate-fade-in-up flex flex-col items-center text-center gap-2"
      style={{ animationDelay: `${delay}ms` }}
    >
      <div className="w-9 h-9 rounded-xl bg-primary-500/10 flex items-center justify-center mb-1">
        {icon}
      </div>
      <p className="text-xs font-medium text-white/35 dark:text-white/35 uppercase tracking-wider">
        {label}
      </p>
      <p className="text-xl sm:text-2xl font-bold text-white/90 dark:text-white/90 tabular-nums tracking-tight">
        {displayValue}
      </p>
    </div>
  );
}

export default function StatsPanel({
  totalMatches,
  fullAnagramCount,
  subAnagramCount,
  longestWord,
  executionMs,
}: StatsPanelProps) {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3 sm:gap-4">
      <StatCard
        delay={0}
        label="Total Matches"
        value={formatNumber(totalMatches)}
        rawNumber={totalMatches}
        icon={
          <svg className="w-4.5 h-4.5 text-primary-400" fill="none" viewBox="0 0 24 24" strokeWidth={1.8} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6A2.25 2.25 0 0 1 6 3.75h2.25A2.25 2.25 0 0 1 10.5 6v2.25a2.25 2.25 0 0 1-2.25 2.25H6a2.25 2.25 0 0 1-2.25-2.25V6ZM3.75 15.75A2.25 2.25 0 0 1 6 13.5h2.25a2.25 2.25 0 0 1 2.25 2.25V18a2.25 2.25 0 0 1-2.25 2.25H6A2.25 2.25 0 0 1 3.75 18v-2.25ZM13.5 6a2.25 2.25 0 0 1 2.25-2.25H18A2.25 2.25 0 0 1 20.25 6v2.25A2.25 2.25 0 0 1 18 10.5h-2.25a2.25 2.25 0 0 1-2.25-2.25V6ZM13.5 15.75a2.25 2.25 0 0 1 2.25-2.25H18a2.25 2.25 0 0 1 2.25 2.25V18A2.25 2.25 0 0 1 18 20.25h-2.25a2.25 2.25 0 0 1-2.25-2.25v-2.25Z" />
          </svg>
        }
      />
      <StatCard
        delay={80}
        label="Full Anagrams"
        value={formatNumber(fullAnagramCount)}
        rawNumber={fullAnagramCount}
        icon={
          <svg className="w-4.5 h-4.5 text-primary-400" fill="none" viewBox="0 0 24 24" strokeWidth={1.8} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 9h16.5m-16.5 6.75h16.5" />
          </svg>
        }
      />
      <StatCard
        delay={160}
        label="Sub-Anagrams"
        value={formatNumber(subAnagramCount)}
        rawNumber={subAnagramCount}
        icon={
          <svg className="w-4.5 h-4.5 text-accent-400" fill="none" viewBox="0 0 24 24" strokeWidth={1.8} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M21 7.5V18M15 7.5V18M3 16.811V8.69c0-.864.933-1.406 1.683-.977l7.108 4.061a1.125 1.125 0 0 1 0 1.954l-7.108 4.061A1.125 1.125 0 0 1 3 16.811Z" />
          </svg>
        }
      />
      <StatCard
        delay={240}
        label="Longest Word"
        value={longestWord ?? '—'}
        icon={
          <svg className="w-4.5 h-4.5 text-primary-400" fill="none" viewBox="0 0 24 24" strokeWidth={1.8} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.087.16 2.185.283 3.293.369V21l4.076-4.076a1.526 1.526 0 0 1 1.037-.443 48.282 48.282 0 0 0 5.68-.494c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018Z" />
          </svg>
        }
      />
      <StatCard
        delay={320}
        label="Speed"
        value={formatMs(executionMs)}
        icon={
          <svg className="w-4.5 h-4.5 text-accent-400" fill="none" viewBox="0 0 24 24" strokeWidth={1.8} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
          </svg>
        }
      />
    </div>
  );
}
