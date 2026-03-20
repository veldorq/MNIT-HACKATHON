import { APP_NAME } from "../utils/constants";

function Header() {
  return (
    <header className="mx-auto flex w-full max-w-6xl items-center justify-between px-4 py-6 sm:px-6">
      <div className="text-xl font-bold tracking-tight text-slate-900">{APP_NAME}</div>
      <nav className="text-sm font-medium text-slate-600">
        <a className="rounded-md px-3 py-2 transition hover:bg-slate-100" href="#analyzer">
          Analyzer
        </a>
      </nav>
    </header>
  );
}

export default Header;
