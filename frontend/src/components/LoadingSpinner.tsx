export default function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center py-16 gap-4">
      <div className="relative w-16 h-16">
        {/* Outer ring */}
        <div className="absolute inset-0 rounded-full border-4 border-primary-500/20" />
        {/* Spinning arc */}
        <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-primary-400 border-r-primary-500 animate-spin-slow" />
        {/* Inner glow dot */}
        <div className="absolute inset-[22px] rounded-full bg-primary-500/40 blur-[4px] animate-pulse" />
      </div>
      <p className="text-sm font-medium text-surface-200 dark:text-surface-200 tracking-wide">
        Solving...
      </p>
    </div>
  );
}
