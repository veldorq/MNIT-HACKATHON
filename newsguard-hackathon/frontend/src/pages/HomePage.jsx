import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import InputBox from "../components/InputBox";
import ResultCard from "../components/ResultCard";
import { analyzeNews, fetchModels } from "../utils/api";

function AnalyzerPage() {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [mode, setMode] = useState("hybrid");
  const [modelOptions, setModelOptions] = useState([
    { mode: "hybrid", label: "Hybrid Ensemble", accuracy: null },
  ]);
  const [isDark, setIsDark] = useState(false);
  const [particles, setParticles] = useState([]);

  useEffect(() => {
    const generated = Array.from({ length: 20 }).map((_, index) => ({
      id: index,
      size: Math.random() * 100 + 50,
      left: Math.random() * 100,
      top: Math.random() * 100,
      opacity: Math.random() * 0.3 + 0.1,
      duration: Math.random() * 10 + 10,
    }));
    setParticles(generated);
  }, []);

  useEffect(() => {
    const loadModels = async () => {
      const options = await fetchModels();
      if (options.length > 0) {
        setModelOptions(options);
        if (!options.find((item) => item.mode === mode)) {
          setMode(options[0].mode);
        }
      }
    };

    loadModels();
  }, []);

  const handleAnalyze = async (text, selectedMode, url, checkUrl) => {
    setIsLoading(true);
    setError("");

    try {
      const response = await analyzeNews(text, selectedMode, url, checkUrl);
      setResult(response);
    } catch (apiError) {
      setError(apiError.message);
      setResult(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={`min-h-screen ${isDark ? "bg-slate-900 text-slate-100" : "bg-[#f7f9fb] text-[#191c1e]"} relative selection:bg-[#dce1ff] selection:text-[#00164e]`}>
      <div className="noise" />
      <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none">
        {particles.map((particle) => (
          <div
            key={particle.id}
            className="particle"
            style={{
              width: `${particle.size}px`,
              height: `${particle.size}px`,
              left: `${particle.left}%`,
              top: `${particle.top}%`,
              opacity: particle.opacity,
              animation: `float ${particle.duration}s ease-in-out infinite`,
            }}
          />
        ))}
      </div>

      <nav className="glass fixed top-0 z-50 w-full shadow-sm shadow-slate-900/5">
        <div className="mx-auto flex w-full max-w-[1600px] items-center justify-between px-8 py-4">
          <Link to="/" className="flex items-center gap-3 hover:opacity-80 transition-opacity">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-900 font-headline text-xl italic text-white">N</div>
            <div className="font-headline text-2xl italic text-slate-900">NewsGuard</div>
          </Link>
          <div className="hidden items-center gap-8 md:flex">
            <Link className="text-xs uppercase tracking-[0.2em] text-slate-500 transition-colors hover:text-slate-900" to="/">
              Home
            </Link>
            <Link className="border-b-2 border-slate-900 pb-1 text-xs font-semibold uppercase tracking-[0.2em] text-slate-900" to="/analyzer">
              Analyzer
            </Link>
            <Link className="text-xs uppercase tracking-[0.2em] text-slate-500 transition-colors hover:text-slate-900" to="/about-us">
              About Us
            </Link>
            <Link className="text-xs uppercase tracking-[0.2em] text-slate-500 transition-colors hover:text-slate-900" to="/methodology">
              Methodology
            </Link>
            <Link className="text-xs uppercase tracking-[0.2em] text-slate-500 transition-colors hover:text-slate-900" to="/about">
              About
            </Link>
          </div>
          <div className="flex items-center gap-4">
            <button className="hidden rounded-full bg-slate-200 px-4 py-2 text-sm text-slate-700 md:block" onClick={() => setIsDark((prev) => !prev)} type="button">
              {isDark ? "Light" : "Dark"}
            </button>
            <button className="rounded-full bg-slate-900 px-6 py-2.5 text-sm font-medium text-white transition-all hover:bg-slate-800" type="button">
              Get Started
            </button>
          </div>
        </div>
      </nav>

      <main className="relative z-10 pb-24 pt-32">
        <section className="mx-auto mb-24 max-w-4xl px-6" id="analyzer">
          <div className="mb-8">
            <h2 className="text-center font-headline text-3xl font-light text-slate-900 mb-2">News Analyzer</h2>
            <p className="text-center text-slate-600 text-sm">Paste any news article or headline below to get instant credibility insights.</p>
          </div>
          <InputBox onAnalyze={handleAnalyze} isLoading={isLoading} mode={mode} onModeChange={setMode} modelOptions={modelOptions} />
          {error ? <p className="mt-4 text-sm font-medium text-red-600">{error}</p> : null}

          {isLoading ? (
            <div className="glass mt-8 rounded-xl p-8 text-center">
              <div className="relative mx-auto mb-6 h-24 w-24">
                <div className="absolute inset-0 rounded-full border-4 border-slate-200" />
                <div className="absolute inset-0 animate-spin rounded-full border-4 border-blue-600 border-t-transparent" />
                <div className="absolute inset-0 flex items-center justify-center text-3xl text-blue-600">*</div>
              </div>
              <h3 className="mb-2 font-headline text-xl">Analyzing Content</h3>
              <p className="mb-4 text-sm text-slate-500">Processing linguistic markers and cross-referencing sources...</p>
              <div className="mx-auto h-1 max-w-md overflow-hidden rounded-full bg-slate-200">
                <div className="animate-pulse h-full w-2/3 rounded-full bg-gradient-to-r from-blue-600 to-amber-500" />
              </div>
            </div>
          ) : null}
        </section>

        {result ? (
          <section className="mx-auto max-w-[1600px] space-y-4 px-8">
            <ResultCard result={result} />
            <button
              className="rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-100"
              onClick={() => setResult(null)}
              type="button"
            >
              Analyze Another
            </button>
          </section>
        ) : null}

        {!result && !isLoading ? (
          <section className="mx-auto mt-24 max-w-4xl px-6 mb-24">
            <div className="grid grid-cols-1 gap-8 text-center md:grid-cols-3">
              <div className="space-y-3">
                <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-100 text-3xl text-blue-600">#</div>
                <h3 className="font-headline text-lg">Source Verification</h3>
                <p className="text-sm leading-relaxed text-slate-500">Cross-referenced against verified sources and fact-checking datasets.</p>
              </div>
              <div className="space-y-3">
                <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-amber-100 text-3xl text-amber-600">*</div>
                <h3 className="font-headline text-lg">Neural Analysis</h3>
                <p className="text-sm leading-relaxed text-slate-500">NLP models detect bias, sentiment, and manipulation markers.</p>
              </div>
              <div className="space-y-3">
                <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-100 text-3xl text-blue-600">!</div>
                <h3 className="font-headline text-lg">Explainable AI</h3>
                <p className="text-sm leading-relaxed text-slate-500">Transparent scoring with confidence and component-level evidence.</p>
              </div>
            </div>
          </section>
        ) : null}
      </main>

      <footer className="relative z-10 mt-32 w-full border-t border-slate-200/40 bg-slate-50/70">
        <div className="mx-auto grid w-full max-w-[1600px] grid-cols-1 gap-12 px-6 py-16 md:grid-cols-4">
          <div className="space-y-4 md:col-span-2">
            <div className="flex items-center gap-3">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-900 font-headline text-sm italic text-white">N</div>
              <div className="font-headline text-xl italic text-slate-900">NewsGuard</div>
            </div>
            <p className="max-w-sm text-sm leading-relaxed text-slate-500">This tool assists in identifying potential misinformation signals. Always verify news through multiple trusted sources.</p>
          </div>

          <div>
            <h4 className="mb-4 text-sm font-semibold uppercase tracking-wider text-slate-900">Product</h4>
            <div className="flex flex-col gap-3">
              <a className="text-sm text-slate-500 hover:text-blue-600" href="#">API Access</a>
              <a className="text-sm text-slate-500 hover:text-blue-600" href="#">Browser Extension</a>
              <a className="text-sm text-slate-500 hover:text-blue-600" href="#">Enterprise</a>
            </div>
          </div>

          <div>
            <h4 className="mb-4 text-sm font-semibold uppercase tracking-wider text-slate-900">Company</h4>
            <div className="flex flex-col gap-3">
              <Link to="/about-us" className="text-sm text-slate-500 hover:text-blue-600">About Us</Link>
              <Link to="/methodology" className="text-sm text-slate-500 hover:text-blue-600">Methodology</Link>
              <a className="text-sm text-slate-500 hover:text-blue-600" href="#">Contact</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default AnalyzerPage;
