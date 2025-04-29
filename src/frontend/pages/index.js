import Head from 'next/head';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { useState, useRef } from 'react';
import { useRouter } from 'next/router';

export default function Home() {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState('');
  const router = useRouter();
  const fileInputRef = useRef(null);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [uploadStatus, setUploadStatus] = useState('idle');
  const [results, setResults] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');

  const handleFileChange = (event) => {
    const newFiles = Array.from(event.target.files);
    setFiles(newFiles);
    setSelectedFiles(newFiles);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const newFiles = Array.from(event.dataTransfer.files);
    setFiles(newFiles);
    setSelectedFiles(newFiles);
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleBrowseClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleUpload = async () => {
    if (files.length === 0) {
      setUploadMessage('Please select files to upload.');
      return;
    }

    setUploadStatus('loading');
    setUploadMessage('Uploading files...');
    setErrorMessage('');
    setResults(null);

    const formData = new FormData();
    files.forEach((file) => {
      formData.append('files', file);
    });

    try {
      const response = await fetch('http://127.0.0.1:8000/upload', { // Adjust URL if needed
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setUploadStatus('success');
        setUploadMessage(data.message);
        // Fetch results immediately after successful upload
        fetchResults(data.upload_id);
      } else {
        const errorData = await response.json();
        setUploadStatus('error');
        setErrorMessage(`Upload failed: ${errorData.detail || response.statusText}`);
      }
    } catch (error) {
      setUploadStatus('error');
      setErrorMessage(`Upload failed: ${error.message}`);
    } finally {
      setUploading(false); // Ensure uploading state is reset
    }
  };

  const fetchResults = async (uploadId) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/results/${uploadId}`); // Adjust URL
      if (response.ok) {
        const data = await response.json();
        setResults(data);
      } else {
        console.error('Failed to fetch results:', response.status);
        setErrorMessage('Failed to fetch processing results.');
        setUploadStatus('error');
      }
    } catch (error) {
      console.error('Error fetching results:', error);
      setErrorMessage('Error fetching processing results.');
      setUploadStatus('error');
    }
  };

  return (
    <div className="min-h-screen bg-[#F5F6FA] text-[#333333] font-roboto flex flex-col">
      <Head>
        <title>Bank Transaction Scanner</title>
        <link rel='icon' href="/ams-favicon.ico" className='rounded-2xl' />
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" />
      </Head>

      <Header />

      <main className="flex-grow bg-gradient-to-br max-w-5xl mx-auto pt-20 pb-10 px-4 sm:px-6 lg:px-8">
        <h1 className="text-2xl text-[#1C2526] font-bold mb-4 text-center">Welcome to our Bank Transaction Scanner</h1>
        <p className="text-lg text-gray-600 mb-4">
          Easily scan and extract key information from your bank statements in just a few clicks.
        </p>
        <ul className="text-left mx-auto space-y-2 mb-6 max-w-lg text-gray-600">
          <li className="flex text-left">
            <span className="text-blue-600 mr-2">📄</span> Upload PDF or image files of bank transactions
          </li>
          <li className="flex text-left">
            <span className="text-blue-600 mr-2">🧠</span> Automatically detect the bank and extract details like amount, date, and transaction ID
          </li>
          <li className="flex text-left">
            <span className="text-blue-600 mr-2">🔎</span> Identify missing information
          </li>
          <li className="flex text-left">
            <span className="text-blue-600 mr-2">📊</span> Export results to Excel, CSV, or PDF
          </li>
        </ul>
        <p className="text-lg text-gray-600 mb-6">
          Start by uploading your statement above and let the scanner do the work for you!
        </p>

        {/* File Upload Section */}
        <div className="text-center mb-8">
          <h3 className="text-xl font-semibold text-[#1C2526]">📤 Upload Your Bank Statements</h3>
          <div
            className="mt-4 border-2 border-dashed border-gray-300 p-12 rounded-lg mb-4 cursor-pointer"
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onClick={handleBrowseClick}
          >
            {selectedFiles.length > 0 ? (
              <ul>
                {selectedFiles.map((file) => (
                  <li key={file.name} className="text-gray-500">{file.name}</li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500">Drag & Drop files here or click to browse</p>
            )}
          </div>
          <input
            type="file"
            multiple
            onChange={handleFileChange}
            ref={fileInputRef}
            className="hidden"
          />
          <p className="text-sm text-gray-500">OR</p>
          <button
            onClick={handleBrowseClick}
            className="mt-4 py-2 px-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Browse Files
          </button>
          <br></br>
          <button
            onClick={handleUpload}
            className="mt-6 py-2 px-6 bg-green-600 text-white rounded-lg hover:bg-green-700"
            disabled={selectedFiles.length === 0 || uploadStatus === 'loading'}
          >
            {uploadStatus === 'loading' ? 'Uploading...' : 'Upload'}
          </button>

          {uploadStatus === 'error' && (
            <p className="mt-4 text-red-500">{errorMessage}</p>
          )}
        </div>

        {/* Display Results */}
        {results && results.extracted_transactions && results.extracted_transactions.length > 0 && (
          <div className="mt-8 p-6 bg-white shadow-md rounded-lg">
            <h2 className="text-xl font-semibold text-[#1C2526] mb-4">Extraction Results:</h2>

            {results.summary?.total_amount !== undefined && (
              <p className="mb-2">
                <span className="font-bold">Total Amount:</span> ${results.summary.total_amount.toFixed(2)}
              </p>
            )}

            {results.validation_errors && results.validation_errors.length > 0 && (
              <div className="mb-4">
                <h3 className="text-lg font-semibold text-red-600 mb-2">Missing Information:</h3>
                <ul>
                  {results.validation_errors.map((error, index) => (
                    <li key={index} className="text-red-500 mb-1">
                      Transaction: {JSON.stringify(error.transaction_data)}, Missing Fields: {error.missing_fields.join(', ')}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <h3 className="text-lg font-semibold text-[#1C2526] mb-2">Extracted Transactions:</h3>
            <ul>
              {results.extracted_transactions.map((transaction, index) => (
                <li key={index} className="mb-2">
                  Date: {transaction.date || 'N/A'}, Description: {transaction.description || 'N/A'}, Amount: ${transaction.amount !== null ? transaction.amount.toFixed(2) : 'N/A'}
                </li>
              ))}
            </ul>
          </div>
        )}


        {uploadStatus === 'success' && !results && (
          <p className="mt-4 text-green-500">Upload successful. Fetching results...</p>
        )}
      </main>

      <Footer />
    </div>
  );
}