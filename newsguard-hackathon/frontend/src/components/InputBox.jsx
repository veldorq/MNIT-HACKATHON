import { useMemo, useState } from "react";

import LoadingSpinner from "./LoadingSpinner";

function InputBox({ onAnalyze, isLoading, mode, onModeChange, modelOptions }) {
  const [text, setText] = useState("");
  const [url, setUrl] = useState("");
  const [checkUrl, setCheckUrl] = useState(false);
  const [showTips, setShowTips] = useState(!text);
  
  const charCount = text.length;
  const wordCount = useMemo(() => text.trim().split(/\s+/).filter(Boolean).length, [text]);
  
  const minChars = 80;
  const minWords = 12;
  const charProgress = Math.min((charCount / minChars) * 100, 100);
  const wordProgress = Math.min((wordCount / minWords) * 100, 100);

  const buttonDisabled = useMemo(() => {
    return isLoading || !text.trim() || text.trim().length < minChars || wordCount < minWords;
  }, [isLoading, text, wordCount]);

  const statusText = useMemo(() => {
    if (!text.trim()) return "Ready to analyze";
    if (text.trim().length < minChars) {
      const charsNeeded = minChars - text.trim().length;
      return `${charsNeeded} more characters needed`;
    }
    if (wordCount < minWords) {
      const wordsNeeded = minWords - wordCount;
      return `${wordsNeeded} more words needed`;
    }
    return "✓ Ready for analysis";
  }, [text, wordCount]);

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!buttonDisabled) {
      onAnalyze(text, mode, url, checkUrl);
    }
  };

  // Keyboard shortcut: Ctrl+Enter or Cmd+Enter to submit
  const handleKeyDown = (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter" && !buttonDisabled) {
      handleSubmit(e);
    }
  };

  return (
    <form className="glass rounded-2xl shadow-[0_20px_60px_-15px_rgba(0,0,0,0.1)]" onSubmit={handleSubmit}>
      {/* Optional Features Section */}
      <div className="border-b border-slate-200/50 bg-gradient-to-r from-slate-50/50 to-slate-100/30 px-8 py-4">
        <p className="text-xs font-semibold text-slate-600 mb-3 uppercase tracking-wider">Optional Checks</p>
        <div className="flex flex-col gap-3 md:flex-row md:items-center md:gap-4">
          {/* URL Verification */}
          <div className="flex flex-1 gap-2">
            <input
              type="url"
              placeholder="https://example.com/article"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="flex-1 rounded-lg border border-slate-300 bg-white px-3 py-2 text-xs text-slate-900 placeholder:text-slate-400 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition"
            />
            <label className="flex items-center gap-1.5 px-3 py-2 rounded-lg bg-blue-100 hover:bg-blue-200 cursor-pointer transition whitespace-nowrap">
              <input
                type="checkbox"
                checked={checkUrl}
                onChange={(e) => setCheckUrl(e.target.checked)}
                className="w-4 h-4 rounded"
              />
              <span className="text-xs font-medium text-blue-700">URL Check</span>
            </label>
          </div>
        </div>
      </div>

      {/* Main Text Input - FAKE NEWS DETECTION (Always enabled) */}
      <div className="border-b border-amber-100 bg-amber-50/40">
        <div className="px-8 py-3 flex items-center justify-between">
          <p className="text-xs font-semibold text-amber-700">📰 Paste any news text below</p>
          <button
            type="button"
            onClick={() => setShowTips(!showTips)}
            className="text-xs text-amber-600 hover:text-amber-700 font-medium underline"
          >
            {showTips ? "Hide tips" : "Show tips"}
          </button>
        </div>
        
        {showTips && (
          <div className="px-8 pb-3 space-y-1">
            <p className="text-xs text-amber-700">💡 Tips for accurate detection:</p>
            <ul className="text-xs text-amber-600 space-y-0.5 ml-4">
              <li>• Paste entire article paragraphs for best results</li>
              <li>• Include headlines and main body text</li>
              <li>• Avoid just headlines or single sentences</li>
            </ul>
          </div>
        )}
        
        <textarea
          id="news-input"
          className="min-h-[280px] w-full resize-none border-none bg-transparent p-8 text-base leading-relaxed text-slate-900 caret-slate-900 placeholder:text-slate-400 focus:ring-0 focus:outline-none"
          placeholder="Example: 'BREAKING: Scientists discover that water can think! New research shows water has consciousness and can communicate through electromagnetic waves...'"
          value={text}
          onChange={(event) => {
            setText(event.target.value);
            setShowTips(!event.target.value);
          }}
          onKeyDown={handleKeyDown}
        />
      </div>

      {/* Progress Indicators */}
      <div className="border-b border-slate-200/50 bg-slate-50/50 px-8 py-4 space-y-3">
        <div className="space-y-1">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-600">Character count: {charCount}/{minChars}</span>
            <span className={`text-xs font-medium ${charCount >= minChars ? 'text-green-600' : 'text-amber-600'}`}>
              {charProgress.toFixed(0)}%
            </span>
          </div>
          <div className="h-1.5 w-full rounded-full bg-slate-300 overflow-hidden">
            <div 
              className={`h-full rounded-full transition-all duration-300 ${charCount >= minChars ? 'bg-green-500' : 'bg-amber-500'}`}
              style={{ width: `${charProgress}%` }}
            />
          </div>
        </div>
        
        <div className="space-y-1">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-600">Word count: {wordCount}/{minWords}</span>
            <span className={`text-xs font-medium ${wordCount >= minWords ? 'text-green-600' : 'text-amber-600'}`}>
              {wordProgress.toFixed(0)}%
            </span>
          </div>
          <div className="h-1.5 w-full rounded-full bg-slate-300 overflow-hidden">
            <div 
              className={`h-full rounded-full transition-all duration-300 ${wordCount >= minWords ? 'bg-green-500' : 'bg-amber-500'}`}
              style={{ width: `${wordProgress}%` }}
            />
          </div>
        </div>
      </div>

      {/* Bottom Controls */}
      <div className="flex flex-col items-center justify-between gap-4 border-t border-slate-200/50 bg-slate-50/50 px-6 py-4 md:flex-row">
        <div className="flex flex-col gap-2 md:flex-row md:items-center md:gap-4">
          <span className={`rounded-full px-3 py-1.5 text-xs font-medium transition ${
            buttonDisabled ? 'bg-slate-200 text-slate-600' : 'bg-green-100 text-green-700'
          }`}>
            {statusText}
          </span>
          
          <select
            id="mode-select"
            value={mode}
            onChange={(event) => onModeChange(event.target.value)}
            className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-xs font-semibold text-slate-700 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition"
          >
            <optgroup label="Detection Models">
              {modelOptions.map((entry) => {
                const accuracyText = entry.accuracy != null ? ` (${(entry.accuracy * 100).toFixed(1)}%)` : "";
                return (
                  <option key={entry.mode} value={entry.mode}>
                    {entry.label}{accuracyText}
                  </option>
                );
              })}
            </optgroup>
          </select>
        </div>

        <div className="flex w-full items-center gap-3 md:w-auto">
          <button
            type="button"
            className="inline-flex flex-1 items-center justify-center gap-2 rounded-lg bg-slate-200 hover:bg-slate-300 px-4 py-3 text-sm font-medium text-slate-700 transition duration-200 md:flex-none"
            onClick={() => {
              setText("");
              setUrl("");
              setShowTips(true);
            }}
          >
            Clear
          </button>
          <button
            type="submit"
            disabled={buttonDisabled}
            title={buttonDisabled ? "Enter at least 80 characters and 12 words" : "Analyze (Ctrl+Enter)"}
            className="inline-flex flex-1 items-center justify-center gap-3 rounded-lg bg-gradient-to-r from-slate-900 to-slate-800 hover:from-slate-800 hover:to-slate-700 px-8 py-3 text-sm font-semibold text-white transition duration-200 disabled:cursor-not-allowed disabled:opacity-50 disabled:from-slate-400 disabled:to-slate-400 md:flex-none"
          >
            {isLoading ? (
              <>
                <LoadingSpinner />
                <span>Analyzing...</span>
              </>
            ) : (
              <span>🔍 Analyze Now</span>
            )}
          </button>
        </div>
      </div>

      {isLoading && (
        <div className={`px-8 pb-6 transition-opacity duration-500 opacity-100`}>
          <div className="relative h-[2px] w-full max-w-xs rounded-full bg-slate-300/80 overflow-hidden">
            <div className="absolute inset-y-0 left-[-40%] w-1/3 rounded-full bg-gradient-to-r from-blue-500 to-blue-700 animate-pulse" />
          </div>
          <p className="text-xs text-slate-500 mt-2">Processing your article...</p>
        </div>
      )}
    </form>
  );
}

export default InputBox;
