import { useMemo, useState } from "react";

import LoadingSpinner from "./LoadingSpinner";

function InputBox({ onAnalyze, isLoading, mode, onModeChange, modelOptions }) {
  const [text, setText] = useState("");
  const [url, setUrl] = useState("");
  const [checkUrl, setCheckUrl] = useState(false);
  const charCount = text.length;
  const wordCount = useMemo(() => text.trim().split(/\s+/).filter(Boolean).length, [text]);

  const buttonDisabled = useMemo(() => {
    return isLoading || !text.trim() || text.trim().length < 80 || wordCount < 12;
  }, [isLoading, text, wordCount]);

  const statusText = useMemo(() => {
    if (!text.trim()) return "Ready to analyze";
    if (text.trim().length < 80 || wordCount < 12) {
      return "Enter at least 80 characters and 12 words for reliable analysis";
    }
    return "Ready for verification";
  }, [text, wordCount]);

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!buttonDisabled) {
      onAnalyze(text, mode, url, checkUrl);
    }
  };

  return (
    <form className="glass rounded-2xl shadow-[0_20px_60px_-15px_rgba(0,0,0,0.1)]" onSubmit={handleSubmit}>
      {/* Optional Features Section */}
      <div className="border-b border-slate-200/50 bg-gradient-to-r from-slate-50/50 to-slate-100/30 px-8 py-4">
        <p className="text-xs font-semibold text-slate-600 mb-3 uppercase">Optional Checks</p>
        <div className="flex flex-col gap-3 md:flex-row md:items-center md:gap-4">
          {/* URL Verification */}
          <div className="flex flex-1 gap-2">
            <input
              type="url"
              placeholder="https://example.com/article"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="flex-1 rounded-lg border border-slate-300 bg-white px-3 py-2 text-xs text-slate-900 placeholder:text-slate-400 focus:border-blue-500 focus:ring-blue-500"
            />
            <label className="flex items-center gap-1.5 px-3 py-2 rounded-lg bg-blue-100 hover:bg-blue-200 cursor-pointer transition whitespace-nowrap">
              <input
                type="checkbox"
                checked={checkUrl}
                onChange={(e) => setCheckUrl(e.target.checked)}
                className="w-4 h-4"
              />
              <span className="text-xs font-medium text-blue-700">URL Check</span>
            </label>
          </div>


        </div>
      </div>

      {/* Main Text Input - FAKE NEWS DETECTION (Always enabled) */}
      <div className="p-1 border-b border-amber-100 bg-amber-50/40">
        <div className="px-8 py-2">
          <p className="text-xs font-semibold text-amber-700">Paste any news text below</p>
        </div>
        <textarea
          id="news-input"
          className="min-h-[280px] w-full resize-none border-none bg-transparent p-8 text-base leading-relaxed text-slate-900 caret-slate-900 placeholder:text-slate-400 focus:ring-0"
          placeholder="e.g. &quot;SHOCKING: Scientists EXPOSE hidden cure banned by Big Pharma...&quot;"
          value={text}
          onChange={(event) => setText(event.target.value)}
        />
      </div>

      <div className="flex flex-col items-center justify-between gap-4 border-t border-slate-200/50 bg-slate-50/50 px-6 py-4 md:flex-row">
        <div className="flex flex-col gap-3 md:flex-row md:items-center md:gap-4">
          <span className="rounded-full bg-slate-200 px-3 py-1.5 text-xs font-medium text-slate-600">{charCount} chars / {wordCount} words</span>
          <div className="hidden h-4 w-px bg-slate-300 md:block" />
          <span className="text-xs text-slate-500">{statusText}</span>
          <select
            id="mode-select"
            value={mode}
            onChange={(event) => onModeChange(event.target.value)}
            className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-xs font-semibold text-slate-700 focus:border-slate-500 focus:ring-slate-500"
          >
            {modelOptions.map((entry) => {
              const accuracyText = entry.accuracy != null ? ` (${(entry.accuracy * 100).toFixed(2)}%)` : "";
              return (
                <option key={entry.mode} value={entry.mode}>
                  {entry.label}{accuracyText}
                </option>
              );
            })}
          </select>
        </div>

        <div className="flex w-full items-center gap-3 md:w-auto">
          <button
            type="button"
            className="inline-flex flex-1 items-center justify-center gap-2 rounded-lg bg-slate-200 px-4 py-3 text-sm font-medium text-slate-700 transition hover:bg-slate-300 md:flex-none"
            onClick={() => {
              setText("");
              setUrl("");
            }}
          >
            Clear
          </button>
          <button
            type="submit"
            disabled={buttonDisabled}
            className="inline-flex flex-1 items-center justify-center gap-3 rounded-lg bg-slate-900 px-8 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-400 md:flex-none"
          >
            {isLoading ? (
              <>
                <LoadingSpinner />
                Analyzing
              </>
            ) : (
              "Analyze Now"
            )}
          </button>
        </div>
      </div>

      <div className={`px-8 pb-6 transition-opacity duration-500 ${isLoading ? "opacity-100" : "opacity-0"}`}>
        <div className="relative h-[2px] w-64 overflow-hidden rounded-full bg-slate-300/80">
          <div className="absolute inset-y-0 left-[-40%] w-1/3 rounded-full bg-blue-700 animate-loading" />
        </div>
      </div>
    </form>
  );
}

export default InputBox;
