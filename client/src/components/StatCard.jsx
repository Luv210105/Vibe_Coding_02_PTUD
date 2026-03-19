export default function StatCard({ label, value, hint }) {
  return (
    <div className="rounded-3xl bg-white/90 p-5 shadow-panel">
      <p className="text-sm uppercase tracking-[0.18em] text-slate-400">{label}</p>
      <p className="mt-3 text-3xl font-bold text-slate-800">{value}</p>
      <p className="mt-2 text-sm text-slate-500">{hint}</p>
    </div>
  );
}