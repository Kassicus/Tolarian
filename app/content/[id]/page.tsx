'use client';

import React, { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import ReactMarkdown from 'react-markdown';
import {
  Title1,
  Title2,
  Title3,
  Body1,
  Button,
  Card,
  makeStyles,
  shorthands,
  tokens,
  Spinner,
  Badge,
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbButton,
  BreadcrumbDivider,
  Divider,
  Avatar,
  MessageBar,
  MessageBarBody,
  Tooltip,
} from '@fluentui/react-components';
import {
  HomeRegular,
  DocumentTextRegular,
  CalendarRegular,
  PersonRegular,
  EyeRegular,
  EditRegular,
  DeleteRegular,
  ShareRegular,
  BookmarkRegular,
  CopyRegular,
  CheckmarkRegular,
  ArrowLeftRegular,
} from '@fluentui/react-icons';
import TopNavBarWrapper from '@/components/Navigation/TopNavBarWrapper';
import apiClient, { Content } from '@/services/api';
import { useAuth } from '@/contexts/AuthContext';

const useStyles = makeStyles({
  container: {
    minHeight: '100vh',
    backgroundColor: tokens.colorNeutralBackground1,
  },

  header: {
    ...shorthands.padding(tokens.spacingVerticalL, tokens.spacingHorizontalL),
    backgroundColor: tokens.colorNeutralBackground2,
    borderBottom: `1px solid ${tokens.colorNeutralStroke1}`,
  },

  headerContent: {
    maxWidth: '1200px',
    ...shorthands.margin('0', 'auto'),
  },

  breadcrumb: {
    marginBottom: tokens.spacingVerticalM,
  },

  mainContent: {
    maxWidth: '900px',
    ...shorthands.margin('0', 'auto'),
    ...shorthands.padding(tokens.spacingVerticalXXL, tokens.spacingHorizontalL),
  },

  contentCard: {
    ...shorthands.padding(tokens.spacingVerticalXXL, tokens.spacingHorizontalXXL),
  },

  title: {
    marginBottom: tokens.spacingVerticalL,
  },

  metadata: {
    display: 'flex',
    alignItems: 'center',
    flexWrap: 'wrap',
    ...shorthands.gap(tokens.spacingHorizontalL),
    marginBottom: tokens.spacingVerticalXL,
    color: tokens.colorNeutralForeground3,
  },

  metaItem: {
    display: 'flex',
    alignItems: 'center',
    ...shorthands.gap(tokens.spacingHorizontalXS),
  },

  badges: {
    display: 'flex',
    ...shorthands.gap(tokens.spacingHorizontalS),
    marginBottom: tokens.spacingVerticalL,
  },

  actions: {
    display: 'flex',
    ...shorthands.gap(tokens.spacingHorizontalM),
    marginBottom: tokens.spacingVerticalXL,
    flexWrap: 'wrap',
  },

  content: {
    lineHeight: '1.8',
    fontSize: tokens.fontSizeBase400,
    color: tokens.colorNeutralForeground1,
    '& h1': {
      fontSize: tokens.fontSizeHero700,
      fontWeight: tokens.fontWeightBold,
      marginTop: tokens.spacingVerticalXXL,
      marginBottom: tokens.spacingVerticalL,
    },
    '& h2': {
      fontSize: tokens.fontSizeBase600,
      fontWeight: tokens.fontWeightSemibold,
      marginTop: tokens.spacingVerticalXL,
      marginBottom: tokens.spacingVerticalM,
    },
    '& h3': {
      fontSize: tokens.fontSizeBase500,
      fontWeight: tokens.fontWeightSemibold,
      marginTop: tokens.spacingVerticalL,
      marginBottom: tokens.spacingVerticalM,
    },
    '& p': {
      marginBottom: tokens.spacingVerticalM,
    },
    '& ul, & ol': {
      marginLeft: tokens.spacingHorizontalXL,
      marginBottom: tokens.spacingVerticalM,
    },
    '& li': {
      marginBottom: tokens.spacingVerticalS,
    },
    '& code': {
      backgroundColor: tokens.colorNeutralBackground3,
      ...shorthands.padding('2px', '6px'),
      borderRadius: tokens.borderRadiusSmall,
      fontSize: '0.9em',
      fontFamily: 'Consolas, Monaco, "Courier New", monospace',
    },
    '& pre': {
      backgroundColor: tokens.colorNeutralBackground3,
      ...shorthands.padding(tokens.spacingVerticalM),
      borderRadius: tokens.borderRadiusMedium,
      overflowX: 'auto',
      marginBottom: tokens.spacingVerticalM,
      '& code': {
        backgroundColor: 'transparent',
        padding: 0,
      },
    },
    '& blockquote': {
      borderLeft: `4px solid ${tokens.colorBrandForeground1}`,
      paddingLeft: tokens.spacingHorizontalL,
      marginLeft: 0,
      marginBottom: tokens.spacingVerticalM,
      color: tokens.colorNeutralForeground2,
      fontStyle: 'italic',
    },
    '& table': {
      width: '100%',
      borderCollapse: 'collapse',
      marginBottom: tokens.spacingVerticalM,
    },
    '& th, & td': {
      ...shorthands.padding(tokens.spacingVerticalS, tokens.spacingHorizontalM),
      borderBottom: `1px solid ${tokens.colorNeutralStroke1}`,
      textAlign: 'left',
    },
    '& th': {
      fontWeight: tokens.fontWeightSemibold,
      backgroundColor: tokens.colorNeutralBackground2,
    },
    '& img': {
      maxWidth: '100%',
      height: 'auto',
      borderRadius: tokens.borderRadiusMedium,
      marginBottom: tokens.spacingVerticalM,
    },
    '& a': {
      color: tokens.colorBrandForeground1,
      textDecoration: 'none',
      ':hover': {
        textDecoration: 'underline',
      },
    },
  },

  sidebar: {
    position: 'sticky',
    top: tokens.spacingVerticalXXL,
    marginLeft: tokens.spacingHorizontalXXL,
  },

  toc: {
    ...shorthands.padding(tokens.spacingVerticalL),
    backgroundColor: tokens.colorNeutralBackground2,
    borderRadius: tokens.borderRadiusMedium,
  },

  tocTitle: {
    marginBottom: tokens.spacingVerticalM,
    fontWeight: tokens.fontWeightSemibold,
  },

  tocList: {
    listStyle: 'none',
    padding: 0,
    margin: 0,
    '& li': {
      marginBottom: tokens.spacingVerticalS,
    },
    '& a': {
      color: tokens.colorNeutralForeground2,
      textDecoration: 'none',
      ':hover': {
        color: tokens.colorBrandForeground1,
      },
    },
  },

  loadingContainer: {
    display: 'flex',
    justifyContent: 'center',
    ...shorthands.padding(tokens.spacingVerticalXXXL),
  },

  errorContainer: {
    ...shorthands.padding(tokens.spacingVerticalXXXL),
    textAlign: 'center',
  },

  tags: {
    display: 'flex',
    flexWrap: 'wrap',
    ...shorthands.gap(tokens.spacingHorizontalXS),
    marginTop: tokens.spacingVerticalXL,
  },

  authorSection: {
    display: 'flex',
    alignItems: 'center',
    ...shorthands.gap(tokens.spacingHorizontalM),
    ...shorthands.padding(tokens.spacingVerticalL),
    backgroundColor: tokens.colorNeutralBackground2,
    borderRadius: tokens.borderRadiusMedium,
    marginTop: tokens.spacingVerticalXXL,
  },
});

export default function ContentDetailPage() {
  const styles = useStyles();
  const router = useRouter();
  const params = useParams();
  const { user } = useAuth();

  const [content, setContent] = useState<Content | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  const contentId = params?.id as string;

  useEffect(() => {
    if (contentId) {
      fetchContent();
    }
  }, [contentId]);

  const fetchContent = async () => {
    try {
      setLoading(true);
      const response = await apiClient.getContentById(contentId);
      if (response.success && response.data) {
        setContent(response.data);
      } else {
        setError('Content not found');
      }
    } catch (error) {
      console.error('Error fetching content:', error);
      setError('Failed to load content');
    } finally {
      setLoading(false);
    }
  };

  const handleCopyLink = () => {
    const url = window.location.href;
    navigator.clipboard.writeText(url);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleEdit = () => {
    router.push(`/content/${contentId}/edit`);
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this content?')) {
      try {
        await apiClient.deleteContent(contentId);
        router.push('/content');
      } catch (error) {
        console.error('Error deleting content:', error);
      }
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const canEdit = user && content && (
    user.role === 'admin' ||
    (user.role === 'editor' && user.id === content.author_id)
  );

  if (loading) {
    return (
      <div className={styles.container}>
        <TopNavBarWrapper user={user} />
        <div className={styles.loadingContainer}>
          <Spinner size="large" label="Loading content..." />
        </div>
      </div>
    );
  }

  if (error || !content) {
    return (
      <div className={styles.container}>
        <TopNavBarWrapper user={user} />
        <div className={styles.errorContainer}>
          <Title2>Content Not Found</Title2>
          <Body1>{error || 'The requested content could not be found.'}</Body1>
          <Button
            appearance="primary"
            icon={<ArrowLeftRegular />}
            onClick={() => router.push('/content')}
            style={{ marginTop: tokens.spacingVerticalL }}
          >
            Back to Content Library
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <TopNavBarWrapper user={user} />

      {/* Header */}
      <section className={styles.header}>
        <div className={styles.headerContent}>
          <Breadcrumb className={styles.breadcrumb}>
            <BreadcrumbItem>
              <BreadcrumbButton icon={<HomeRegular />} onClick={() => router.push('/')}>
                Home
              </BreadcrumbButton>
            </BreadcrumbItem>
            <BreadcrumbDivider />
            <BreadcrumbItem>
              <BreadcrumbButton icon={<DocumentTextRegular />} onClick={() => router.push('/content')}>
                Content Library
              </BreadcrumbButton>
            </BreadcrumbItem>
            <BreadcrumbDivider />
            <BreadcrumbItem current>
              {content.title}
            </BreadcrumbItem>
          </Breadcrumb>
        </div>
      </section>

      {/* Main Content */}
      <section className={styles.mainContent}>
        <Card className={styles.contentCard}>
          {/* Title */}
          <Title1 className={styles.title}>{content.title}</Title1>

          {/* Badges */}
          <div className={styles.badges}>
            {content.content_type && (
              <Badge appearance="tint" color="brand">
                {content.content_type}
              </Badge>
            )}
            {content.category && (
              <Badge appearance="tint" color="informative">
                {content.category}
              </Badge>
            )}
            {content.is_featured && (
              <Badge appearance="tint" color="warning">
                Featured
              </Badge>
            )}
            {content.status === 'draft' && (
              <Badge appearance="tint" color="subtle">
                Draft
              </Badge>
            )}
          </div>

          {/* Metadata */}
          <div className={styles.metadata}>
            <div className={styles.metaItem}>
              <CalendarRegular fontSize={16} />
              <Body1>Published {formatDate(content.published_at || content.created_at)}</Body1>
            </div>
            <div className={styles.metaItem}>
              <CalendarRegular fontSize={16} />
              <Body1>Updated {formatDate(content.updated_at)}</Body1>
            </div>
            {content.view_count !== undefined && (
              <div className={styles.metaItem}>
                <EyeRegular fontSize={16} />
                <Body1>{content.view_count} views</Body1>
              </div>
            )}
          </div>

          {/* Actions */}
          <div className={styles.actions}>
            <Button
              appearance="outline"
              icon={copied ? <CheckmarkRegular /> : <CopyRegular />}
              onClick={handleCopyLink}
            >
              {copied ? 'Copied!' : 'Copy Link'}
            </Button>
            <Button
              appearance="outline"
              icon={<ShareRegular />}
            >
              Share
            </Button>
            <Button
              appearance="outline"
              icon={<BookmarkRegular />}
            >
              Bookmark
            </Button>
            {canEdit && (
              <>
                <Button
                  appearance="outline"
                  icon={<EditRegular />}
                  onClick={handleEdit}
                >
                  Edit
                </Button>
                <Button
                  appearance="outline"
                  icon={<DeleteRegular />}
                  onClick={handleDelete}
                >
                  Delete
                </Button>
              </>
            )}
          </div>

          <Divider />

          {/* Content Body */}
          <div className={styles.content}>
            <ReactMarkdown>
              {content.body || 'No content available.'}
            </ReactMarkdown>
          </div>

          {/* Tags */}
          {content.tags && content.tags.length > 0 && (
            <>
              <Divider />
              <div className={styles.tags}>
                <Body1 style={{ marginRight: tokens.spacingHorizontalM }}>Tags:</Body1>
                {content.tags.map((tag, index) => (
                  <Badge
                    key={index}
                    appearance="outline"
                    shape="rounded"
                  >
                    {tag}
                  </Badge>
                ))}
              </div>
            </>
          )}

          {/* Author Section */}
          {content.author_id && (
            <>
              <Divider style={{ marginTop: tokens.spacingVerticalXXL }} />
              <div className={styles.authorSection}>
                <Avatar
                  name="Author"
                  size={48}
                  icon={<PersonRegular />}
                />
                <div>
                  <Title3>About the Author</Title3>
                  <Body1>Content created by user {content.author_id}</Body1>
                </div>
              </div>
            </>
          )}
        </Card>
      </section>
    </div>
  );
}