'use client'
import Link from 'next/link'
import Image from 'next/image'
import { useState } from 'react'

export default function Header() {
  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <header className="fixed top-0 w-full bg-white shadow-md flex justify-between items-center py-2 px-4 z-10">
      {/* Logo */}
      <Link href="/" className="flex items-center gap-2">
        <div className="relative w-10 h-10">
          <Image
            src="/ams-logo.jpg"
            alt="AMS Logo"
            fill
            className="object-contain rounded-md"
          />
        </div>
      </Link>

      {/* Desktop Navigation */}
      <nav className="hidden md:flex gap-6 items-center">
        <Link href="/" className="text-[#1C2526] hover:text-[#C0392B]">Home</Link>
        <Link href="/history" className="text-[#1C2526] hover:text-[#C0392B]">History</Link>
        <Link href="/about" className="text-[#1C2526] hover:text-[#C0392B]">About</Link>
      </nav>

      {/* Hamburger Icon */}
      <button
        className="md:hidden text-2xl text-[#1C2526]"
        onClick={() => setMenuOpen(!menuOpen)}
        aria-label="Toggle Menu"
      >
        <i className={`fa-solid ${menuOpen ? 'fa-xmark' : 'fa-bars'}`}></i>
      </button>

      {/* Mobile Dropdown */}
      {menuOpen && (
        <div className="absolute top-full left-0 w-full bg-white shadow-md md:hidden">
          <nav className="flex flex-col gap-4 p-4">
            <Link href="/" onClick={() => setMenuOpen(false)} className="text-[#1C2526] hover:text-[#C0392B]">Home</Link>
            <Link href="/history" onClick={() => setMenuOpen(false)} className="text-[#1C2526] hover:text-[#C0392B]">History</Link>
            <Link href="/about" onClick={() => setMenuOpen(false)} className="text-[#1C2526] hover:text-[#C0392B]">About</Link>
          </nav>
        </div>
      )}
    </header>
  )
}
