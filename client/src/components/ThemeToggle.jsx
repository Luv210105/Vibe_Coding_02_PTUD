export default function ThemeToggle({ theme, onToggleTheme }) {
  return (
    <button
      type="button"
      onClick={onToggleTheme}
      aria-label={theme === "dark" ? "Chuyển sang light mode" : "Chuyển sang dark mode"}
      title={theme === "dark" ? "Light mode" : "Dark mode"}
      className="fixed bottom-5 right-5 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-black text-2xl text-white shadow-2xl transition hover:scale-105 hover:bg-slate-800 dark:border dark:border-slate-700 dark:bg-slate-900 dark:hover:bg-slate-800"
    >
      💡
    </button>
  );
}
