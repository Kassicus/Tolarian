import Link from 'next/link';
import { Calendar, User, Tag as TagIcon } from 'lucide-react';
import type { Article } from '@/types';
import { formatRelativeTime } from '@/lib/utils';

interface ArticleCardProps {
  article: Article;
}

export function ArticleCard({ article }: ArticleCardProps) {
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm transition-shadow hover:shadow-md">
      <Link href={`/articles/${article.id}`}>
        <h3 className="mb-2 text-xl font-semibold text-gray-900 hover:text-blue-600">
          {article.title}
        </h3>
      </Link>

      <p className="mb-4 line-clamp-3 text-gray-600">
        {article.content.substring(0, 200)}...
      </p>

      <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500">
        <div className="flex items-center gap-1">
          <Calendar className="h-4 w-4" />
          <span>{formatRelativeTime(article.createdAt)}</span>
        </div>

        {article.createdBy && (
          <div className="flex items-center gap-1">
            <User className="h-4 w-4" />
            <span>{article.createdBy}</span>
          </div>
        )}

        {article.categoryName && (
          <span className="rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium text-gray-800">
            {article.categoryName}
          </span>
        )}
      </div>

      {article.tags.length > 0 && (
        <div className="mt-4 flex flex-wrap gap-2">
          {article.tags.map((tag) => (
            <span
              key={tag.id}
              className="inline-flex items-center gap-1 rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-800"
            >
              <TagIcon className="h-3 w-3" />
              {tag.name}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
