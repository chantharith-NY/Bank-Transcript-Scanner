import Head from 'next/head';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { useState, useEffect } from 'react';
import Link from 'next/link';

const HistoryPage = () => {
  const [history, setHistory] = useState([]);
  const [downloadOptionsVisible, setDownloadOptionsVisible] = useState(null);
  const [selectedDownloadId, setSelectedDownloadId] = useState(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/history'); // Adjust URL if needed
      if (response.ok) {
        const data = await response.json();
        setHistory(data);
      } else {
        console.error('Failed to fetch history:', response.status);
      }
    } catch (error) {
      console.error('Error fetching history:', error);
    }
  };

  const handleView = (uploadId) => {
    // Redirect to a results detail page (you might need to create this)
    window.location.href = `/results-detail/${uploadId}`;
  };

  const handleDownloadClick = (uploadId) => {
    setSelectedDownloadId(uploadId);
    setDownloadOptionsVisible(uploadId);
  };

  const handleDownload = async (format) => {
    if (selectedDownloadId) {
      const url = format === 'excel' ? `/download/excel/${selectedDownloadId}` : `/download/csv/${selectedDownloadId}`;
      window.location.href = url; // Trigger download
      setDownloadOptionsVisible(null);
      setSelectedDownloadId(null);
    }
  };

  return (
    <div className="min-h-screen bg-[#F5F6FA] text-[#333333] font-roboto flex flex-col">
      <Head>
        <title>Transaction History</title>
        <link rel='icon' href="/ams-favicon.ico" className='rounded-2xl' />
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" />
      </Head>

      <Header />

      <main className="flex-grow bg-gradient-to-br max-w-8xl mx-auto pt-20 pb-6 px-4 sm:px-6 lg:px-8">
        <h1 className="text-2xl font-semibold text-[#1C2526] mb-6">Transaction History</h1>

        {history.length > 0 ? (
          <div className="overflow-x-auto bg-white shadow-md rounded-lg">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider sm:px-6">Transaction ID</th>
                  <th scope="col" className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider sm:px-6">Date & Time</th>
                  <th scope="col" className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider sm:px-6">Total Amount</th>
                  <th scope="col" className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider sm:px-6">Total Files</th>
                  <th scope="col" className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider sm:px-6">Missing Info</th>
                  <th scope="col" className="px-3 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider sm:px-6">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {history.map((item) => (
                  <tr key={item.upload_id}>
                    <td className="px-3 py-4 whitespace-nowrap text-sm text-gray-500 sm:px-6">{item.upload_id}</td>
                    <td className="px-3 py-4 whitespace-nowrap text-sm text-gray-500 sm:px-6">{new Date(item.upload_date).toLocaleString()}</td>
                    <td className="px-3 py-4 whitespace-nowrap text-sm text-gray-500 sm:px-6">${item.total_amount ? item.total_amount.toFixed(2) : 'N/A'}</td>
                    <td className="px-3 py-4 whitespace-nowrap text-sm text-gray-500 sm:px-6">{item.total_files}</td>
                    <td className="px-3 py-4 whitespace-nowrap text-sm text-gray-500 sm:px-6">{item.validation_errors_count || 0}</td>
                    <td className="px-3 py-4 whitespace-nowrap text-right text-sm font-medium sm:px-6">
                      <button onClick={() => handleView(item.upload_id)} className="text-blue-600 hover:text-blue-800 mr-2">
                        View
                      </button>
                      <div className="relative inline-block text-left">
                        <button
                          onClick={() => handleDownloadClick(item.upload_id)}
                          className="text-green-600 hover:text-green-800 focus:outline-none"
                        >
                          Download
                        </button>
                        {downloadOptionsVisible === item.upload_id && (
                          <div className="origin-top-right absolute right-0 mt-2 w-32 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-50">
                            <div className="py-1" role="menu" aria-orientation="vertical" aria-labelledby="options-menu-button">
                              <button onClick={() => handleDownload('excel')} className="block w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" role="menuitem">
                                Excel
                              </button>
                              <button onClick={() => handleDownload('csv')} className="block w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" role="menuitem">
                                CSV
                              </button>
                            </div>
                          </div>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p>No transaction history available.</p>
        )}
      </main>

      <Footer />
    </div>
  );
};

export default HistoryPage;