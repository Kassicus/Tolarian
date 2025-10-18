'use client';

import { useQuery } from '@tanstack/react-query';
import { Navbar } from '@/components/layout/Navbar';
import { Sidebar } from '@/components/layout/Sidebar';
import { Footer } from '@/components/layout/Footer';
import { ArticleCard } from '@/components/articles/ArticleCard';
import { articlesApi } from '@/lib/api';

export default function ArticlesPage() {
  const { data: articles, isLoading, error } = useQuery({
    queryKey: ['articles'],
    queryFn: () => articlesApi.getAll(1, 20),
  });

  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />

      <div className="flex flex-1">
        <Sidebar />

        <main className="flex-1 p-8">
          <div className="mx-auto max-w-5xl">
            <h1 className="mb-8 text-3xl font-bold text-gray-900">Articles</h1>

            {isLoading && (
              <div className="text-center text-gray-600">Loading articles...</div>
            )}

            {error && (
              <div className="rounded-lg bg-red-50 p-4 text-red-800">
                Error loading articles. Make sure the backend API is running.
              </div>
            )}

            {articles && articles.length === 0 && (
              <div className="text-center text-gray-600">
                No articles yet. Create your first article to get started!
              </div>
            )}

            <div className="space-y-6">
              {articles?.map((article) => (
                <ArticleCard key={article.id} article={article} />
              ))}
            </div>
          </div>
        </main>
      </div>

      <Footer />
    </div>
  );
}
