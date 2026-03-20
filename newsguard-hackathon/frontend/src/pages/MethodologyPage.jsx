import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function MethodologyPage() {
  const [particles, setParticles] = useState([]);
  const [isDark, setIsDark] = useState(false);

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
          <Link to="/" className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-900 font-headline text-xl italic text-white">N</div>
            <div className="font-headline text-2xl italic text-slate-900">NewsGuard</div>
          </Link>
          <div className="hidden items-center gap-8 md:flex">
            <Link className="text-xs uppercase tracking-[0.2em] text-slate-500 transition-colors hover:text-slate-900" to="/">
              Analyzer
            </Link>
            <Link className="text-xs uppercase tracking-[0.2em] text-slate-500 transition-colors hover:text-slate-900" to="/about-us">
              About Us
            </Link>
            <Link className="border-b-2 border-slate-900 pb-1 text-xs font-semibold uppercase tracking-[0.2em] text-slate-900" to="/methodology">
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

      <main className="relative z-10 pt-32 pb-24">
        <section className="mx-auto max-w-4xl px-6 text-center mb-20">
          <h1 className="mb-6 font-headline text-5xl font-light leading-tight tracking-tight md:text-7xl">
            Methodology
          </h1>
          <p className="mx-auto mb-12 max-w-2xl text-lg leading-relaxed text-slate-600">
            Our fake news detection system combines machine learning, NLP, and source analysis to deliver accurate, explainable credibility assessments.
          </p>
        </section>

        <section className="mx-auto max-w-5xl px-6 mb-20">
          <h2 className="mb-12 font-headline text-4xl italic text-center">Technical Pipeline</h2>

          <div className="space-y-8">
            <div className="glass rounded-2xl p-8 text-slate-900">
              <div className="flex items-start gap-6">
                <div className="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-xl bg-blue-100 font-semibold text-blue-600">1</div>
                <div>
                  <h3 className="mb-3 font-headline text-2xl italic">Text Preprocessing</h3>
                  <p className="text-sm text-slate-700 mb-3">
                    Raw text is cleaned, normalized, and tokenized using industry-standard NLP techniques. URLs, emails, and special characters are removed while preserving semantic meaning.
                  </p>
                </div>
              </div>
            </div>

            <div className="glass rounded-2xl p-8 text-slate-900">
              <div className="flex items-start gap-6">
                <div className="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-xl bg-amber-100 font-semibold text-amber-600">2</div>
                <div>
                  <h3 className="mb-3 font-headline text-2xl italic">TF-IDF Vectorization</h3>
                  <p className="text-sm text-slate-700 mb-3">
                    Term Frequency-Inverse Document Frequency encoding transforms text into numerical features. We use bigram/unigram representation optimized for fake news detection patterns.
                  </p>
                </div>
              </div>
            </div>

            <div className="glass rounded-2xl p-8 text-slate-900">
              <div className="flex items-start gap-6">
                <div className="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-xl bg-blue-100 font-semibold text-blue-600">3</div>
                <div>
                  <h3 className="mb-3 font-headline text-2xl italic">Multi-Model Ensemble</h3>
                  <p className="text-sm text-slate-700 mb-3">
                    Multiple classifiers (LogisticRegression, PassiveAggressive) are trained on diverse datasets. Predictions are combined using weighted voting for robust consensus.
                  </p>
                </div>
              </div>
            </div>

            <div className="glass rounded-2xl p-8 text-slate-900">
              <div className="flex items-start gap-6">
                <div className="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-xl bg-amber-100 font-semibold text-amber-600">4</div>
                <div>
                  <h3 className="mb-3 font-headline text-2xl italic">Confidence Calibration</h3>
                  <p className="text-sm text-slate-700 mb-3">
                    Model confidence is calibrated to reflect true probability. Predictions below a configurable threshold are marked "Needs Verification" instead of forced binary classification.
                  </p>
                </div>
              </div>
            </div>

            <div className="glass rounded-2xl p-8 text-slate-900">
              <div className="flex items-start gap-6">
                <div className="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-xl bg-blue-100 font-semibold text-blue-600">5</div>
                <div>
                  <h3 className="mb-3 font-headline text-2xl italic">Explainability</h3>
                  <p className="text-sm text-slate-700 mb-3">
                    Each prediction includes score breakdowns showing contributions from linguistic markers, source signals, and structural features for user transparency.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="mx-auto max-w-5xl px-6">
          <h2 className="mb-12 font-headline text-4xl italic text-center">Datasets Used</h2>

          <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
            <div className="glass rounded-2xl p-6 text-slate-900">
              <h4 className="mb-2 font-headline text-lg italic">Kaggle Fake News</h4>
              <p className="text-sm text-slate-700 mb-2">
                Large corpus of real and fake news articles for foundational model training.
              </p>
              <p className="text-xs text-slate-500">Accuracy: 99.23%</p>
            </div>

            <div className="glass rounded-2xl p-6 text-slate-900">
              <h4 className="mb-2 font-headline text-lg italic">LIAR Dataset</h4>
              <p className="text-sm text-slate-700 mb-2">
                Claim-level labels from PolitiFact fact-checking articles for diverse perspectives.
              </p>
              <p className="text-xs text-slate-500">Trained Models: 62.02% accuracy</p>
            </div>

            <div className="glass rounded-2xl p-6 text-slate-900">
              <h4 className="mb-2 font-headline text-lg italic">FakeNewsNet</h4>
              <p className="text-sm text-slate-700 mb-2">
                Social media fake news network data from Politifact and GossipCop sources.
              </p>
              <p className="text-xs text-slate-500">Best Combined: 90.53%</p>
            </div>
          </div>
        </section>
      </main>

      <footer className="relative z-10 mt-12 w-full border-t border-slate-200/40 bg-slate-50/70">
        <div className="mx-auto grid w-full max-w-[1600px] grid-cols-1 gap-12 px-6 py-16 md:grid-cols-4">
          <div className="space-y-4 md:col-span-2">
            <div className="flex items-center gap-3">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-900 font-headline text-sm italic text-white">N</div>
              <div className="font-headline text-xl italic text-slate-900">NewsGuard</div>
            </div>
            <p className="max-w-sm text-sm leading-relaxed text-slate-500">Editorial integrity meets algorithmic precision. Verify content credibility in real-time.</p>
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
              <Link className="text-sm text-slate-500 hover:text-blue-600" to="/about-us">About Us</Link>
              <Link className="text-sm text-slate-500 hover:text-blue-600" to="/methodology">Methodology</Link>
              <a className="text-sm text-slate-500 hover:text-blue-600" href="#">Contact</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default MethodologyPage;
