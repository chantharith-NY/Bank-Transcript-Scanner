export default function Footer() {
  return (
    <footer className="bg-white border-t border-gray-200 text-[#1C2526] text-sm py-4 px-2">
      <div className="text-center">
        <p className="mb-2">
          Developed by <span className="font-semibold">AMS 3rd Gen</span>
        </p>

        <div className="flex flex-col sm:flex-row justify-center items-center gap-2 sm:gap-4 text-sm">
          <a
            href="https://itc.edu.kh/home-ams/"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-[#354ac5] transition-colors"
          >
            <i className="fa-solid fa-building-columns mr-1"></i>
            Department of Applied Mathematics and Statistics
          </a>

          <span className="hidden sm:inline">|</span>

          <a
            href="https://github.com/chantharith-NY/Bank-Transcript-Scanner"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-[#354ac5] transition-colors"
          >
            <i className="fa-brands fa-github mr-1"></i>
            GitHub
          </a>

          <span className="hidden sm:inline">|</span>

          <a
            href="/license"
            className="hover:text-[#354ac5] transition-colors"
          >
            <i className="fa-solid fa-scale-balanced mr-1"></i>
            MIT License
          </a>
        </div>

        <p className="mt-4 text-gray-400 text-xs">
          &copy; {new Date().getFullYear()} AMS. All rights reserved.
        </p>
      </div>
    </footer>
  )
}
