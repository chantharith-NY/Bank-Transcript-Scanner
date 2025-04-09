import Head from 'next/head';
import Header from '../components/Header';
import Footer from '../components/Footer';

export default function Home() {
  return (
    <div className="min-h-screen bg-[#F5F6FA] text-[#333333] font-roboto flex flex-col">
      <Head>
        <title>Bank Transaction Scanner</title>
        <link rel="icon" href="/ams-favicon.ico" className="rounded-2xl" />
      </Head>

      <Header />

      <main className="flex-grow bg-gradient-to-br from-yellow-100 to-orange-200 flex items-center justify-center p-4">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-800 mb-4">🚧 Under Construction</h1>
          <p className="text-lg text-gray-700 max-w-lg mx-auto">
            We're currently working hard on our bank transaction scanner. Please check back soon!
          </p>
          <footer className="mt-10 text-sm text-gray-500">
            &copy; {new Date().getFullYear()} Bank Transaction Scanner
          </footer>
        </div>
      </main>

      <Footer />
    </div>
  );
}

