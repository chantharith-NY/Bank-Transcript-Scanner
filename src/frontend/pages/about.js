import Head from 'next/head'
import Header from '../components/Header'
import Footer from '../components/Footer'

export default function About() {
  return (
    <div className="min-h-screen bg-[#F5F6FA] text-[#333333] font-roboto flex flex-col">
      <Head>
        <title>Bank Transaction Scanner</title>
        <link rel='icon' href="/ams-favicon.ico" className='rounded-2xl' />
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" />
      </Head>

      <Header />

      <main className="flex-grow bg-gradient-to-br max-w-5xl mx-auto pt-20 pb-10 px-4 sm:px-6 lg:px-8">
        <h1 className="text-2xl text-[#1C2526] font-bold mb-4 text-center">About us</h1>
        <p className="text-sm text-gray-600 mb-6">
          The Bank Transcript Scanner is a final exam project developed by students of the Department of Applied Mathematics and Statistics (AMS). This tool automates the extraction of financial data from scanned bank transactions for business auditing purposes.
        </p>

        <h2 className="text-2xl text-[#1C2526] font-semibold mb-10 text-center mt-20">Team Members</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6 mb-10">
          {[
            { name: "LEND Devid", role: "Frontend Developer", img: "devid.jpg", github: "https://github.com/KIRIKUUU", username: "KIRIKUUU" },
            { name: "LY Chungheang", role: "ML Engineer", img: "chungheang.jpg", github: "https://github.com/Chungheang0980", username: "Chungheang0980" },
            { name: "NANG Chettra", role: "ML Engineer", img: "chettra.png", github: "https://github.com/Chettraa", username: "NANG-Chettra" },
            { name: "NHEN Theary", role: "ML Engineer", img: "theary.jpg", github: "https://github.com/nhentheary", username: "nhentheary" },
            { name: "NGOUN Lyhorng", role: "ML Engineer", img: "lyhorng.png", github: "https://github.com/Ngounlyhorn11", username: "Ngounlyhorn11" },
            { name: "NY Chantharith", role: "Backend Developer", img: "chantharith.jpg", github: "https://github.com/chantharith-NY", username: "Chantharith Ny" },
          ].map(member => (
            <div key={member.name}>
              <img src={member.img} alt={member.name} className="rounded-full w-24 h-24 sm:w-28 sm:h-28 lg:w-32 lg:h-32 mx-auto object-cover" />
              <h3 className="text-lg text-[#1C2526] font-semibold mt-4 text-center">{member.name}</h3>
              <p className="text-sm text-gray-600 text-center">{member.role}</p>
              <p className="text-sm text-gray-800 text-center">
                <i className="fa-brands fa-github"></i> <a href={member.github} target="_blank" rel="noreferrer">{member.username}</a>
              </p>
            </div>
          ))}
        </div>
      </main>

      <Footer />
    </div>
  )
}
