// Enhanced Header Component with better branding and info
import { APP_NAME } from "../utils/constants";

function Header() {
  return (
    <header className="sticky top-0 z-40 border-b border-slate-200/50 bg-gradient-to-r from-slate-50 to-slate-100/50 backdrop-blur-sm">
      <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-4 py-4 sm:px-6">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-blue-500 to-blue-600 text-white font-bold">
            ✓
          </div>
          <div>
            <div className="text-lg font-bold tracking-tight text-slate-900">{APP_NAME}</div>
            <p className="text-xs text-slate-600">Real-time Fake News Detection</p>
          </div>
        </div>
        
        <nav className="flex items-center gap-4">
          <a 
            className="text-sm font-medium text-slate-600 rounded-md px-3 py-2 transition hover:bg-white hover:text-slate-900" 
            href="#analyzer"
          >
            Analyze
          </a>
          <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-green-100/50 border border-green-200/50">
            <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse"></div>
            <span className="text-xs font-medium text-green-700">System Online</span>
          </div>
        </nav>
      </div>
    </header>
  );
}

export default Header;
