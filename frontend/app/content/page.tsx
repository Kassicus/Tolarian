'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import {
  Title1,
  Title3,
  Body1,
  Button,
  Card,
  CardHeader,
  makeStyles,
  shorthands,
  tokens,
  Spinner,
  SearchBox,
  Dropdown,
  Option,
  Badge,
  Toolbar,
  ToolbarButton,
  Divider,
} from '@fluentui/react-components';
import {
  DocumentTextRegular,
  FilterRegular,
  AddRegular,
  ArrowSortRegular,
  GridRegular,
  ListRegular,
  CalendarRegular,
  PersonRegular,
  TagRegular,
} from '@fluentui/react-icons';
import TopNavBarWrapper from '@/components/Navigation/TopNavBarWrapper';
import ContentCard from '@/components/Cards/ContentCard';
import apiClient, { Content } from '@/services/api';
import { useAuth } from '@/contexts/AuthContext';

const useStyles = makeStyles({
  container: {
    minHeight: '100vh',
    backgroundColor: tokens.colorNeutralBackground1,
  },

  header: {
    ...shorthands.padding(tokens.spacingVerticalXXL, tokens.spacingHorizontalL),
    backgroundColor: tokens.colorBrandBackground2,
  },

  headerContent: {
    maxWidth: '1200px',
    ...shorthands.margin('0', 'auto'),
  },

  headerTitle: {
    marginBottom: tokens.spacingVerticalM,
  },

  headerDescription: {
    color: tokens.colorNeutralForeground2,
    marginBottom: tokens.spacingVerticalL,
  },

  controls: {
    display: 'flex',
    gap: tokens.spacingHorizontalM,
    flexWrap: 'wrap',
    marginBottom: tokens.spacingVerticalXL,
  },

  searchBox: {
    flex: '1 1 300px',
    minWidth: '250px',
  },

  mainContent: {
    maxWidth: '1200px',
    ...shorthands.margin('0', 'auto'),
    ...shorthands.padding(tokens.spacingVerticalXL, tokens.spacingHorizontalL),
  },

  toolbar: {
    marginBottom: tokens.spacingVerticalL,
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    flexWrap: 'wrap',
    gap: tokens.spacingHorizontalM,
  },

  toolbarLeft: {
    display: 'flex',
    gap: tokens.spacingHorizontalS,
    alignItems: 'center',
  },

  toolbarRight: {
    display: 'flex',
    gap: tokens.spacingHorizontalS,
    alignItems: 'center',
  },

  contentGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
    gap: tokens.spacingHorizontalL,
  },

  contentList: {
    display: 'flex',
    flexDirection: 'column',
    gap: tokens.spacingHorizontalM,
  },

  loadingContainer: {
    display: 'flex',
    justifyContent: 'center',
    ...shorthands.padding(tokens.spacingVerticalXXXL),
  },

  emptyState: {
    textAlign: 'center',
    ...shorthands.padding(tokens.spacingVerticalXXXL),
  },

  emptyStateIcon: {
    fontSize: '48px',
    color: tokens.colorNeutralForeground3,
    marginBottom: tokens.spacingVerticalL,
  },

  stats: {
    display: 'flex',
    gap: tokens.spacingHorizontalM,
    marginBottom: tokens.spacingVerticalL,
  },

  statBadge: {
    padding: `${tokens.spacingVerticalXS} ${tokens.spacingHorizontalM}`,
  },

  pagination: {
    display: 'flex',
    justifyContent: 'center',
    gap: tokens.spacingHorizontalS,
    marginTop: tokens.spacingVerticalXXL,
  },
});

type ViewMode = 'grid' | 'list';
type SortBy = 'date' | 'title' | 'views';

export default function ContentPage() {
  const styles = useStyles();
  const router = useRouter();
  const { user } = useAuth();

  const [content, setContent] = useState<Content[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [viewMode, setViewMode] = useState<ViewMode>('grid');
  const [sortBy, setSortBy] = useState<SortBy>('date');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalItems, setTotalItems] = useState(0);

  useEffect(() => {
    fetchContent();
  }, [currentPage, selectedCategory, sortBy]);

  const fetchContent = async () => {
    try {
      setLoading(true);
      const response = await apiClient.getContent({
        page: currentPage,
        per_page: 12,
        category: selectedCategory === 'all' ? undefined : selectedCategory,
        sort: sortBy === 'date' ? 'created_at' : sortBy === 'title' ? 'title' : 'view_count',
        order: sortBy === 'views' ? 'desc' : 'asc',
      });

      if (response.success && response.data) {
        setContent(response.data);
        if (response.pagination) {
          setTotalPages(response.pagination.total_pages);
          setTotalItems(response.pagination.total);
        }
      }
    } catch (error) {
      console.error('Error fetching content:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (searchQuery.trim()) {
      router.push(`/search?q=${encodeURIComponent(searchQuery)}`);
    }
  };

  const canCreateContent = user && (user.role === 'editor' || user.role === 'admin');

  return (
    <div className={styles.container}>
      <TopNavBarWrapper user={user} />

      {/* Header */}
      <section className={styles.header}>
        <div className={styles.headerContent}>
          <Title1 className={styles.headerTitle}>
            <DocumentTextRegular /> Content Library
          </Title1>
          <Body1 className={styles.headerDescription}>
            Browse and discover documentation, guides, templates, and resources
          </Body1>

          <div className={styles.controls}>
            <SearchBox
              className={styles.searchBox}
              placeholder="Search content..."
              value={searchQuery}
              onChange={(e, data) => setSearchQuery(data.value)}
              onClear={() => setSearchQuery('')}
              size="large"
              appearance="filled-lighter"
              onKeyDown={(e) => {
                if (e.key === 'Enter') handleSearch();
              }}
            />

            <Dropdown
              placeholder="Category"
              value={selectedCategory}
              onOptionSelect={(e, data) => {
                setSelectedCategory(data.optionValue as string);
                setCurrentPage(1);
              }}
            >
              <Option value="all">All Categories</Option>
              <Option value="development">Development</Option>
              <Option value="templates">Templates</Option>
              <Option value="guides">Guides</Option>
              <Option value="documentation">Documentation</Option>
            </Dropdown>

            {canCreateContent && (
              <Button
                appearance="primary"
                icon={<AddRegular />}
                onClick={() => router.push('/content/new')}
              >
                Create Content
              </Button>
            )}
          </div>
        </div>
      </section>

      {/* Main Content */}
      <section className={styles.mainContent}>
        {/* Toolbar */}
        <div className={styles.toolbar}>
          <div className={styles.toolbarLeft}>
            {!loading && (
              <Body1>
                Showing {content.length} of {totalItems} items
              </Body1>
            )}
          </div>

          <div className={styles.toolbarRight}>
            <Dropdown
              placeholder="Sort by"
              value={sortBy}
              onOptionSelect={(e, data) => setSortBy(data.optionValue as SortBy)}
            >
              <Option value="date">Date</Option>
              <Option value="title">Title</Option>
              <Option value="views">Most Viewed</Option>
            </Dropdown>

            <ToolbarButton
              icon={<GridRegular />}
              appearance={viewMode === 'grid' ? 'primary' : 'subtle'}
              onClick={() => setViewMode('grid')}
            />
            <ToolbarButton
              icon={<ListRegular />}
              appearance={viewMode === 'list' ? 'primary' : 'subtle'}
              onClick={() => setViewMode('list')}
            />
          </div>
        </div>

        {/* Content Display */}
        {loading ? (
          <div className={styles.loadingContainer}>
            <Spinner size="large" label="Loading content..." />
          </div>
        ) : content.length > 0 ? (
          <>
            <div className={viewMode === 'grid' ? styles.contentGrid : styles.contentList}>
              {content.map((item) => (
                <ContentCard
                  key={item.id}
                  content={item}
                  onCardClick={() => router.push(`/content/${item.id}`)}
                  viewMode={viewMode}
                />
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className={styles.pagination}>
                <Button
                  appearance="outline"
                  disabled={currentPage === 1}
                  onClick={() => setCurrentPage(currentPage - 1)}
                >
                  Previous
                </Button>

                {[...Array(Math.min(5, totalPages))].map((_, i) => {
                  const pageNum = i + 1;
                  return (
                    <Button
                      key={pageNum}
                      appearance={pageNum === currentPage ? 'primary' : 'subtle'}
                      onClick={() => setCurrentPage(pageNum)}
                    >
                      {pageNum}
                    </Button>
                  );
                })}

                {totalPages > 5 && (
                  <>
                    <span>...</span>
                    <Button
                      appearance={totalPages === currentPage ? 'primary' : 'subtle'}
                      onClick={() => setCurrentPage(totalPages)}
                    >
                      {totalPages}
                    </Button>
                  </>
                )}

                <Button
                  appearance="outline"
                  disabled={currentPage === totalPages}
                  onClick={() => setCurrentPage(currentPage + 1)}
                >
                  Next
                </Button>
              </div>
            )}
          </>
        ) : (
          <div className={styles.emptyState}>
            <DocumentTextRegular className={styles.emptyStateIcon} />
            <Title3>No content found</Title3>
            <Body1>
              {selectedCategory !== 'all'
                ? 'Try selecting a different category or search term'
                : 'Start by creating your first piece of content'}
            </Body1>
            {canCreateContent && (
              <Button
                appearance="primary"
                icon={<AddRegular />}
                onClick={() => router.push('/content/new')}
                style={{ marginTop: tokens.spacingVerticalL }}
              >
                Create Content
              </Button>
            )}
          </div>
        )}
      </section>
    </div>
  );
}