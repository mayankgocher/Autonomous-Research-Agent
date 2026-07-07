import React from 'react'

export default function Dashboard() {
  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar Placeholder */}
      <div className="w-64 glass-panel border-r border-slate-700 hidden md:flex flex-col">
        <div className="p-6">
          <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent">
            ResearchAgent
          </h1>
        </div>
        <div className="flex-1 overflow-y-auto p-4 space-y-2">
          {/* History items will go here */}
          <div className="text-slate-400 text-sm p-2">No previous research found.</div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col relative overflow-hidden">
        {/* Header / Search Area */}
        <header className="p-6 md:p-10 glass-panel border-b border-slate-700 z-10 flex flex-col items-center justify-center">
          <h2 className="text-2xl md:text-4xl font-extrabold mb-6 text-center">
            What would you like to research?
          </h2>
          <div className="w-full max-w-3xl relative">
            <input 
              type="text" 
              className="w-full bg-slate-800/50 border border-slate-600 rounded-full py-4 px-6 pr-14 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-lg shadow-inner transition-all hover:bg-slate-800/80"
              placeholder="e.g. Research the best multimodal embedding models..."
            />
            <button className="absolute right-2 top-2 p-2 bg-blue-600 hover:bg-blue-500 rounded-full text-white transition-colors flex items-center justify-center w-10 h-10">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m21 21-6-6m2-5a7 7 0 1 1-14 0 7 7 0 0 1 14 0z"/></svg>
            </button>
          </div>
        </header>

        {/* Dashboard Body / Results Area */}
        <main className="flex-1 overflow-y-auto p-6 md:p-10 bg-slate-900/50 relative">
          <div className="max-w-5xl mx-auto flex flex-col items-center justify-center h-full text-center space-y-4 text-slate-500">
            <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" className="text-slate-600 mb-4 opacity-50"><path d="m21 16-4 4-4-4"/><path d="M17 20V4"/><path d="m3 8 4-4 4 4"/><path d="M7 4v16"/></svg>
            <p className="text-lg">Your research results and workflow progress will appear here.</p>
            <p className="text-sm">Powered by LangGraph and Ollama</p>
          </div>
        </main>
      </div>
    </div>
  )
}
