function ScoreBreakdown({ breakdown }) {
  const rows = [
    ["Model", breakdown?.modelScore ?? 0],
    ["Keywords", breakdown?.keywordScore ?? 0],
    ["Length", breakdown?.lengthScore ?? 0],
    ["Hedge", breakdown?.hedgeScore ?? 0],
  ];

  return (
    <div className="rounded-xl bg-slate-50 p-4">
      <h4 className="mb-3 text-sm font-semibold text-slate-700">Score Breakdown</h4>
      <div className="space-y-2">
        {rows.map(([label, value]) => (
          <div className="flex items-center justify-between text-sm" key={label}>
            <span className="text-slate-600">{label}</span>
            <span className="font-medium text-slate-900">{value}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ScoreBreakdown;
