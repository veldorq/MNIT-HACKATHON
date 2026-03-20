import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { TAGLINE } from "../utils/constants";

function LandingPage() {
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
            <Link className="border-b-2 border-slate-900 pb-1 text-xs font-semibold uppercase tracking-[0.2em] text-slate-900" to="/">
              Home
            </Link>
            <Link className="text-xs uppercase tracking-[0.2em] text-slate-500 transition-colors hover:text-slate-900" to="/analyzer">
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
            <Link to="/analyzer" className="rounded-full bg-slate-900 px-6 py-2.5 text-sm font-medium text-white transition-all hover:bg-slate-800 inline-block">
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      <main className="relative z-10 pb-24 pt-32">
        {/* Landing Section */}
        <section className="mx-auto mb-32 max-w-5xl px-6 text-center">
          <div className="mb-8 inline-flex items-center gap-2 rounded-full border border-blue-200 bg-blue-100/60 px-4 py-2 text-xs font-semibold uppercase tracking-wider text-blue-900">
            <span className="h-2 w-2 rounded-full bg-blue-600" />
            AI-Powered Verification
          </div>
          <h1 className="mb-6 font-headline text-5xl font-light leading-tight tracking-tight md:text-7xl">
            Can You Trust What You're Reading?
          </h1>
          <p className="mx-auto mb-12 max-w-2xl text-lg leading-relaxed text-slate-600">NewsGuard uses machine learning to analyze news articles and headlines — flagging sensational language, uncertainty markers, and credibility signals in seconds.</p>

          <div className="mt-16 flex flex-col items-center gap-4">
            <Link 
              to="/analyzer"
              className="rounded-lg bg-gradient-to-r from-blue-600 to-blue-700 px-8 py-3.5 text-sm font-semibold text-white transition-all hover:from-blue-700 hover:to-blue-800 shadow-lg hover:shadow-xl inline-block"
            >
              Try It Free — Analyze a Headline
            </Link>
            <p className="text-xs text-slate-500">Trained on the Kaggle Fake and Real News Dataset · Passive Aggressive Classifier · Built for accuracy, not assumptions</p>
          </div>

          <div className="mt-16 flex flex-wrap justify-center gap-8 text-center md:gap-16">
            <div className="space-y-1">
              <div className="font-headline text-3xl font-light text-slate-900">99.23%</div>
              <div className="text-xs font-medium uppercase tracking-widest text-slate-500">Peak Accuracy</div>
            </div>
            <div className="hidden h-8 w-px bg-slate-300 md:block" />
            <div className="space-y-1">
              <div className="font-headline text-3xl font-light text-slate-900">8.8K+</div>
              <div className="text-xs font-medium uppercase tracking-widest text-slate-500">Training Samples</div>
            </div>
            <div className="hidden h-8 w-px bg-slate-300 md:block" />
            <div className="space-y-1">
              <div className="font-headline text-3xl font-light text-slate-900">TF-IDF</div>
              <div className="text-xs font-medium uppercase tracking-widest text-slate-500">ML Vectorization</div>
            </div>
          </div>
        </section>

        {/* Why NewsGuard Section */}
        <section className="mx-auto mb-24 max-w-5xl px-6">
          <div className="rounded-2xl border border-slate-200/60 bg-gradient-to-br from-slate-50/50 to-blue-50/30 p-12 backdrop-blur-sm">
            <h2 className="mb-12 text-center font-headline text-3xl font-light text-slate-900">Why NewsGuard?</h2>
            <div className="grid grid-cols-1 gap-8 md:grid-cols-2">
              <div className="space-y-4">
                <div className="flex items-start gap-4">
                  <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg bg-blue-100 text-blue-600 font-headline">🎯</div>
                  <div>
                    <h3 className="font-headline text-lg text-slate-900">Highly Accurate</h3>
                    <p className="text-sm text-slate-600">99.23% accuracy using TF-IDF vectorization and passive-aggressive machine learning, trained on 8,837 labeled news samples.</p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg bg-amber-100 text-amber-600 font-headline">⚡</div>
                  <div>
                    <h3 className="font-headline text-lg text-slate-900">Instant Analysis</h3>
                    <p className="text-sm text-slate-600">Get comprehensive credibility reports in under a second. No long wait times, no unnecessary complexity.</p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg bg-blue-100 text-blue-600 font-headline">🔍</div>
                  <div>
                    <h3 className="font-headline text-lg text-slate-900">Explainable Results</h3>
                    <p className="text-sm text-slate-600">See exactly which language patterns triggered the credibility analysis — no black box predictions.</p>
                  </div>
                </div>
              </div>
              <div className="space-y-4">
                <div className="flex items-start gap-4">
                  <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg bg-amber-100 text-amber-600 font-headline">📊</div>
                  <div>
                    <h3 className="font-headline text-lg text-slate-900">Hybrid Detection</h3>
                    <p className="text-sm text-slate-600">Combines machine learning classification with keyword signal detection for robust analysis of sensational language and credibility markers.</p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg bg-blue-100 text-blue-600 font-headline">🛡️</div>
                  <div>
                    <h3 className="font-headline text-lg text-slate-900">Privacy First</h3>
                    <p className="text-sm text-slate-600">Your texts are analyzed locally. We don't store, log, or share your data or analysis history.</p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg bg-amber-100 text-amber-600 font-headline">✨</div>
                  <div>
                    <h3 className="font-headline text-lg text-slate-900">100% Free & Open</h3>
                    <p className="text-sm text-slate-600">No paywalls, no hidden tiers. All source code available. Built by the community, for everyone.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* How It Works Section */}
        <section className="mx-auto mb-24 max-w-5xl px-6">
          <h2 className="mb-12 text-center font-headline text-3xl font-light text-slate-900">How It Works</h2>
          <div className="grid grid-cols-1 gap-6 md:grid-cols-4">
            <div className="rounded-xl border border-slate-200/60 bg-white/60 backdrop-blur-sm p-6 text-center">
              <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-blue-100 font-headline text-xl text-blue-600">1</div>
              <h3 className="mb-2 font-headline text-lg text-slate-900">Paste Content</h3>
              <p className="text-sm text-slate-600">Copy-paste any article, headline, or news snippet to analyze.</p>
            </div>
            <div className="rounded-xl border border-slate-200/60 bg-white/60 backdrop-blur-sm p-6 text-center">
              <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-amber-100 font-headline text-xl text-amber-600">2</div>
              <h3 className="mb-2 font-headline text-lg text-slate-900">AI Scans for Signals</h3>
              <p className="text-sm text-slate-600">NewsGuard preprocesses your text and runs it through a TF-IDF vectorizer and Passive Aggressive Classifier — a machine learning model trained on thousands of real and fake news articles from Kaggle.</p>
            </div>
            <div className="rounded-xl border border-slate-200/60 bg-white/60 backdrop-blur-sm p-6 text-center">
              <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-blue-100 font-headline text-xl text-blue-600">3</div>
              <h3 className="mb-2 font-headline text-lg text-slate-900">Get Your Credibility Report</h3>
              <p className="text-sm text-slate-600">Receive an instant credibility score, a fake probability rating, and a keyword breakdown highlighting sensational, uncertain, and suspicious language patterns detected in the text.</p>
            </div>
            <div className="rounded-xl border border-slate-200/60 bg-white/60 backdrop-blur-sm p-6 text-center">
              <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-amber-100 font-headline text-xl text-amber-600">4</div>
              <h3 className="mb-2 font-headline text-lg text-slate-900">Make Decisions</h3>
              <p className="text-sm text-slate-600">Use insights to verify credibility before sharing or trusting content. Always cross-check with multiple trusted sources.</p>
            </div>
          </div>
        </section>

        {/* Trust Section */}
        <section className="mx-auto mb-24 max-w-5xl px-6">
          <div className="rounded-2xl border border-blue-200/60 bg-gradient-to-r from-blue-50/60 to-amber-50/40 backdrop-blur-sm p-12">
            <h2 className="mb-12 text-center font-headline text-2xl font-light text-slate-900">Built with Real Data</h2>
            <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
              <div className="text-center">
                <div className="mb-3 text-xl font-semibold text-blue-600">8,837</div>
                <p className="text-sm text-slate-600">Kaggle Test Samples</p>
              </div>
              <div className="text-center">
                <div className="mb-3 text-xl font-semibold text-amber-600">Multiple</div>
                <p className="text-sm text-slate-600">ML Models & Datasets</p>
              </div>
              <div className="text-center">
                <div className="mb-3 text-xl font-semibold text-blue-600">100%</div>
                <p className="text-sm text-slate-600">Open Source</p>
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer className="relative z-10 mt-32 w-full border-t border-slate-200/40 bg-slate-50/70">
        <div className="mx-auto grid w-full max-w-[1600px] grid-cols-1 gap-12 px-6 py-16 md:grid-cols-4">
          <div className="space-y-4 md:col-span-2">
            <div className="flex items-center gap-3">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-900 font-headline text-sm italic text-white">N</div>
              <div className="font-headline text-xl italic text-slate-900">NewsGuard</div>
            </div>
            <p className="max-w-sm text-sm leading-relaxed text-slate-500">NewsGuard — Read with confidence. An open-source ML project for detecting misinformation signals in news text. Built with Python, Flask, React, and scikit-learn using the Kaggle Fake & Real News Dataset.</p>
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

export default LandingPage;
