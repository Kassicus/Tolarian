'use client';

import React, { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import {
  Title1,
  Body1,
  Button,
  Card,
  makeStyles,
  shorthands,
  tokens,
  Spinner,
  SearchBox,
  Badge,
  Dropdown,
  Option,
} from '@fluentui/react-components';
import {
  SearchRegular,
  FilterRegular,
  DocumentTextRegular,
  ArrowLeftRegular,
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
    display: 'flex',
    alignItems: 'center',
    gap: tokens.spacingHorizontalM,
    marginBottom: tokens.spacingVerticalL,
  },

  searchContainer: {
    display: 'flex',
    gap: tokens.spacingHorizontalM,
    marginBottom: tokens.spacingVerticalXL,
    flexWrap: 'wrap',
  },

  searchBox: {
    flex: '1 1 400px',
    minWidth: '250px',
  },

  mainContent: {
    maxWidth: '1200px',
    ...shorthands.margin('0', 'auto'),
    ...shorthands.padding(tokens.spacingVerticalXL, tokens.spacingHorizontalL),
  },

  resultsHeader: {
    marginBottom: tokens.spacingVerticalL,
  },

  resultsCount: {
    color: tokens.colorNeutralForeground2,
    marginBottom: tokens.spacingVerticalM,
  },

  resultsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
    gap: tokens.spacingHorizontalL,
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

  suggestions: {
    marginTop: tokens.spacingVerticalXL,
  },

  suggestionList: {
    listStyle: 'none',
    padding: 0,
    margin: 0,
    '& li': {
      marginBottom: tokens.spacingVerticalS,
    },
  },

  suggestionItem: {
    color: tokens.colorBrandForeground1,
    cursor: 'pointer',
    textDecoration: 'none',
    ':hover': {
      textDecoration: 'underline',
    },
  },
});

export default function SearchPage() {
  const styles = useStyles();
  const router = useRouter();
  const searchParams = useSearchParams();
  const { user } = useAuth();

  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<Content[]>([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  useEffect(() => {
    const query = searchParams?.get('q');
    if (query) {
      setSearchQuery(query);
      performSearch(query);
    }
  }, [searchParams]);

  const performSearch = async (query: string, category?: string) => {
    if (!query.trim()) return;

    setLoading(true);
    setHasSearched(true);

    try {
      const response = await apiClient.search(
        query,
        category === 'all' ? undefined : category,
        50
      );

      if (response.success && response.data) {
        setSearchResults(response.data);
      } else {
        setSearchResults([]);
      }
    } catch (error) {
      console.error('Search error:', error);
      setSearchResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => {
    if (searchQuery.trim()) {
      // Update URL with search query
      const params = new URLSearchParams();
      params.set('q', searchQuery);
      if (selectedCategory !== 'all') {
        params.set('category', selectedCategory);
      }
      router.push(`/search?${params.toString()}`);

      performSearch(searchQuery, selectedCategory);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const popularSearches = [
    'getting started',
    'authentication',
    'deployment',
    'API documentation',
    'templates',
    'best practices',
  ];

  return (
    <div className={styles.container}>
      <TopNavBarWrapper user={user} />

      {/* Search Header */}
      <section className={styles.header}>
        <div className={styles.headerContent}>
          <div className={styles.headerTitle}>
            <SearchRegular fontSize={32} />
            <Title1>Search Knowledge Base</Title1>
          </div>

          <div className={styles.searchContainer}>
            <SearchBox
              className={styles.searchBox}
              placeholder="Search for documentation, guides, templates..."
              value={searchQuery}
              onChange={(e, data) => setSearchQuery(data.value)}
              onClear={() => {
                setSearchQuery('');
                setSearchResults([]);
                setHasSearched(false);
              }}
              size="large"
              appearance="filled-lighter"
              onKeyDown={handleKeyDown}
            />

            <Dropdown
              placeholder="Category"
              value={selectedCategory}
              onOptionSelect={(e, data) => {
                setSelectedCategory(data.optionValue as string);
              }}
            >
              <Option value="all">All Categories</Option>
              <Option value="development">Development</Option>
              <Option value="templates">Templates</Option>
              <Option value="guides">Guides</Option>
              <Option value="documentation">Documentation</Option>
            </Dropdown>

            <Button
              appearance="primary"
              icon={<SearchRegular />}
              size="large"
              onClick={handleSearch}
              disabled={!searchQuery.trim()}
            >
              Search
            </Button>
          </div>
        </div>
      </section>

      {/* Search Results */}
      <section className={styles.mainContent}>
        {loading ? (
          <div className={styles.loadingContainer}>
            <Spinner size="large" label="Searching..." />
          </div>
        ) : hasSearched ? (
          searchResults.length > 0 ? (
            <>
              <div className={styles.resultsHeader}>
                <Body1 className={styles.resultsCount}>
                  Found {searchResults.length} result{searchResults.length !== 1 ? 's' : ''} for "{searchQuery}"
                  {selectedCategory !== 'all' && ` in ${selectedCategory}`}
                </Body1>
              </div>

              <div className={styles.resultsGrid}>
                {searchResults.map((content) => (
                  <ContentCard
                    key={content.id}
                    content={content}
                    onCardClick={() => router.push(`/content/${content.id}`)}
                  />
                ))}
              </div>
            </>
          ) : (
            <div className={styles.emptyState}>
              <DocumentTextRegular className={styles.emptyStateIcon} />
              <Title1>No results found</Title1>
              <Body1>
                We couldn't find any content matching "{searchQuery}"
                {selectedCategory !== 'all' && ` in ${selectedCategory}`}.
              </Body1>
              <Body1>Try adjusting your search terms or browse all content.</Body1>

              <Button
                appearance="primary"
                icon={<ArrowLeftRegular />}
                onClick={() => router.push('/content')}
                style={{ marginTop: tokens.spacingVerticalL }}
              >
                Browse All Content
              </Button>
            </div>
          )
        ) : (
          <div className={styles.emptyState}>
            <SearchRegular className={styles.emptyStateIcon} />
            <Title1>What are you looking for?</Title1>
            <Body1>
              Enter a search term above to find documentation, guides, and resources.
            </Body1>

            <div className={styles.suggestions}>
              <Body1 style={{ marginBottom: tokens.spacingVerticalM }}>
                <strong>Popular searches:</strong>
              </Body1>
              <ul className={styles.suggestionList}>
                {popularSearches.map((term) => (
                  <li key={term}>
                    <a
                      className={styles.suggestionItem}
                      onClick={() => {
                        setSearchQuery(term);
                        performSearch(term);
                      }}
                    >
                      {term}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </section>
    </div>
  );
}