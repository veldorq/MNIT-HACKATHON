import ScoreBreakdown from "./ScoreBreakdown";

function getBadgeMeta(score) {
  if (score >= 80) {
    return {
      title: "High Credibility",
      badgeClass: "trust-badge",
      badgeLabel: "Trusted Source",
      description: "This content demonstrates strong alignment with verified sources and maintains editorial neutrality standards.",
    };
  }

  if (score >= 60) {
    return {
      title: "Moderate Credibility",
      badgeClass: "warning-badge",
      badgeLabel: "Caution Advised",
      description: "Some concerns detected regarding source attribution. Verify claims independently before sharing.",
    };
  }

  return {
    title: "Low Credibility",
    badgeClass: "danger-badge",
    badgeLabel: "Unverified",
    description: "Significant red flags detected. High probability of misinformation or satirical content.",
  };
}

function ResultCard({ result }) {
  // Extract main fake news analysis
  const fakeNewsData = result?.fakeNewsAnalysis || result;
  
  // Handle needs_verification case for fake news analysis
  if (fakeNewsData?.prediction === "needs_verification") {
    return (
      <section className="space-y-8">
        {/* MAIN: Fake News Analysis - Needs Verification */}
        <div className="glass rounded-2xl border border-slate-200/30 p-12 text-center text-slate-900">
          <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-amber-100 mx-auto">
            <span className="text-3xl">!</span>
          </div>
          <h2 className="mb-3 font-headline text-3xl italic">Needs Verification</h2>
          <p className="mb-4 text-lg text-slate-600">
            The model's confidence is below the reliability threshold. This content requires manual verification or additional evidence.
          </p>
          <div className="mt-6 rounded-lg bg-amber-50 p-4 text-left">
            <p className="text-sm text-slate-700">
              <span className="font-semibold">Why this happened:</span> The article may contain ambiguous language, mixed signals, or patterns not seen frequently in training data. Consider:
            </p>
            <ul className="mt-2 list-inside space-y-1 text-sm text-slate-600">
              <li>- Checking multiple fact-checking sources</li>
              <li>- Verifying claims with primary sources</li>
              <li>- Looking for corroborating evidence</li>
            </ul>
          </div>
          <div className="mt-6 text-sm text-slate-500">
            <p>Model confidence: {Math.round((fakeNewsData?.confidence ?? 0) * 100)}%</p>
            <p>Provider: {fakeNewsData?.provider || "unknown"}</p>
            {fakeNewsData?.mode && <p>Mode: {fakeNewsData.mode}</p>}
          </div>
        </div>

        {/* OPTIONAL: URL Analysis */}
        {result?.urlAnalysis && !result.urlAnalysis.error && (
          <div className="glass rounded-2xl border border-blue-200/50 p-8 bg-gradient-to-br from-blue-50/50 to-blue-100/30">
            <h3 className="mb-4 font-headline text-xl text-slate-900">🔗 URL Domain Verification</h3>
            <p className="text-sm text-slate-700 mb-3 font-medium">{result.urlAnalysis.domain}</p>
            <div className="flex flex-wrap gap-2 mb-4">
              <span className={`rounded-full px-3 py-1.5 text-xs font-semibold uppercase ${
                result.urlAnalysis.is_credible ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'
              }`}>
                {result.urlAnalysis.is_credible ? '✓ Credible' : '✗ Suspicious'}
              </span>
              <span className={`rounded-full px-3 py-1.5 text-xs font-semibold uppercase ${
                result.urlAnalysis.risk_level === 'safe' ? 'bg-green-200 text-green-800'
                : result.urlAnalysis.risk_level === 'dangerous' ? 'bg-red-200 text-red-800'
                : 'bg-yellow-200 text-yellow-800'
              }`}>
                {result.urlAnalysis.risk_level === 'safe' && '🛡️ Safe'}
                {result.urlAnalysis.risk_level === 'suspicious' && '⚠️ Suspicious'}
                {result.urlAnalysis.risk_level === 'dangerous' && '🚨 Dangerous'}
              </span>
            </div>
            <p className="text-sm text-slate-600 bg-white/60 rounded px-3 py-2">
              {result.urlAnalysis.explanation}
            </p>
          </div>
        )}
      </section>
    );
  }

  const score = fakeNewsData?.credibilityScore ?? 0;
  const confidence = Math.round((fakeNewsData?.confidence ?? 0) * 100);
  const badge = getBadgeMeta(score);

  const circumference = 2 * Math.PI * 45;
  const offset = circumference - (score / 100) * circumference;

  const modelScore = Math.min(100, Math.round(((fakeNewsData?.breakdown?.modelScore || 0) / 50) * 100));
  const keywordScore = Math.min(100, Math.round(((fakeNewsData?.breakdown?.keywordScore || 0) / 25) * 100));
  const lengthScore = Math.min(100, Math.round(((fakeNewsData?.breakdown?.lengthScore || 0) / 15) * 100));

  return (
    <section className="space-y-8">
      {/* MAIN FEATURE: Fake News Detection Analysis */}
      <div className="grid grid-cols-1 gap-6 md:grid-cols-12">
        <div className="glass relative overflow-hidden rounded-2xl p-8 text-slate-900 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.1)] md:col-span-5">
          <span className="mb-6 block text-[10px] font-semibold uppercase tracking-widest text-slate-500">Credibility Report</span>

          <div className="mb-6 flex items-center gap-6">
            <div className="relative h-28 w-28 flex-shrink-0">
              <svg className="h-full w-full -rotate-90 transform" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" fill="none" stroke="#e2e8f0" strokeWidth="8" />
                <circle
                  cx="50"
                  cy="50"
                  r="45"
                  fill="none"
                  stroke="#3b82f6"
                  strokeWidth="8"
                  strokeLinecap="round"
                  strokeDasharray={circumference}
                  strokeDashoffset={offset}
                  style={{ transition: "stroke-dashoffset 1.2s ease" }}
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="font-headline text-4xl font-light text-slate-900">{score}</span>
              </div>
            </div>

            <div className="flex-1">
              <div className={`mb-3 inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-bold uppercase tracking-tighter text-white ${badge.badgeClass}`}>
                {badge.badgeLabel}
              </div>
              <h3 className="mb-1 font-headline text-2xl italic text-slate-900">{badge.title}</h3>
              <p className="text-sm leading-relaxed text-slate-600">{badge.description}</p>
            </div>
          </div>

          <div className="space-y-3 border-t border-slate-200 pt-6">
            <div className="flex items-center justify-between text-sm">
              <span className="text-slate-500">Source Authority</span>
              <div className="flex items-center gap-2">
                <div className="h-1.5 w-24 overflow-hidden rounded-full bg-slate-200">
                  <div className="h-full rounded-full bg-blue-600" style={{ width: `${modelScore}%` }} />
                </div>
                <span className="w-10 text-right font-semibold text-slate-800">{modelScore}%</span>
              </div>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-slate-500">Linguistic Neutrality</span>
              <div className="flex items-center gap-2">
                <div className="h-1.5 w-24 overflow-hidden rounded-full bg-slate-200">
                  <div className="h-full rounded-full bg-amber-500" style={{ width: `${keywordScore}%` }} />
                </div>
                <span className="w-10 text-right font-semibold text-slate-800">{keywordScore}%</span>
              </div>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-slate-500">Factual Density</span>
              <div className="flex items-center gap-2">
                <div className="h-1.5 w-24 overflow-hidden rounded-full bg-slate-200">
                  <div className="h-full rounded-full bg-blue-500" style={{ width: `${lengthScore}%` }} />
                </div>
                <span className="w-10 text-right font-semibold text-slate-800">{lengthScore}%</span>
              </div>
            </div>
          </div>
        </div>

        <div className="relative min-h-[400px] overflow-hidden rounded-2xl md:col-span-7">
          <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900" />
          <div className="absolute inset-0 opacity-20" style={{ backgroundImage: "radial-gradient(circle at 2px 2px, rgba(255,255,255,0.2) 1px, transparent 0)", backgroundSize: "24px 24px" }} />

          <div className="relative z-10 flex h-full flex-col justify-between p-8 md:p-10">
            <div>
              <span className="mb-2 block text-[10px] font-semibold uppercase tracking-widest text-white/60">Neural Confidence</span>
              <div className="flex items-baseline gap-3">
                <h3 className="font-headline text-6xl font-light text-white">{confidence}%</h3>
                <span className="text-sm font-medium text-white/60">certainty</span>
              </div>
            </div>

            <div className="space-y-4">
              <div className="flex items-start gap-4">
                <div className="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-xl bg-white/10 text-2xl text-white">#</div>
                <div>
                  <h4 className="mb-1 font-medium text-white">Cross-Reference Analysis</h4>
                  <p className="text-sm text-white/70">Mode: {fakeNewsData.mode} | Provider: {fakeNewsData.provider}</p>
                </div>
              </div>
              <div className="flex items-start gap-4">
                <div className="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-xl bg-white/10 text-2xl text-white">*</div>
                <div>
                  <h4 className="mb-1 font-medium text-white">Pattern Recognition</h4>
                  <p className="text-sm text-white/70">Prediction: {fakeNewsData.prediction === "fake" ? "Likely Fake News" : "Likely Real News"}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="glass rounded-2xl border border-slate-200/30 p-8 text-slate-900">
        <div className="mb-6 flex items-center justify-between border-b border-slate-200 pb-4">
          <h2 className="font-headline text-3xl italic text-slate-900">Detailed Analysis</h2>
          <span className="text-sm text-slate-500">Complete Report</span>
        </div>

        {/* OPTIONAL: URL Analysis */}
        {result?.urlAnalysis && !result.urlAnalysis.error && (
          <div className="mb-8 rounded-xl border border-blue-200/50 bg-gradient-to-br from-blue-50/50 to-blue-100/30 p-6">
            <h4 className="mb-1 font-headline text-lg">🔗 URL Domain Verification</h4>
            <p className="text-sm text-slate-700 mb-3 font-medium">{result.urlAnalysis.domain}</p>
            <div className="flex flex-wrap gap-2 mb-3">
              <span className={`rounded-full px-3 py-1.5 text-xs font-semibold uppercase ${
                result.urlAnalysis.is_credible ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'
              }`}>
                {result.urlAnalysis.is_credible ? '✓ Credible' : '✗ Suspicious'}
              </span>
              <span className={`rounded-full px-3 py-1.5 text-xs font-semibold uppercase ${
                result.urlAnalysis.risk_level === 'safe' ? 'bg-green-200 text-green-800'
                : result.urlAnalysis.risk_level === 'dangerous' ? 'bg-red-200 text-red-800'
                : 'bg-yellow-200 text-yellow-800'
              }`}>
                {result.urlAnalysis.risk_level === 'safe' && '🛡️ Safe'}
                {result.urlAnalysis.risk_level === 'suspicious' && '⚠️ Suspicious'}
                {result.urlAnalysis.risk_level === 'dangerous' && '🚨 Dangerous'}
              </span>
            </div>
            <p className="text-sm text-slate-600 bg-white/60 rounded px-3 py-2">
              {result.urlAnalysis.explanation}
            </p>
          </div>
        )}

        {/* AI GENERATION DETECTION */}
        {result?.aiGenerationAnalysis && (
          <div className="mb-8 rounded-xl border border-purple-200/50 bg-gradient-to-br from-purple-50/50 to-pink-50/30 p-6">
            <div className="flex items-center justify-between mb-4">
              <h4 className="font-headline text-lg">🤖 AI Generation Indicators</h4>
              <span className={`rounded-full px-3 py-1 text-xs font-semibold uppercase ${
                result.aiGenerationAnalysis.aiScore >= 0.7 ? 'bg-red-200 text-red-800'
                : result.aiGenerationAnalysis.aiScore >= 0.5 ? 'bg-yellow-200 text-yellow-800'
                : 'bg-green-200 text-green-800'
              }`}>
                Score: {(result.aiGenerationAnalysis.aiScore * 100).toFixed(0)}%
              </span>
            </div>
            <p className="text-sm font-medium text-slate-800 mb-2">{result.aiGenerationAnalysis.verdict}</p>
            <p className="text-xs text-slate-600 bg-white/60 rounded px-3 py-2 mb-3">
              {result.aiGenerationAnalysis.disclaimer}
            </p>
            {result.aiGenerationAnalysis.indicators && (
              <div className="space-y-2">
                {Object.entries(result.aiGenerationAnalysis.indicators || {}).map(([key, data]) => {
                  if (data.error) return null;
                  return (
                    <div key={key} className="text-xs text-slate-600">
                      <span className="font-medium">{data.description}:</span> {data.matches} occurrences (score: {data.score || 0})
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}

        <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
          <div className="rounded-xl border border-slate-200 bg-white p-6">
            <h4 className="mb-2 font-headline text-lg">Sentiment Analysis</h4>
            <p className="mb-4 text-sm text-slate-600">Model confidence and keyword penalties produce an explainable neutrality signal.</p>
            <div className="h-1 w-full overflow-hidden rounded-full bg-slate-200">
              <div className="h-full rounded-full bg-blue-600" style={{ width: `${Math.max(8, keywordScore)}%` }} />
            </div>
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-6">
            <h4 className="mb-2 font-headline text-lg">Language Signals Detected</h4>
            <p className="mb-4 text-sm text-slate-600">Highlighting sensational, uncertain, and suspicious language patterns detected in the text.</p>
            <div className="flex flex-wrap gap-2">
              {(fakeNewsData.flaggedKeywords || []).slice(0, 3).map((keyword) => (
                <span key={keyword} className="rounded-full bg-red-50 px-3 py-1 text-xs font-medium text-red-700">
                  {keyword}
                </span>
              ))}
              {(fakeNewsData.flaggedKeywords || []).length === 0 ? <span className="text-xs text-slate-500">No suspicious keywords</span> : null}
            </div>
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-6">
            <h4 className="mb-2 font-headline text-lg">Temporal Analysis</h4>
            <p className="mb-4 text-sm text-slate-600">Breakdown scores track the contribution of model, keywords, and text length.</p>
            <ScoreBreakdown breakdown={fakeNewsData.breakdown} />
          </div>
        </div>

        {fakeNewsData.ensemble ? (
          <div className="mt-6 rounded-xl border border-slate-200 bg-slate-50 p-4 text-xs text-slate-700">
            <p className="mb-2 font-semibold text-slate-800">Hybrid Votes</p>
            <p>Kaggle: {fakeNewsData.ensemble.kaggle.prediction} ({Math.round(fakeNewsData.ensemble.kaggle.confidence * 100)}%)</p>
            <p>LIAR: {fakeNewsData.ensemble.liar.prediction} ({Math.round(fakeNewsData.ensemble.liar.confidence * 100)}%)</p>
            <p>Weights: fake {fakeNewsData.ensemble.weights.fake}, real {fakeNewsData.ensemble.weights.real}</p>
          </div>
        ) : null}
      </div>
    </section>
  );
}

export default ResultCard;
