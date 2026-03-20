import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function AboutPage() {
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
            <Link className="border-b-2 border-slate-900 pb-1 text-xs font-semibold uppercase tracking-[0.2em] text-slate-900" to="/about-us">
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

      <main className="relative z-10 pt-32 pb-24">
        <section className="mx-auto max-w-4xl px-6 text-center mb-20">
          <h1 className="mb-6 font-headline text-5xl font-light leading-tight tracking-tight md:text-7xl">
            About Us
          </h1>
          <p className="mx-auto mb-12 max-w-2xl text-lg leading-relaxed text-slate-600">
            NewsGuard is dedicated to combating misinformation through advanced AI-powered analysis, real-time verification, and transparent methodology.
          </p>
        </section>

        <section className="mx-auto max-w-5xl px-6 grid grid-cols-1 gap-12 md:grid-cols-2 mb-20">
          <div className="glass rounded-2xl p-8 text-slate-900">
            <h3 className="mb-4 font-headline text-2xl italic">Our Mission</h3>
            <p className="text-sm leading-relaxed text-slate-700">
              We believe that access to trustworthy information is fundamental to a healthy society. Our mission is to empower individuals and organizations with the tools and insights needed to verify news credibility and combat the spread of misinformation.
            </p>
          </div>

          <div className="glass rounded-2xl p-8 text-slate-900">
            <h3 className="mb-4 font-headline text-2xl italic">Our Vision</h3>
            <p className="text-sm leading-relaxed text-slate-700">
              We envision a future where reliable information prevails. Through cutting-edge machine learning, curated datasets, and human expertise, we aim to restore trust in media and create a more informed, resilient society.
            </p>
          </div>
        </section>

        <section className="mx-auto max-w-5xl px-6 mb-20">
          <h2 className="mb-12 font-headline text-4xl italic text-center">Why NewsGuard?</h2>
          <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
            <div className="glass rounded-2xl p-8 text-center text-slate-900">
              <div className="mb-4 inline-flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-100">
                <span className="text-3xl text-blue-600">*</span>
              </div>
              <h4 className="mb-3 font-headline text-lg">Advanced AI</h4>
              <p className="text-sm text-slate-700">Real-time credibility scoring powered by machine learning trained on verified datasets.</p>
            </div>

            <div className="glass rounded-2xl p-8 text-center text-slate-900">
              <div className="mb-4 inline-flex h-16 w-16 items-center justify-center rounded-2xl bg-amber-100">
                <span className="text-3xl text-amber-600">#</span>
              </div>
              <h4 className="mb-3 font-headline text-lg">Transparent</h4>
              <p className="text-sm text-slate-700">Explainable analysis with breakdowns of linguistic patterns and source reliability signals.</p>
            </div>

            <div className="glass rounded-2xl p-8 text-center text-slate-900">
              <div className="mb-4 inline-flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-100">
                <span className="text-3xl text-blue-600">!</span>
              </div>
              <h4 className="mb-3 font-headline text-lg">Reliable</h4>
              <p className="text-sm text-slate-700">Calibrated confidence metrics and conservative thresholds that avoid overconfident misclassifications.</p>
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

export default AboutPage;
