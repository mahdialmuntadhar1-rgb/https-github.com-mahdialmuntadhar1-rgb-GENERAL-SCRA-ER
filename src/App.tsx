import React, { useState, useEffect } from 'react';
import { createClient } from '@supabase/supabase-js';
import { 
  LayoutDashboard, 
  Upload, 
  ClipboardCheck, 
  School, 
  Settings, 
  LogOut, 
  Search, 
  Filter, 
  CheckCircle2, 
  XCircle, 
  AlertCircle,
  Database,
  Globe,
  Phone,
  Mail,
  ChevronRight,
  MoreVertical,
  Download
} from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

import { GoogleGenAI } from "@google/genai";

// --- Utility ---
function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// --- Supabase Client ---
const supabaseUrl = (import.meta as any).env.VITE_SUPABASE_URL || '';
const supabaseAnonKey = (import.meta as any).env.VITE_SUPABASE_ANON_KEY || '';
const geminiApiKey = (import.meta as any).env.VITE_GEMINI_API_KEY || '';

// Only initialize if credentials exist to prevent "supabaseUrl is required" crash
const supabase = supabaseUrl && supabaseAnonKey 
  ? createClient(supabaseUrl, supabaseAnonKey) 
  : null;

const ai = geminiApiKey ? new GoogleGenAI({ apiKey: geminiApiKey }) : null;

// --- Components ---

const SidebarItem = ({ icon: Icon, label, active, onClick }: { icon: any, label: string, active: boolean, onClick: () => void }) => (
  <button
    onClick={onClick}
    className={cn(
      "w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group",
      active 
        ? "bg-blue-600 text-white shadow-lg shadow-blue-200" 
        : "text-slate-500 hover:bg-slate-100 hover:text-slate-900"
    )}
  >
    <Icon size={20} className={cn(active ? "text-white" : "text-slate-400 group-hover:text-slate-900")} />
    <span className="font-medium text-sm">{label}</span>
    {active && <motion.div layoutId="active-pill" className="ml-auto w-1.5 h-1.5 rounded-full bg-white" />}
  </button>
);

const StatCard = ({ label, value, icon: Icon, color }: { label: string, value: string | number, icon: any, color: string }) => (
  <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition-shadow">
    <div className="flex items-start justify-between">
      <div>
        <p className="text-slate-500 text-xs font-semibold uppercase tracking-wider mb-1">{label}</p>
        <h3 className="text-2xl font-bold text-slate-900">{value}</h3>
      </div>
      <div className={cn("p-3 rounded-xl", color)}>
        <Icon size={24} className="text-white" />
      </div>
    </div>
  </div>
);

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [universities, setUniversities] = useState<any[]>([]);
  const [staging, setStaging] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);
  const [isScraping, setIsScraping] = useState(false);
  const [scraperLogs, setScraperLogs] = useState<string[]>([]);
  const [scrapingInterval, setScrapingInterval] = useState<any>(null);
  const [isCleaning, setIsCleaning] = useState(false);

  // --- Data Fetching ---
  const fetchData = async () => {
    if (!supabase) {
      setLoading(false);
      return;
    }
    setLoading(true);
    try {
      const { data: univs } = await supabase.from('universities').select('*').order('name_ar');
      const { data: stage } = await supabase.from('staging_records').select('*').eq('status', 'pending');
      setUniversities(univs || []);
      setStaging(stage || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // --- Actions ---
  const approveRecord = async (record: any) => {
    if (!supabase) return;
    try {
      const raw = record.raw_data;
      const { error: insertError } = await supabase.from('universities').insert({
        name_ar: raw.name_ar || 'NOT VERIFIED',
        name_en: raw.name_en,
        type: raw.type || 'private',
        website_url: raw.website_url,
        is_verified: true
      });

      if (insertError) throw insertError;

      await supabase.from('staging_records').update({ status: 'approved' }).eq('id', record.id);
      setMessage({ type: 'success', text: 'Record approved and synced to production.' });
      fetchData();
    } catch (err: any) {
      setMessage({ type: 'error', text: err.message });
    }
  };

  const rejectRecord = async (recordId: string) => {
    if (!supabase) return;
    try {
      await supabase.from('staging_records').update({ status: 'rejected' }).eq('id', recordId);
      setMessage({ type: 'success', text: 'Record rejected.' });
      fetchData();
    } catch (err: any) {
      setMessage({ type: 'error', text: err.message });
    }
  };

  const startScraping = () => {
    if (!supabase) return;
    setIsScraping(true);
    setScraperLogs(["--- Starting Scraping Session ---"]);
    
    const sources = ["MoHE Website", "University News", "Education Portal"];
    let currentSourceIdx = 0;
    let recordsFound = 0;

    const interval = setInterval(async () => {
      if (currentSourceIdx >= sources.length) {
        clearInterval(interval);
        setIsScraping(false);
        setScraperLogs(prev => [...prev, `--- FINISHED: ${recordsFound} records added to staging ---`]);
        fetchData();
        return;
      }

      const source = sources[currentSourceIdx];
      setScraperLogs(prev => [...prev, `🔍 Scraping source: ${source}...`]);
      
      // Simulate finding a record
      const newRecord = {
        name_ar: `جامعة تجريبية ${Math.floor(Math.random() * 1000)}`,
        name_en: `Exp Univ ${Math.floor(Math.random() * 1000)}`,
        website_url: `https://univ-${Math.floor(Math.random() * 100)}.edu.iq`,
        type: 'private'
      };

      try {
        await supabase.from('staging_records').insert({
          raw_data: newRecord,
          source_file: `Web Scraper: ${source}`,
          status: 'pending'
        });
        recordsFound++;
        setScraperLogs(prev => [...prev, `✅ Found: ${newRecord.name_ar}`]);
      } catch (err) {
        console.error(err);
      }

      currentSourceIdx++;
    }, 2000);

    setScrapingInterval(interval);
  };

  const stopScraping = () => {
    if (scrapingInterval) {
      clearInterval(scrapingInterval);
      setScrapingInterval(null);
    }
    setIsScraping(false);
    setScraperLogs(prev => [...prev, "🛑 Scraping stopped by user."]);
    fetchData();
  };

  const aiCleanRecord = async (record: any) => {
    if (!ai) {
      setMessage({ type: 'error', text: 'Gemini API Key required for AI cleaning.' });
      return;
    }
    setIsCleaning(true);
    try {
      const prompt = `Clean and normalize this Iraq university data record. 
      Return ONLY valid JSON.
      Input: ${JSON.stringify(record.raw_data)}
      Rules:
      - Ensure name_ar is correct Arabic.
      - Ensure name_en is correct English.
      - Standardize type to one of: public, private, college, institute.
      - Fix website URL if broken.`;

      const response = await ai.models.generateContent({
        model: "gemini-2.0-flash",
        contents: [{ parts: [{ text: prompt }] }],
        config: { responseMimeType: "application/json" }
      });

      const cleanedData = JSON.parse(response.text || '{}');
      
      await supabase?.from('staging_records').update({ 
        raw_data: cleanedData,
        validation_errors: { ai_cleaned: true }
      }).eq('id', record.id);

      setMessage({ type: 'success', text: 'AI cleaning complete.' });
      fetchData();
    } catch (err: any) {
      setMessage({ type: 'error', text: `AI Error: ${err.message}` });
    } finally {
      setIsCleaning(false);
    }
  };

  // --- Render Helpers ---
  const renderContent = () => {
    if (!supabaseUrl || !supabaseAnonKey) {
      return (
        <div className="flex flex-col items-center justify-center h-[60vh] text-center p-8">
          <div className="bg-amber-50 p-6 rounded-2xl border border-amber-100 max-w-md">
            <AlertCircle className="mx-auto text-amber-500 mb-4" size={48} />
            <h2 className="text-xl font-bold text-amber-900 mb-2">Supabase Connection Required</h2>
            <p className="text-amber-700 text-sm mb-6">
              To use this live preview, please add your Supabase credentials to the <b>Secrets</b> panel in AI Studio.
            </p>
            <div className="space-y-2 text-left bg-white p-4 rounded-xl border border-amber-200 font-mono text-xs">
              <p>VITE_SUPABASE_URL=your_url</p>
              <p>VITE_SUPABASE_ANON_KEY=your_key</p>
            </div>
          </div>
        </div>
      );
    }

    if (loading) return <div className="flex items-center justify-center h-64"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div></div>;

    switch (activeTab) {
      case 'dashboard':
        return (
          <div className="space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <StatCard label="Approved Univs" value={universities.length} icon={School} color="bg-blue-600" />
              <StatCard label="Pending Review" value={staging.length} icon={ClipboardCheck} color="bg-amber-500" />
              <StatCard label="Import Batches" value="12" icon={Upload} color="bg-indigo-600" />
              <StatCard label="System Health" value="100%" icon={Database} color="bg-emerald-600" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
                <h3 className="text-lg font-bold text-slate-900 mb-4">Recent Approvals</h3>
                <div className="space-y-4">
                  {universities.slice(0, 5).map((u) => (
                    <div key={u.id} className="flex items-center justify-between p-3 rounded-xl hover:bg-slate-50 transition-colors">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-lg bg-blue-50 flex items-center justify-center text-blue-600 font-bold">
                          {u.name_ar[0]}
                        </div>
                        <div>
                          <p className="font-semibold text-slate-900 text-sm">{u.name_ar}</p>
                          <p className="text-slate-500 text-xs">{u.type}</p>
                        </div>
                      </div>
                      <CheckCircle2 size={18} className="text-emerald-500" />
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
                <h3 className="text-lg font-bold text-slate-900 mb-4">Quick Actions</h3>
                <div className="grid grid-cols-2 gap-4">
                  <button className="p-4 rounded-xl border border-slate-100 hover:bg-slate-50 text-left transition-all">
                    <Upload className="text-blue-600 mb-2" size={20} />
                    <p className="font-bold text-slate-900 text-sm">Bulk Import</p>
                    <p className="text-slate-500 text-xs">CSV, Excel, JSON</p>
                  </button>
                  <button className="p-4 rounded-xl border border-slate-100 hover:bg-slate-50 text-left transition-all">
                    <Download className="text-indigo-600 mb-2" size={20} />
                    <p className="font-bold text-slate-900 text-sm">Export Clean</p>
                    <p className="text-slate-500 text-xs">Production Ready</p>
                  </button>
                </div>
              </div>
            </div>
          </div>
        );

      case 'review':
        return (
          <div className="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
            <div className="p-6 border-b border-slate-100 flex items-center justify-between">
              <div>
                <h3 className="text-xl font-bold text-slate-900">Review Queue</h3>
                <p className="text-slate-500 text-sm">Validate and approve raw data imports</p>
              </div>
              <div className="flex gap-2">
                <button className="px-4 py-2 bg-slate-100 text-slate-700 rounded-lg text-sm font-semibold hover:bg-slate-200 transition-colors">
                  Reject All
                </button>
              </div>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead className="bg-slate-50 border-b border-slate-100">
                  <tr>
                    <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Entity Name</th>
                    <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Source</th>
                    <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Validation</th>
                    <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {staging.length === 0 ? (
                    <tr><td colSpan={4} className="px-6 py-12 text-center text-slate-500 italic">No records pending review</td></tr>
                  ) : staging.map((record) => (
                    <tr key={record.id} className="hover:bg-slate-50 transition-colors group">
                      <td className="px-6 py-4">
                        <p className="font-bold text-slate-900">{record.raw_data.name_ar || record.raw_data.name_en || 'Unnamed'}</p>
                        <p className="text-slate-500 text-xs">{record.raw_data.type || 'Unknown Type'}</p>
                      </td>
                      <td className="px-6 py-4">
                        <span className="px-2 py-1 bg-slate-100 text-slate-600 rounded text-[10px] font-bold uppercase">
                          {record.source_file}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-1 text-emerald-600 text-xs font-semibold">
                          <CheckCircle2 size={14} />
                          <span>Ready</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-right">
                        <div className="flex items-center justify-end gap-2">
                          <button 
                            onClick={() => aiCleanRecord(record)}
                            disabled={isCleaning || !ai}
                            title="AI Clean"
                            className="p-2 text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors disabled:opacity-50"
                          >
                            <Globe size={20} className={isCleaning ? "animate-spin" : ""} />
                          </button>
                          <button 
                            onClick={() => approveRecord(record)}
                            className="p-2 text-emerald-600 hover:bg-emerald-50 rounded-lg transition-colors"
                          >
                            <CheckCircle2 size={20} />
                          </button>
                          <button 
                            onClick={() => rejectRecord(record.id)}
                            className="p-2 text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                          >
                            <XCircle size={20} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        );

      case 'universities':
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div className="relative w-96">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                <input 
                  type="text" 
                  placeholder="Search universities..." 
                  className="w-full pl-10 pr-4 py-2 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                />
              </div>
              <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-xl font-bold text-sm hover:bg-blue-700 transition-all shadow-lg shadow-blue-100">
                <School size={18} />
                Add University
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
              {universities.map((u) => (
                <div key={u.id} className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition-all group">
                  <div className="flex items-start justify-between mb-4">
                    <div className="w-12 h-12 rounded-xl bg-slate-50 flex items-center justify-center text-slate-400 group-hover:bg-blue-50 group-hover:text-blue-600 transition-colors">
                      <School size={24} />
                    </div>
                    <div className="flex gap-1">
                      <button className="p-2 text-slate-400 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition-all">
                        <MoreVertical size={18} />
                      </button>
                    </div>
                  </div>
                  <h4 className="text-lg font-bold text-slate-900 mb-1">{u.name_ar}</h4>
                  <p className="text-slate-500 text-sm mb-4">{u.name_en || 'No English Name'}</p>
                  
                  <div className="space-y-2 pt-4 border-t border-slate-50">
                    <div className="flex items-center gap-2 text-slate-600 text-xs">
                      <Globe size={14} className="text-slate-400" />
                      <span className="truncate">{u.website_url || 'No Website'}</span>
                    </div>
                    <div className="flex items-center gap-2 text-slate-600 text-xs">
                      <Database size={14} className="text-slate-400" />
                      <span className="capitalize">{u.type}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        );

      case 'scraper':
        return (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm flex items-center justify-between">
              <div>
                <h3 className="text-lg font-bold text-slate-900">Scraper Control Panel</h3>
                <p className="text-slate-500 text-sm">Automated data collection from web sources</p>
              </div>
              <div className="flex gap-3">
                {!isScraping ? (
                  <button 
                    onClick={startScraping}
                    className="flex items-center gap-2 px-6 py-3 bg-emerald-600 text-white rounded-xl font-bold hover:bg-emerald-700 transition-all shadow-lg shadow-emerald-100"
                  >
                    <CheckCircle2 size={18} />
                    Start Scraping
                  </button>
                ) : (
                  <button 
                    onClick={stopScraping}
                    className="flex items-center gap-2 px-6 py-3 bg-rose-600 text-white rounded-xl font-bold hover:bg-rose-700 transition-all shadow-lg shadow-rose-100"
                  >
                    <XCircle size={18} />
                    Stop Scraping
                  </button>
                )}
              </div>
            </div>

            <div className="bg-slate-900 rounded-2xl p-6 font-mono text-sm text-emerald-400 min-h-[400px] shadow-2xl overflow-y-auto max-h-[600px]">
              {scraperLogs.length === 0 ? (
                <p className="text-slate-500 italic">Ready to start scraping session...</p>
              ) : (
                scraperLogs.map((log, i) => (
                  <div key={i} className="mb-1">
                    <span className="text-slate-500 mr-2">[{new Date().toLocaleTimeString()}]</span>
                    {log}
                  </div>
                ))
              )}
              {isScraping && <div className="animate-pulse inline-block w-2 h-4 bg-emerald-400 ml-1"></div>}
            </div>
          </div>
        );

      default:
        return <div className="p-12 text-center text-slate-500">Feature coming soon...</div>;
    }
  };

  return (
    <div className="flex h-screen bg-[#F8FAFC] font-sans text-slate-900">
      {/* Sidebar */}
      <aside className="w-72 bg-white border-r border-slate-100 flex flex-col p-6">
        <div className="flex items-center gap-3 px-2 mb-10">
          <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center text-white shadow-lg shadow-blue-200">
            <Database size={24} />
          </div>
          <div>
            <h1 className="font-black text-lg tracking-tight">IraqEdu</h1>
            <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest leading-none">Admin Control</p>
          </div>
        </div>

        <nav className="flex-1 space-y-2">
          <SidebarItem icon={LayoutDashboard} label="Dashboard" active={activeTab === 'dashboard'} onClick={() => setActiveTab('dashboard')} />
          <SidebarItem icon={Upload} label="Import Center" active={activeTab === 'import'} onClick={() => setActiveTab('import')} />
          <SidebarItem icon={Globe} label="Scraper Center" active={activeTab === 'scraper'} onClick={() => setActiveTab('scraper')} />
          <SidebarItem icon={ClipboardCheck} label="Review Queue" active={activeTab === 'review'} onClick={() => setActiveTab('review')} />
          <SidebarItem icon={School} label="Universities" active={activeTab === 'universities'} onClick={() => setActiveTab('universities')} />
          <div className="pt-4 pb-2 px-4">
            <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">System</p>
          </div>
          <SidebarItem icon={Settings} label="Settings" active={activeTab === 'settings'} onClick={() => setActiveTab('settings')} />
        </nav>

        <div className="mt-auto pt-6 border-t border-slate-50">
          <button className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-slate-500 hover:bg-rose-50 hover:text-rose-600 transition-all group">
            <LogOut size={20} className="text-slate-400 group-hover:text-rose-600" />
            <span className="font-medium text-sm">Sign Out</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="h-20 bg-white/80 backdrop-blur-md border-b border-slate-100 px-8 flex items-center justify-between z-10">
          <h2 className="text-xl font-bold text-slate-900 capitalize">{activeTab}</h2>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-3 px-4 py-2 bg-slate-50 rounded-xl border border-slate-100">
              <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold text-xs">
                MA
              </div>
              <div className="text-left">
                <p className="text-xs font-bold text-slate-900 leading-none">Mahdi A.</p>
                <p className="text-[10px] text-slate-500 font-medium">Administrator</p>
              </div>
            </div>
          </div>
        </header>

        {/* Content Area */}
        <div className="flex-1 overflow-y-auto p-8">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
            >
              {renderContent()}
            </motion.div>
          </AnimatePresence>
        </div>

        {/* Toast Messages */}
        <AnimatePresence>
          {message && (
            <motion.div
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 50 }}
              className={cn(
                "fixed bottom-8 right-8 px-6 py-4 rounded-2xl shadow-2xl flex items-center gap-3 z-50",
                message.type === 'success' ? "bg-emerald-600 text-white" : "bg-rose-600 text-white"
              )}
            >
              {message.type === 'success' ? <CheckCircle2 size={20} /> : <AlertCircle size={20} />}
              <span className="font-bold text-sm">{message.text}</span>
              <button onClick={() => setMessage(null)} className="ml-4 opacity-70 hover:opacity-100">
                <XCircle size={18} />
              </button>
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}
