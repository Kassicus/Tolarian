export function Sidebar() {
  return (
    <aside className="w-64 border-r border-gray-200 bg-gray-50 p-4">
      <div className="space-y-4">
        <div>
          <h3 className="mb-2 text-sm font-semibold text-gray-900">Categories</h3>
          <ul className="space-y-1 text-sm text-gray-600">
            <li className="hover:text-blue-600 cursor-pointer">All Articles</li>
            <li className="hover:text-blue-600 cursor-pointer">Getting Started</li>
            <li className="hover:text-blue-600 cursor-pointer">Guides</li>
            <li className="hover:text-blue-600 cursor-pointer">Tutorials</li>
          </ul>
        </div>
        <div>
          <h3 className="mb-2 text-sm font-semibold text-gray-900">Tags</h3>
          <div className="flex flex-wrap gap-2">
            <span className="inline-flex items-center rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-800 cursor-pointer hover:bg-blue-200">
              React
            </span>
            <span className="inline-flex items-center rounded-full bg-green-100 px-2.5 py-0.5 text-xs font-medium text-green-800 cursor-pointer hover:bg-green-200">
              Next.js
            </span>
            <span className="inline-flex items-center rounded-full bg-purple-100 px-2.5 py-0.5 text-xs font-medium text-purple-800 cursor-pointer hover:bg-purple-200">
              TypeScript
            </span>
          </div>
        </div>
      </div>
    </aside>
  );
}
