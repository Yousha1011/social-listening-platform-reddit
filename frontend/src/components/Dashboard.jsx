import React, { useState } from 'react';

const Dashboard = () => {
    const [keywords, setKeywords] = useState('');
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState(null);
    const [error, setError] = useState(null);

    const handleAnalyze = async () => {
        setLoading(true);
        setError(null);
        try {
            // Use environment variable for production, fallback to localhost for dev
            const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
            const response = await fetch(`${API_URL}/api/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    keywords: keywords.split(',').map(k => k.trim()),
                    limit: 10000 // Attempt to fetch as many as possible
                }),
            });

            if (!response.ok) {
                throw new Error('Analysis failed');
            }

            const result = await response.json();
            setData(result);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-6 max-w-7xl mx-auto">
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-gray-900 mb-4">Measles Vaccine Hesitancy Dashboard</h1>
                <div className="flex gap-4">
                    <input
                        type="text"
                        placeholder="Enter keywords (e.g., measles)"
                        className="flex-1 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
                        value={keywords}
                        onChange={(e) => setKeywords(e.target.value)}
                    />
                    <button
                        onClick={handleAnalyze}
                        disabled={loading || !keywords}
                        className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
                    >
                        {loading ? 'Analyzing...' : 'Start Analysis'}
                    </button>
                </div>
                {error && <p className="mt-2 text-red-600">{error}</p>}
            </div>

            {data && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="bg-white p-6 rounded-lg shadow">
                        <h2 className="text-xl font-semibold mb-4">Overview</h2>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="p-4 bg-blue-50 rounded-md">
                                <p className="text-sm text-gray-500">Total Analyzed</p>
                                <p className="text-2xl font-bold text-blue-600">{data.total_analyzed}</p>
                            </div>
                            <div className="p-4 bg-red-50 rounded-md">
                                <p className="text-sm text-gray-500">Hesitancy Rate</p>
                                <p className="text-2xl font-bold text-red-600">{(data.hesitancy_rate * 100).toFixed(1)}%</p>
                            </div>
                            <div className="p-4 bg-yellow-50 rounded-md">
                                <p className="text-sm text-gray-500">Exemption Rate</p>
                                <p className="text-2xl font-bold text-yellow-600">{(data.exemption_rate * 100).toFixed(1)}%</p>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white p-6 rounded-lg shadow">
                        <h2 className="text-xl font-semibold mb-4">Exemption Reasons</h2>
                        <div className="space-y-2">
                            {Object.entries(data.reasons_distribution).map(([reason, count]) => (
                                <div key={reason} className="flex justify-between items-center border-b pb-2">
                                    <span className="text-gray-700">{reason}</span>
                                    <span className="font-medium bg-gray-100 px-2 py-1 rounded">{count}</span>
                                </div>
                            ))}
                            {Object.keys(data.reasons_distribution).length === 0 && (
                                <p className="text-gray-500 italic">No exemption reasons identified yet.</p>
                            )}
                        </div>
                    </div>

                    <div className="col-span-1 md:col-span-2 bg-white p-6 rounded-lg shadow">
                        <h2 className="text-xl font-semibold mb-4">Recent Results</h2>
                        <div className="overflow-x-auto">
                            <table className="min-w-full divide-y divide-gray-200">
                                <thead className="bg-gray-50">
                                    <tr>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Author</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Content</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Hesitancy</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Exemption</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Reason</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Sentiment</th>
                                    </tr>
                                </thead>
                                <tbody className="bg-white divide-y divide-gray-200">
                                    {data.recent_results.map((result) => (
                                        <tr key={result.post_id}>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                {new Date(result.post.created_utc * 1000).toLocaleDateString()}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                {result.post.author}
                                            </td>
                                            <td className="px-6 py-4 text-sm text-gray-500 max-w-xs truncate">
                                                <a href={result.post.url} target="_blank" rel="noopener noreferrer" className="text-indigo-600 hover:text-indigo-900 block font-medium mb-1">
                                                    {result.post.title}
                                                </a>
                                                <span title={result.post.content}>{result.post.content.substring(0, 100)}...</span>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${result.hesitancy ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}`}>
                                                    {result.hesitancy ? 'Yes' : 'No'}
                                                </span>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${result.philosophical_exemption ? 'bg-yellow-100 text-yellow-800' : 'bg-gray-100 text-gray-800'}`}>
                                                    {result.philosophical_exemption ? 'Yes' : 'No'}
                                                </span>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{result.exemption_reason || '-'}</td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 capitalize">{result.sentiment}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Dashboard;
