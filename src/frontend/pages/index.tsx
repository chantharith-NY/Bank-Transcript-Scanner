import Head from 'next/head';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { useState, useRef } from 'react';

export default function Home() {
  const [files, setFiles] = useState<File[]>([]);
  const [uploading, setUploading] = useState<boolean>(false);
  const [uploadMessage, setUploadMessage] = useState<string>('');
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [results, setResults] = useState<{ prediction: string[] } | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>('');

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newFiles = Array.from(event.target.files || []);
    setFiles(newFiles);
    setSelectedFiles(newFiles);
    setUploadStatus('idle'); // Reset status on new file selection
    setErrorMessage('');
    setResults(null);
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    const newFiles = Array.from(event.dataTransfer.files);
    setFiles(newFiles);
    setSelectedFiles(newFiles);
    setUploadStatus('idle');
    setErrorMessage('');
    setResults(null);
  };

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
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
      setUploadStatus('error');
      return;
    }

    setUploadStatus('loading');
    setUploadMessage('Classifying files...');
    setErrorMessage('');
    setResults(null);
    setUploading(true);

    try {
      // Create FormData to send files
      const formData = new FormData();
      files.forEach((file) => {
        formData.append('files', file);
      });

      // Send to classify endpoint
      const response = await fetch('http://localhost:5000/classify', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setUploadStatus('success');
        setUploadMessage('Classification successful!');
        setResults(data);
      } else {
        const errorData = await response.json();
        setUploadStatus('error');
        setErrorMessage(`Classification failed: ${errorData.detail || response.statusText}`);
      }
    } catch (error) {
      setUploadStatus('error');
      setErrorMessage(`Classification failed: ${(error as Error).message}`);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#F5F6FA] text-[#333333] font-roboto flex flex-col">
      <Head>
        <title>Bank Transaction Scanner</title>
        <link rel="icon" href="/ams-favicon.ico" className="rounded-2xl" />
        <link
          rel="stylesheet"
          href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"
        />
      </Head>

      <Header />

      <main className="flex-grow bg-gradient-to-br max-w-5xl mx-auto pt-20 pb-10 px-4 sm:px-6 lg:px-8">
        <h1 className="text-2xl text-[#1C2526] font-bold mb-4 text-center">
          Welcome to our Bank Transaction Scanner
        </h1>
        <p className="text-lg text-gray-600 mb-4">
          Easily classify bank statements from your uploaded images.
        </p>
        <ul className="text-left mx-auto space-y-2 mb-6 max-w-lg text-gray-600">
          <li className="flex text-left">
            <span className="text-blue-600 mr-2">📄</span> Upload image files of bank transactions
          </li>
          <li className="flex text-left">
            <span className="text-blue-600 mr-2">🧠</span> Automatically classify the bank
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
                  <li key={file.name} className="text-gray-500">
                    {file.name}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500">Drag & Drop files here or click to browse</p>
            )}
          </div>
          <input
            type="file"
            multiple
            accept="image/*"
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
          <br />
          <button
            onClick={handleUpload}
            className="mt-6 py-2 px-6 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400"
            disabled={selectedFiles.length === 0 || uploadStatus === 'loading'}
          >
            {uploadStatus === 'loading' ? 'Classifying...' : 'Classify'}
          </button>

          {uploadStatus === 'error' && <p className="mt-4 text-red-500">{errorMessage}</p>}
          {uploadMessage && uploadStatus !== 'error' && (
            <p className="mt-4 text-gray-600">{uploadMessage}</p>
          )}
        </div>

        {/* Display Results */}
        {results && results.prediction && (
          <div className="mt-8 p-6 bg-white shadow-md rounded-lg">
            <h2 className="text-xl font-semibold text-[#1C2526] mb-4">Classification Results:</h2>
            <ul>
              {results.prediction.map((pred, index) => (
                <li key={index} className="mb-2">
                  File {selectedFiles[index]?.name || index + 1}: Classified as{' '}
                  <strong>{pred}</strong>
                </li>
              ))}
            </ul>
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
}