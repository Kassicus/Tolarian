import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';

export default function CreateArticlePage() {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />

      <main className="flex-1 py-8">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <h1 className="mb-8 text-3xl font-bold text-gray-900">Create Article</h1>

          <div className="rounded-lg border border-blue-200 bg-blue-50 p-6">
            <h2 className="mb-2 text-lg font-semibold text-blue-900">
              Coming in Phase 2
            </h2>
            <p className="text-blue-800">
              The markdown editor with live preview will be implemented in Phase 2.
              For now, you can use the API directly to create articles.
            </p>
            <p className="mt-4 text-sm text-blue-700">
              Phase 2 will include:
            </p>
            <ul className="mt-2 list-inside list-disc text-sm text-blue-700">
              <li>Markdown editor with live preview</li>
              <li>Syntax highlighting for code blocks</li>
              <li>Image upload and insertion</li>
              <li>Tag and category selection</li>
            </ul>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
