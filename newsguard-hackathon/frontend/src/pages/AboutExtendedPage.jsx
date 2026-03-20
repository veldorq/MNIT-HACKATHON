import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function AboutExtendedPage() {
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
            <Link className="text-xs uppercase tracking-[0.2em] text-slate-500 transition-colors hover:text-slate-900" to="/methodology">
              Methodology
            </Link>
            <Link className="border-b-2 border-slate-900 pb-1 text-xs font-semibold uppercase tracking-[0.2em] text-slate-900" to="/about">
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
            About
          </h1>
          <p className="mx-auto mb-12 max-w-2xl text-lg leading-relaxed text-slate-600">
            Learn more about our organization, team, and the impact we're making in the fight against misinformation.
          </p>
        </section>

        <section className="mx-auto max-w-5xl px-6 mb-20">
          <h2 className="mb-12 font-headline text-4xl italic text-center">Our Story</h2>

          <div className="glass rounded-2xl p-8 text-slate-900">
            <div className="prose prose-sm max-w-none space-y-4 text-sm text-slate-700">
              <p>
                We built NewsGuard because we were frustrated. In a world where false information spreads faster than corrections, we realized we needed a better way to spot what's credible and what isn't. That's why we're building tools people can actually trust.
              </p>
              <p>
                Our team is a mix of ML engineers, researchers, and people obsessed with truth. We built this to be transparent—when something looks suspicious, we show you <em>why</em>, not just a red flag. No black boxes, no magic. Just honest analysis.
              </p>
              <p>
                We're helping people make smarter decisions about what they read. Whether you're checking a headline or doing research, NewsGuard cuts through the noise. It's not perfect, but it's honest—and that matters.
              </p>
            </div>
          </div>
        </section>

        <section className="mx-auto max-w-5xl px-6 mb-20">
          <h2 className="mb-12 font-headline text-4xl italic text-center">Our Impact</h2>

          <div className="grid grid-cols-1 gap-8 md:grid-cols-2">
            <div className="glass rounded-2xl p-8 text-slate-900">
              <div className="mb-4 inline-block rounded-3xl bg-blue-100 px-8 py-4">
                <span className="font-headline text-5xl font-light text-blue-600">99.23%</span>
              </div>
              <h4 className="mb-3 font-headline text-lg italic font-light">Peak Accuracy</h4>
              <p className="text-sm text-slate-700">
                Achieved using TF-IDF vectorization and Passive Aggressive Classifier on 8,837 Kaggle test samples.
              </p>
            </div>

            <div className="glass rounded-2xl p-8 text-slate-900">
              <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-amber-100">
                <span className="font-headline text-3xl italic text-amber-600">4</span>
              </div>
              <h4 className="mb-3 font-headline text-xl italic">ML Models</h4>
              <p className="text-sm text-slate-700">
                Multiple trained models using Kaggle, LIAR, and multi-source datasets for robust predictions.
              </p>
            </div>

            <div className="glass rounded-2xl p-8 text-slate-900">
              <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-100">
                <span className="font-headline text-3xl italic text-blue-600">⚡</span>
              </div>
              <h4 className="mb-3 font-headline text-xl italic">Instant Analysis</h4>
              <p className="text-sm text-slate-700">
                Real-time ML processing—results delivered in under a second with explainable signals.
              </p>
            </div>

            <div className="glass rounded-2xl p-8 text-slate-900">
              <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-amber-100">
                <span className="font-headline text-3xl italic text-amber-600">🔓</span>
              </div>
              <h4 className="mb-3 font-headline text-xl italic">Open & Honest</h4>
              <p className="text-sm text-slate-700">
                100% open source. No hidden metrics, no inflated claims. Just transparent ML detection.
              </p>
            </div>
          </div>
        </section>

        <section className="mx-auto max-w-5xl px-6">
          <h2 className="mb-12 font-headline text-4xl italic text-center">Get Involved</h2>

          <div className="glass rounded-2xl border border-slate-200/30 p-8 text-center text-slate-900">
            <h3 className="mb-4 font-headline text-2xl italic">Join Our Mission</h3>
            <p className="mb-8 max-w-2xl mx-auto text-sm text-slate-700">
              Whether you're a researcher, developer, journalist, or organization committed to fighting misinformation, there are many ways to collaborate with NewsGuard.
            </p>
            <div className="flex flex-col gap-4 sm:flex-row justify-center">
              <button className="rounded-xl bg-slate-900 px-8 py-3 text-sm font-medium text-white transition-all hover:bg-slate-800">
                Contact Us
              </button>
              <button className="rounded-xl border border-slate-300 bg-white px-8 py-3 text-sm font-medium text-slate-900 transition-all hover:bg-slate-50">
                API Documentation
              </button>
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

export default AboutExtendedPage;
