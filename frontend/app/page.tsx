'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
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
  SearchBox,
  Spinner,
} from '@fluentui/react-components';
import {
  BookRegular,
  DocumentTextRegular,
  CodeRegular,
  DocumentRegular,
  SearchRegular,
  AddRegular,
  ArrowRightRegular,
} from '@fluentui/react-icons';
import TopNavBarWrapper from '@/components/Navigation/TopNavBarWrapper';
import ContentCard from '@/components/Cards/ContentCard';
import apiClient, { Content, Category } from '@/services/api';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';

const useStyles = makeStyles({
  container: {
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    backgroundColor: tokens.colorNeutralBackground1,
  },

  hero: {
    ...shorthands.padding(tokens.spacingVerticalXXXL, tokens.spacingHorizontalL),
    textAlign: 'center',
    background: `linear-gradient(180deg, ${tokens.colorBrandBackground2} 0%, ${tokens.colorNeutralBackground1} 100%)`,
  },

  heroContent: {
    maxWidth: '800px',
    ...shorthands.margin('0', 'auto'),
  },

  heroTitle: {
    fontSize: tokens.fontSizeHero900,
    fontWeight: tokens.fontWeightBold,
    marginBottom: tokens.spacingVerticalL,
    color: tokens.colorNeutralForeground1,
  },

  heroDescription: {
    fontSize: tokens.fontSizeBase400,
    color: tokens.colorNeutralForeground2,
    marginBottom: tokens.spacingVerticalXXL,
  },

  searchContainer: {
    maxWidth: '600px',
    ...shorthands.margin('0', 'auto', tokens.spacingVerticalXXL),
  },

  searchBox: {
    width: '100%',
  },

  statsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    ...shorthands.gap(tokens.spacingHorizontalL),
    ...shorthands.padding(tokens.spacingVerticalXL, tokens.spacingHorizontalL),
    maxWidth: '1200px',
    ...shorthands.margin('0', 'auto'),
  },

  statCard: {
    textAlign: 'center',
    ...shorthands.padding(tokens.spacingVerticalL),
  },

  statValue: {
    fontSize: tokens.fontSizeHero700,
    fontWeight: tokens.fontWeightBold,
    color: tokens.colorBrandForeground1,
  },

  statLabel: {
    fontSize: tokens.fontSizeBase200,
    color: tokens.colorNeutralForeground3,
    textTransform: 'uppercase',
  },

  section: {
    ...shorthands.padding(tokens.spacingVerticalXXL, tokens.spacingHorizontalL),
    maxWidth: '1200px',
    ...shorthands.margin('0', 'auto'),
    width: '100%',
  },

  sectionTitle: {
    marginBottom: tokens.spacingVerticalXL,
  },

  categoriesGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
    ...shorthands.gap(tokens.spacingHorizontalL),
  },

  categoryCard: {
    cursor: 'pointer',
    transition: 'all 0.2s ease',
    ':hover': {
      transform: 'translateY(-2px)',
      boxShadow: tokens.shadow16,
    },
  },

  recentContent: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
    ...shorthands.gap(tokens.spacingHorizontalL),
  },

  cta: {
    ...shorthands.padding(tokens.spacingVerticalXXXL, tokens.spacingHorizontalL),
    background: tokens.colorNeutralBackground2,
    textAlign: 'center',
  },

  ctaCard: {
    maxWidth: '600px',
    ...shorthands.margin('0', 'auto'),
    ...shorthands.padding(tokens.spacingVerticalXXL),
  },

  loadingContainer: {
    display: 'flex',
    justifyContent: 'center',
    ...shorthands.padding(tokens.spacingVerticalXXL),
  },
});

const categories = [
  {
    id: 'development',
    name: 'Development',
    icon: <CodeRegular fontSize={24} />,
    description: 'Code standards, best practices, and development guides.',
    color: 'brand',
  },
  {
    id: 'templates',
    name: 'Templates',
    icon: <DocumentRegular fontSize={24} />,
    description: 'Ready-to-use project templates and boilerplates.',
    color: 'success',
  },
  {
    id: 'guides',
    name: 'Guides',
    icon: <BookRegular fontSize={24} />,
    description: 'Step-by-step tutorials and how-to guides.',
    color: 'informative',
  },
];

export default function HomePage() {
  const styles = useStyles();
  const router = useRouter();
  const { user } = useAuth();
  const [searchQuery, setSearchQuery] = useState('');
  const [recentContent, setRecentContent] = useState<Content[]>([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    documents: 0,
    templates: 0,
    categories: 0,
    contributors: 0,
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const contentResponse = await apiClient.getContent({ per_page: 6 });
      if (contentResponse.success && contentResponse.data) {
        setRecentContent(contentResponse.data);
      }

      // Fetch stats (you might need to add this endpoint)
      // const statsResponse = await apiClient.getStats();
      // setStats(statsResponse.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => {
    if (searchQuery.trim()) {
      router.push(`/search?q=${encodeURIComponent(searchQuery)}`);
    }
  };

  return (
    <div className={styles.container}>
      <TopNavBarWrapper user={user} />

      {/* Hero Section */}
      <section className={styles.hero}>
        <div className={styles.heroContent}>
          <Title1 className={styles.heroTitle}>
            <BookRegular /> Tolarian Knowledge Base
          </Title1>
          <Body1 className={styles.heroDescription}>
            Centralized knowledge management for development teams.
            Find project templates, documentation, guides, and resources all in one place.
          </Body1>

          <div className={styles.searchContainer}>
            <SearchBox
              className={styles.searchBox}
              placeholder="Search for documentation, guides, templates..."
              size="large"
              value={searchQuery}
              onChange={(e, data) => setSearchQuery(data.value)}
              onClear={() => setSearchQuery('')}
              appearance="filled-darker"
              contentAfter={
                <Button
                  appearance="primary"
                  icon={<SearchRegular />}
                  onClick={handleSearch}
                >
                  Search
                </Button>
              }
              onKeyDown={(e) => {
                if (e.key === 'Enter') handleSearch();
              }}
            />
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className={styles.statsGrid}>
        <Card className={styles.statCard}>
          <div className={styles.statValue}>{stats.documents}</div>
          <div className={styles.statLabel}>Documents</div>
        </Card>
        <Card className={styles.statCard}>
          <div className={styles.statValue}>{stats.templates}</div>
          <div className={styles.statLabel}>Templates</div>
        </Card>
        <Card className={styles.statCard}>
          <div className={styles.statValue}>{stats.categories}</div>
          <div className={styles.statLabel}>Categories</div>
        </Card>
        <Card className={styles.statCard}>
          <div className={styles.statValue}>{stats.contributors}</div>
          <div className={styles.statLabel}>Contributors</div>
        </Card>
      </section>

      {/* Categories */}
      <section className={styles.section}>
        <Title3 className={styles.sectionTitle}>Browse by Category</Title3>
        <div className={styles.categoriesGrid}>
          {categories.map((category) => (
            <Card
              key={category.id}
              className={styles.categoryCard}
              appearance="filled-alternative"
              onClick={() => router.push(`/content?category=${category.id}`)}
            >
              <CardHeader
                image={category.icon}
                header={category.name}
                description={category.description}
                action={
                  <Button
                    appearance="transparent"
                    icon={<ArrowRightRegular />}
                    size="small"
                  >
                    Browse
                  </Button>
                }
              />
            </Card>
          ))}
        </div>
      </section>

      {/* Recent Content */}
      <section className={styles.section}>
        <Title3 className={styles.sectionTitle}>Recent Content</Title3>
        {loading ? (
          <div className={styles.loadingContainer}>
            <Spinner size="large" label="Loading content..." />
          </div>
        ) : recentContent.length > 0 ? (
          <div className={styles.recentContent}>
            {recentContent.map((content) => (
              <ContentCard
                key={content.id}
                content={content}
                onCardClick={() => router.push(`/content/${content.id}`)}
              />
            ))}
          </div>
        ) : (
          <Card>
            <CardHeader
              header="No content yet"
              description="Start by adding your first document!"
            />
          </Card>
        )}
      </section>

      {/* CTA */}
      <section className={styles.cta}>
        <Card className={styles.ctaCard}>
          <Title3>Ready to Get Started?</Title3>
          <Body1 style={{ margin: `${tokens.spacingVerticalL} 0` }}>
            Login to start contributing to the knowledge base or browse existing content.
          </Body1>
          <div style={{ display: 'flex', gap: tokens.spacingHorizontalM, justifyContent: 'center' }}>
            <Button appearance="primary" size="large" onClick={() => router.push('/login')}>
              Login
            </Button>
            <Button appearance="outline" size="large" onClick={() => router.push('/content')}>
              Browse Content
            </Button>
          </div>
        </Card>
      </section>
    </div>
  );
}