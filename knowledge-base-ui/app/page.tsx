import Link from 'next/link';
import { BookOpen, FileText, Layers } from 'lucide-react';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />

      <main className="flex-1">
        <div className="bg-blue-600 py-20">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="text-center">
              <h1 className="text-4xl font-bold tracking-tight text-white sm:text-5xl md:text-6xl">
                Tolarian Knowledge Base
              </h1>
              <p className="mx-auto mt-3 max-w-md text-lg text-blue-100 sm:text-xl md:mt-5 md:max-w-3xl">
                A comprehensive knowledge base system for development teams featuring markdown documentation, syntax highlighting, and rapid search capabilities.
              </p>
              <div className="mx-auto mt-10 max-w-md sm:flex sm:justify-center md:mt-12">
                <Link
                  href="/articles"
                  className="flex w-full items-center justify-center rounded-md bg-white px-8 py-3 text-base font-medium text-blue-600 hover:bg-gray-50 md:px-10 md:py-4 md:text-lg"
                >
                  Browse Articles
                </Link>
                <Link
                  href="/articles/create"
                  className="mt-3 flex w-full items-center justify-center rounded-md bg-blue-500 px-8 py-3 text-base font-medium text-white hover:bg-blue-400 sm:ml-3 sm:mt-0 md:px-10 md:py-4 md:text-lg"
                >
                  Create Article
                </Link>
              </div>
            </div>
          </div>
        </div>

        <div className="py-12">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <h2 className="mb-8 text-3xl font-bold text-gray-900">Features</h2>
            <div className="grid gap-8 md:grid-cols-3">
              <div className="rounded-lg border border-gray-200 p-6">
                <FileText className="h-12 w-12 text-blue-600" />
                <h3 className="mt-4 text-xl font-semibold text-gray-900">
                  Markdown Support
                </h3>
                <p className="mt-2 text-gray-600">
                  Write documentation in Markdown with syntax highlighting for 20+ programming languages.
                </p>
              </div>
              <div className="rounded-lg border border-gray-200 p-6">
                <BookOpen className="h-12 w-12 text-blue-600" />
                <h3 className="mt-4 text-xl font-semibold text-gray-900">
                  Organized Content
                </h3>
                <p className="mt-2 text-gray-600">
                  Categorize and tag articles for easy organization and discovery.
                </p>
              </div>
              <div className="rounded-lg border border-gray-200 p-6">
                <Layers className="h-12 w-12 text-blue-600" />
                <h3 className="mt-4 text-xl font-semibold text-gray-900">
                  Fast Search
                </h3>
                <p className="mt-2 text-gray-600">
                  Find what you need quickly with PostgreSQL full-text search.
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
