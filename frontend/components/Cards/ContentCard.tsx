'use client';

import React from 'react';
import Link from 'next/link';
import {
  Card,
  CardHeader,
  CardPreview,
  Text,
  Badge,
  Button,
  makeStyles,
  shorthands,
  tokens,
  Caption1,
  Body1,
} from '@fluentui/react-components';
import {
  DocumentTextRegular,
  CalendarRegular,
  PersonRegular,
  EyeRegular,
  StarRegular,
  StarFilled,
} from '@fluentui/react-icons';
import { Content } from '@/services/api';

const useStyles = makeStyles({
  card: {
    width: '100%',
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
    cursor: 'pointer',
    transition: 'all 0.2s ease',
    ':hover': {
      transform: 'translateY(-2px)',
      boxShadow: tokens.shadow16,
    },
  },

  cardHeader: {
    ...shorthands.padding(tokens.spacingVerticalM, tokens.spacingHorizontalL),
  },

  title: {
    fontSize: tokens.fontSizeBase500,
    fontWeight: tokens.fontWeightSemibold,
    color: tokens.colorNeutralForeground1,
    marginBottom: tokens.spacingVerticalS,
    display: '-webkit-box',
    WebkitLineClamp: 2,
    WebkitBoxOrient: 'vertical',
    overflow: 'hidden',
  },

  preview: {
    ...shorthands.padding(tokens.spacingVerticalS, tokens.spacingHorizontalL),
    backgroundColor: tokens.colorNeutralBackground3,
    minHeight: '80px',
  },

  excerpt: {
    color: tokens.colorNeutralForeground2,
    display: '-webkit-box',
    WebkitLineClamp: 3,
    WebkitBoxOrient: 'vertical',
    overflow: 'hidden',
    lineHeight: '1.5',
  },

  metadata: {
    display: 'flex',
    alignItems: 'center',
    flexWrap: 'wrap',
    ...shorthands.gap(tokens.spacingHorizontalM),
    marginTop: tokens.spacingVerticalM,
    color: tokens.colorNeutralForeground3,
  },

  metaItem: {
    display: 'flex',
    alignItems: 'center',
    ...shorthands.gap(tokens.spacingHorizontalXS),
  },

  tags: {
    display: 'flex',
    flexWrap: 'wrap',
    ...shorthands.gap(tokens.spacingHorizontalXS),
    marginTop: tokens.spacingVerticalS,
  },

  featuredBadge: {
    position: 'absolute',
    top: tokens.spacingVerticalM,
    right: tokens.spacingHorizontalM,
    zIndex: 1,
  },

  categoryBadge: {
    textTransform: 'capitalize',
  },
});

interface ContentCardProps {
  content: Partial<Content>;
  showAuthor?: boolean;
  showStats?: boolean;
  onCardClick?: () => void;
  viewMode?: 'grid' | 'list';
}

export default function ContentCard({
  content,
  showAuthor = true,
  showStats = true,
  onCardClick,
  viewMode = 'grid'
}: ContentCardProps) {
  const styles = useStyles();

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getExcerpt = () => {
    if (!content.body) return 'No content available';
    // Remove markdown formatting and truncate
    const plainText = content.body
      .replace(/[#*`\[\]()]/g, '')
      .replace(/\n+/g, ' ')
      .trim();
    return plainText.length > 200 ? plainText.substring(0, 200) + '...' : plainText;
  };

  const handleClick = () => {
    if (onCardClick) {
      onCardClick();
    }
  };

  return (
    <Card
      className={styles.card}
      appearance="filled-alternative"
      onClick={handleClick}
    >
      {content.is_featured && (
        <div className={styles.featuredBadge}>
          <StarFilled color={tokens.colorWarning} fontSize={20} />
        </div>
      )}

      <CardHeader
        header={
          <Text className={styles.title}>
            {content.title || 'Untitled'}
          </Text>
        }
        description={
          <div className={styles.tags}>
            {content.content_type && (
              <Badge
                appearance="tint"
                color="brand"
                className={styles.categoryBadge}
              >
                {content.content_type}
              </Badge>
            )}
            {content.category && (
              <Badge
                appearance="tint"
                color="informative"
                className={styles.categoryBadge}
              >
                {content.category}
              </Badge>
            )}
            {content.status === 'draft' && (
              <Badge appearance="tint" color="warning">
                Draft
              </Badge>
            )}
          </div>
        }
      />

      <CardPreview className={styles.preview}>
        <Body1 className={styles.excerpt}>
          {getExcerpt()}
        </Body1>
      </CardPreview>

      <div className={styles.cardHeader}>
        <div className={styles.metadata}>
          <div className={styles.metaItem}>
            <CalendarRegular fontSize={14} />
            <Caption1>{formatDate(content.updated_at || content.created_at)}</Caption1>
          </div>

          {showStats && content.view_count !== undefined && (
            <div className={styles.metaItem}>
              <EyeRegular fontSize={14} />
              <Caption1>{content.view_count} views</Caption1>
            </div>
          )}

          {showAuthor && content.author_id && (
            <div className={styles.metaItem}>
              <PersonRegular fontSize={14} />
              <Caption1>Author</Caption1>
            </div>
          )}
        </div>

        {content.tags && content.tags.length > 0 && (
          <div className={styles.tags} style={{ marginTop: tokens.spacingVerticalS }}>
            {content.tags.slice(0, 3).map((tag, index) => (
              <Badge
                key={index}
                appearance="outline"
                size="small"
                shape="rounded"
              >
                {tag}
              </Badge>
            ))}
            {content.tags.length > 3 && (
              <Caption1>+{content.tags.length - 3} more</Caption1>
            )}
          </div>
        )}
      </div>
    </Card>
  );
}