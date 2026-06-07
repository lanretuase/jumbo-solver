import type { ReactNode } from 'react';

interface LayoutProps {
  isDark: boolean;
  onToggleTheme: () => void;
  children: ReactNode;
}

export default function Layout({ isDark, onToggleTheme, children }: LayoutProps) {
  return (
    <div className="min-h-screen flex flex-col">
      {/* ── Header ────────────────────────────────────────────────── */}
      <header className="relative z-10 border-b border-white/5 dark:border-white/5">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-5 flex items-center justify-between">
          <div className="flex items-center gap-3">
            {/* Logo */}
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center shadow-lg shadow-primary-500/20">
              <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5M12 17.25h8.25" />
              </svg>
            </div>
            <div>
              <h1 className="text-lg sm:text-xl font-bold gradient-text tracking-tight">
                Jumble Solver
              </h1>
              <p className="text-[11px] text-white/30 dark:text-white/30 font-medium tracking-wide hidden sm:block">
                Unscramble any set of letters instantly
              </p>
            </div>
          </div>

          {/* Theme toggle */}
          <button
            onClick={onToggleTheme}
            className="relative w-10 h-10 rounded-xl border border-white/10 dark:border-white/10 
                       bg-white/5 dark:bg-white/5 hover:bg-white/10 dark:hover:bg-white/10
                       transition-all duration-300 flex items-center justify-center group cursor-pointer"
            aria-label={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
          >
            {isDark ? (
              /* Sun icon */
              <svg
                className="w-5 h-5 text-amber-300 group-hover:text-amber-200 transition-colors"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={1.8}
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M12 3v2.25m6.364.386-1.591 1.591M21 12h-2.25m-.386 6.364-1.591-1.591M12 18.75V21m-4.773-4.227-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0Z"
                />
              </svg>
            ) : (
              /* Moon icon */
              <svg
                className="w-5 h-5 text-primary-400 group-hover:text-primary-300 transition-colors"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={1.8}
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M21.752 15.002A9.72 9.72 0 0 1 18 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 0 0 3 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 0 0 9.002-5.998Z"
                />
              </svg>
            )}
          </button>
        </div>
      </header>

      {/* ── Main Content ──────────────────────────────────────────── */}
      <main className="flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>

      {/* ── Footer ────────────────────────────────────────────────── */}
      <footer className="border-t border-white/5 dark:border-white/5">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-5 flex flex-col sm:flex-row items-center justify-between gap-2">
          <p className="text-xs text-white/25 dark:text-white/25">
            Built with{' '}
            <span className="text-primary-400/60">FastAPI</span>
            {' & '}
            <span className="text-primary-400/60">React</span>
          </p>
          <p className="text-xs text-white/20 dark:text-white/20">
            © {new Date().getFullYear()} Jumble Solver
          </p>
        </div>
      </footer>
    </div>
  );
}
