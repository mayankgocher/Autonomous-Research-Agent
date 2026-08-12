import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Search, History, Sparkles, FileText, Download, Loader2, ChevronRight, CheckCircle2 } from 'lucide-react';

export default function Dashboard() {
  const [query, setQuery] = useState('');
  const [history, setHistory] = useState([]);
  const [selectedResearch, setSelectedResearch] = useState(null);
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const res = await axios.get('http://localhost:8000/history');
      setHistory(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  const handleResearch = async () => {
    if (!query) return;
    setLoading(true);
    try {
      await axios.post('http://localhost:8000/research', { query });
      setQuery('');
      fetchHistory();
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const loadReport = async (id) => {
    setSelectedResearch(id);
    setReport(null);
    try {
      const res = await axios.get(`http://localhost:8000/report/${id}`);
      setReport(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="flex h-screen overflow-hidden bg-[url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2564&auto=format&fit=crop')] bg-cover bg-center">
      {/* Dark overlay for the background image */}
      <div className="absolute inset-0 bg-zinc-950/80 backdrop-blur-3xl"></div>

      {/* Sidebar */}
      <div className="relative w-72 glass-panel border-r border-white/5 flex flex-col z-10">
        <div className="p-6 border-b border-white/5 flex items-center gap-3">
          <div className="p-2 bg-blue-500/20 rounded-lg border border-blue-500/30 text-blue-400">
            <Sparkles size={24} className="animate-pulse" />
          </div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400 bg-clip-text text-transparent">
            AuraSearch
          </h1>
        </div>
        <div className="flex-1 overflow-y-auto p-4 space-y-2">
          <div className="flex items-center justify-between mb-4 px-2">
            <span className="text-xs font-semibold text-zinc-400 uppercase tracking-wider flex items-center gap-2">
              <History size={14} /> Recent Research
            </span>
            <button onClick={fetchHistory} className="text-zinc-500 hover:text-blue-400 transition-colors" title="Refresh History">
              <History size={14} className="rotate-180" />
            </button>
          </div>

          {history.length === 0 ? (
            <div className="text-zinc-500 text-sm p-4 text-center border border-dashed border-zinc-700/50 rounded-xl bg-zinc-800/20">
              No previous research. <br /> Start a new one!
            </div>
          ) : (
            history.map((item) => (
              <div 
                key={item.id} 
                onClick={() => loadReport(item.id)}
                className={`group p-4 rounded-xl cursor-pointer transition-all duration-300 ${
                  selectedResearch === item.id 
                    ? 'bg-blue-600/20 border border-blue-500/30 shadow-[0_0_15px_rgba(59,130,246,0.15)]' 
                    : 'bg-zinc-800/30 border border-white/5 hover:bg-zinc-800/50 hover:border-white/10'
                }`}
              >
                <div className="text-sm font-medium text-zinc-200 line-clamp-2 leading-snug group-hover:text-blue-300 transition-colors">
                  {item.query}
                </div>
                <div className="mt-3 flex items-center justify-between">
                  <span className={`text-[10px] font-medium px-2 py-1 rounded-full flex items-center gap-1 ${
                    item.status === 'completed' 
                      ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' 
                      : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                  }`}>
                    {item.status === 'completed' ? <CheckCircle2 size={10} /> : <Loader2 size={10} className="animate-spin" />}
                    {item.status}
                  </span>
                  <ChevronRight size={14} className={`transition-transform ${selectedResearch === item.id ? 'text-blue-400 translate-x-1' : 'text-zinc-600 group-hover:text-zinc-400'}`} />
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className="relative flex-1 flex flex-col overflow-hidden z-10">
        {/* Header / Search Area */}
        <header className="px-8 py-10 md:py-16 flex flex-col items-center justify-center relative border-b border-white/5 bg-zinc-900/30 backdrop-blur-md">
          <h2 className="text-3xl md:text-5xl font-extrabold mb-8 text-center text-zinc-100 tracking-tight animate-fade-in-up">
            What would you like to explore?
          </h2>
          <div className="w-full max-w-3xl relative focus-glow rounded-full transition-all duration-500 animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
            <div className="absolute inset-y-0 left-6 flex items-center pointer-events-none">
              <Search className="text-zinc-400" size={24} />
            </div>
            <input 
              type="text" 
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleResearch()}
              className="w-full bg-zinc-900/60 border border-white/10 rounded-full py-5 pl-16 pr-16 text-lg text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-blue-500/50 focus:bg-zinc-900/80 transition-all shadow-xl backdrop-blur-xl"
              placeholder="Research autonomous AI agents, multimodal models..."
            />
            <button 
              onClick={handleResearch}
              disabled={loading || !query}
              className="absolute right-3 top-3 bottom-3 bg-blue-600 hover:bg-blue-500 text-white rounded-full transition-all duration-300 flex items-center justify-center w-12 hover:shadow-[0_0_20px_rgba(59,130,246,0.4)] disabled:opacity-50 disabled:hover:shadow-none disabled:cursor-not-allowed"
            >
              {loading ? <Loader2 size={20} className="animate-spin" /> : <Sparkles size={20} />}
            </button>
          </div>
        </header>

        {/* Dashboard Body / Results Area */}
        <main className="flex-1 overflow-y-auto p-8 md:p-12 scroll-smooth">
          <div className="max-w-4xl mx-auto h-full">
            {!selectedResearch ? (
              <div className="flex flex-col items-center justify-center h-full text-center space-y-6 text-zinc-500 animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
                <div className="w-32 h-32 rounded-full bg-zinc-800/30 flex items-center justify-center mb-4 border border-white/5 shadow-2xl animate-float">
                  <FileText size={48} className="text-zinc-600" />
                </div>
                <h3 className="text-2xl font-semibold text-zinc-300">Discover Deep Insights</h3>
                <p className="text-lg max-w-md">Select a topic from the sidebar or enter a new query to generate a comprehensive, AI-driven research report.</p>
              </div>
            ) : report ? (
              <div className="glass-panel p-10 md:p-14 rounded-2xl animate-fade-in-up">
                <div className="prose-custom">
                  <div dangerouslySetInnerHTML={{ __html: report.markdown ? report.markdown.replace(/\n/g, '<br/>') : '<div class="text-zinc-400 italic">Report is generating or empty.</div>' }} />
                </div>
                
                {report.pdf_path && (
                  <div className="mt-12 pt-6 border-t border-white/10 flex items-center justify-between bg-zinc-900/50 p-4 rounded-xl">
                    <div className="flex items-center gap-3 text-zinc-300">
                      <div className="p-2 bg-red-500/20 text-red-400 rounded-lg">
                        <FileText size={20} />
                      </div>
                      <span className="text-sm font-medium">Exported Document Available</span>
                    </div>
                    <a 
                      href={`file://${report.pdf_path}`} 
                      target="_blank" 
                      rel="noreferrer"
                      className="flex items-center gap-2 text-sm font-semibold bg-zinc-800 hover:bg-zinc-700 text-white px-4 py-2 rounded-lg transition-colors border border-white/10"
                    >
                      <Download size={16} /> Open PDF
                    </a>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-full space-y-6 animate-fade-in-up">
                <div className="relative">
                  <div className="absolute inset-0 border-4 border-blue-500/20 rounded-full animate-ping"></div>
                  <div className="relative bg-zinc-900 border border-blue-500/30 p-4 rounded-full shadow-[0_0_30px_rgba(59,130,246,0.3)]">
                    <Sparkles size={32} className="text-blue-400 animate-pulse" />
                  </div>
                </div>
                <div className="text-xl font-medium text-zinc-400 tracking-wide animate-pulse">
                  Synthesizing Research...
                </div>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
