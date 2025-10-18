'use client';

import { useQuery } from '@tanstack/react-query';
import { useParams } from 'next/navigation';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { articlesApi } from '@/lib/api';
import { formatDate } from '@/lib/utils';
import { Calendar, User, Tag as TagIcon } from 'lucide-react';

export default function ArticleDetailPage() {
  const params = useParams();
  const articleId = params.id as string;

  const { data: article, isLoading, error } = useQuery({
    queryKey: ['article', articleId],
    queryFn: () => articlesApi.getById(articleId),
  });

  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />

      <main className="flex-1 py-8">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          {isLoading && (
            <div className="text-center text-gray-600">Loading article...</div>
          )}

          {error && (
            <div className="rounded-lg bg-red-50 p-4 text-red-800">
              Error loading article. Make sure the backend API is running.
            </div>
          )}

          {article && (
            <article>
              <header className="mb-8">
                <h1 className="mb-4 text-4xl font-bold text-gray-900">
                  {article.title}
                </h1>

                <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600">
                  <div className="flex items-center gap-1">
                    <Calendar className="h-4 w-4" />
                    <span>{formatDate(article.createdAt)}</span>
                  </div>

                  {article.createdBy && (
                    <div className="flex items-center gap-1">
                      <User className="h-4 w-4" />
                      <span>{article.createdBy}</span>
                    </div>
                  )}

                  {article.categoryName && (
                    <span className="rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-800">
                      {article.categoryName}
                    </span>
                  )}
                </div>

                {article.tags.length > 0 && (
                  <div className="mt-4 flex flex-wrap gap-2">
                    {article.tags.map((tag) => (
                      <span
                        key={tag.id}
                        className="inline-flex items-center gap-1 rounded-full bg-blue-100 px-3 py-1 text-sm font-medium text-blue-800"
                      >
                        <TagIcon className="h-4 w-4" />
                        {tag.name}
                      </span>
                    ))}
                  </div>
                )}
              </header>

              <div className="prose max-w-none">
                <div className="whitespace-pre-wrap rounded-lg bg-gray-50 p-6">
                  {article.content}
                </div>
              </div>
            </article>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
}
