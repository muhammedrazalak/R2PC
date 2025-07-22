import React, { useState } from 'react';

export default function App() {
  const [repoUrl, setRepoUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState(null);

  const handleGenerate = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess(false);
    setDownloadUrl(null);
    if (!repoUrl.startsWith('https://github.com/')) {
      setError('Please enter a valid public GitHub repository URL.');
      return;
    }
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/generate-postman', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ repoUrl }),
      });
      if (!response.ok) {
        const data = await response.json();
        setError(data.detail || 'Error generating collection.');
        setLoading(false);
        return;
      }
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      setDownloadUrl(url);
      setSuccess(true);
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-indigo-100 to-white px-4">
      <div className="w-full max-w-xl bg-white rounded-2xl shadow-xl p-8 mt-8">
        <h1 className="text-3xl font-bold text-indigo-700 mb-2 text-center">Express → Postman Collection Generator</h1>
        <p className="text-gray-500 mb-6 text-center">Paste a public GitHub Express.js repo URL below. The tool will analyze the code and generate a downloadable Postman collection, organized by controller.</p>
        <form onSubmit={handleGenerate} className="flex flex-col gap-4">
          <input
            type="url"
            className="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
            placeholder="https://github.com/your/repo"
            value={repoUrl}
            onChange={e => setRepoUrl(e.target.value)}
            required
            disabled={loading}
          />
          <button
            type="submit"
            className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 rounded-lg transition disabled:opacity-60"
            disabled={loading}
          >
            {loading ? (
              <span className="flex items-center justify-center"><svg className="animate-spin h-5 w-5 mr-2 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path></svg>Generating...</span>
            ) : (
              'Generate Collection'
            )}
          </button>
        </form>
        {error && <div className="mt-4 text-red-600 text-center">{error}</div>}
        {success && downloadUrl && (
          <div className="mt-6 flex flex-col items-center">
            <a
              href={downloadUrl}
              download="postman_collection.json"
              className="bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-6 rounded-lg transition mb-2"
            >
              Download Collection
            </a>
            <span className="text-green-700">Collection ready!</span>
          </div>
        )}
      </div>
      <footer className="mt-10 text-gray-400 text-sm text-center">
        Built with <span className="text-indigo-500">React</span> & <span className="text-blue-400">Tailwind CSS</span> · Powered by <span className="text-black font-semibold">Gemini Flash</span>
      </footer>
    </div>
  );
} 