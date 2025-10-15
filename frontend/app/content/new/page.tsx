'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import {
  Title1,
  Body1,
  Button,
  Card,
  makeStyles,
  shorthands,
  tokens,
  Input,
  Textarea,
  Dropdown,
  Option,
  MessageBar,
  MessageBarBody,
  MessageBarTitle,
  Switch,
  Label,
  TabList,
  Tab,
  Badge,
} from '@fluentui/react-components';
import {
  SaveRegular,
  DismissRegular,
  DocumentTextRegular,
  PreviewLinkRegular,
  TagRegular,
} from '@fluentui/react-icons';
import ReactMarkdown from 'react-markdown';
import TopNavBarWrapper from '@/components/Navigation/TopNavBarWrapper';
import apiClient from '@/services/api';
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
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },

  mainContent: {
    maxWidth: '1200px',
    ...shorthands.margin('0', 'auto'),
    ...shorthands.padding(tokens.spacingVerticalXL, tokens.spacingHorizontalL),
  },

  editorCard: {
    ...shorthands.padding(tokens.spacingVerticalXL, tokens.spacingHorizontalXL),
  },

  formSection: {
    marginBottom: tokens.spacingVerticalXL,
  },

  formRow: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: tokens.spacingHorizontalL,
    marginBottom: tokens.spacingVerticalL,
    '@media (max-width: 768px)': {
      gridTemplateColumns: '1fr',
    },
  },

  fullWidth: {
    gridColumn: '1 / -1',
  },

  label: {
    marginBottom: tokens.spacingVerticalS,
    fontWeight: tokens.fontWeightSemibold,
  },

  input: {
    width: '100%',
  },

  textarea: {
    width: '100%',
    minHeight: '400px',
    fontFamily: 'Consolas, Monaco, "Courier New", monospace',
  },

  preview: {
    ...shorthands.padding(tokens.spacingVerticalL),
    backgroundColor: tokens.colorNeutralBackground2,
    borderRadius: tokens.borderRadiusMedium,
    minHeight: '400px',
    '& h1': {
      fontSize: tokens.fontSizeHero700,
      fontWeight: tokens.fontWeightBold,
      marginTop: tokens.spacingVerticalXL,
      marginBottom: tokens.spacingVerticalL,
    },
    '& h2': {
      fontSize: tokens.fontSizeBase600,
      fontWeight: tokens.fontWeightSemibold,
      marginTop: tokens.spacingVerticalL,
      marginBottom: tokens.spacingVerticalM,
    },
    '& h3': {
      fontSize: tokens.fontSizeBase500,
      fontWeight: tokens.fontWeightSemibold,
      marginTop: tokens.spacingVerticalM,
      marginBottom: tokens.spacingVerticalS,
    },
    '& p': {
      marginBottom: tokens.spacingVerticalM,
      lineHeight: '1.8',
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
    },
    '& pre': {
      backgroundColor: tokens.colorNeutralBackground3,
      ...shorthands.padding(tokens.spacingVerticalM),
      borderRadius: tokens.borderRadiusMedium,
      overflowX: 'auto',
      '& code': {
        backgroundColor: 'transparent',
        padding: 0,
      },
    },
  },

  tabs: {
    marginBottom: tokens.spacingVerticalL,
  },

  tagInput: {
    display: 'flex',
    gap: tokens.spacingHorizontalS,
    marginBottom: tokens.spacingVerticalS,
  },

  tagList: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: tokens.spacingHorizontalXS,
  },

  actions: {
    display: 'flex',
    gap: tokens.spacingHorizontalM,
    justifyContent: 'flex-end',
    marginTop: tokens.spacingVerticalXL,
    paddingTop: tokens.spacingVerticalL,
    borderTop: `1px solid ${tokens.colorNeutralStroke1}`,
  },

  errorMessage: {
    marginBottom: tokens.spacingVerticalL,
  },

  unauthorized: {
    textAlign: 'center',
    ...shorthands.padding(tokens.spacingVerticalXXXL),
  },
});

type PreviewMode = 'edit' | 'preview' | 'split';

export default function CreateContentPage() {
  const styles = useStyles();
  const router = useRouter();
  const { user } = useAuth();

  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [contentType, setContentType] = useState('document');
  const [category, setCategory] = useState('');
  const [tags, setTags] = useState<string[]>([]);
  const [tagInput, setTagInput] = useState('');
  const [isDraft, setIsDraft] = useState(true);
  const [isFeatured, setIsFeatured] = useState(false);
  const [previewMode, setPreviewMode] = useState<PreviewMode>('split');
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Check if user has permission to create content
  const canCreate = user && (user.role === 'editor' || user.role === 'admin');

  const handleAddTag = () => {
    if (tagInput.trim() && !tags.includes(tagInput.trim())) {
      setTags([...tags, tagInput.trim()]);
      setTagInput('');
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setTags(tags.filter((tag) => tag !== tagToRemove));
  };

  const handleSave = async () => {
    // Validate required fields
    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    if (!content.trim()) {
      setError('Content is required');
      return;
    }

    if (!category) {
      setError('Please select a category');
      return;
    }

    setSaving(true);
    setError(null);

    try {
      const response = await apiClient.createContent({
        title: title.trim(),
        content: content.trim(),
        category,
        tags,
      });

      if (response.success && response.data) {
        // Redirect to the newly created content
        router.push(`/content/${response.data.id}`);
      } else {
        setError(response.message || 'Failed to create content');
      }
    } catch (err: any) {
      setError(err.message || 'An error occurred while saving');
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    if (
      (title || content) &&
      !window.confirm('Are you sure you want to discard your changes?')
    ) {
      return;
    }
    router.push('/content');
  };

  if (!canCreate) {
    return (
      <div className={styles.container}>
        <TopNavBarWrapper user={user} />
        <div className={styles.unauthorized}>
          <Title1>Unauthorized</Title1>
          <Body1>You don't have permission to create content.</Body1>
          <Button
            appearance="primary"
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
          <Title1>
            <DocumentTextRegular /> Create New Content
          </Title1>
          <div className={styles.actions}>
            <Button
              appearance="outline"
              icon={<DismissRegular />}
              onClick={handleCancel}
            >
              Cancel
            </Button>
            <Button
              appearance="primary"
              icon={<SaveRegular />}
              onClick={handleSave}
              disabled={saving}
            >
              {saving ? 'Saving...' : 'Save Content'}
            </Button>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <section className={styles.mainContent}>
        <Card className={styles.editorCard}>
          {error && (
            <MessageBar intent="error" className={styles.errorMessage}>
              <MessageBarBody>
                <MessageBarTitle>Error</MessageBarTitle>
                {error}
              </MessageBarBody>
            </MessageBar>
          )}

          {/* Basic Information */}
          <div className={styles.formSection}>
            <div className={styles.formRow}>
              <div>
                <Label className={styles.label} required>
                  Title
                </Label>
                <Input
                  className={styles.input}
                  value={title}
                  onChange={(e, data) => setTitle(data.value)}
                  placeholder="Enter content title"
                  size="large"
                />
              </div>

              <div>
                <Label className={styles.label} required>
                  Category
                </Label>
                <Dropdown
                  placeholder="Select a category"
                  value={category}
                  onOptionSelect={(e, data) =>
                    setCategory(data.optionValue as string)
                  }
                >
                  <Option value="development">Development</Option>
                  <Option value="templates">Templates</Option>
                  <Option value="guides">Guides</Option>
                  <Option value="documentation">Documentation</Option>
                </Dropdown>
              </div>
            </div>

            <div className={styles.formRow}>
              <div>
                <Label className={styles.label}>Content Type</Label>
                <Dropdown
                  value={contentType}
                  onOptionSelect={(e, data) =>
                    setContentType(data.optionValue as string)
                  }
                >
                  <Option value="document">Document</Option>
                  <Option value="template">Template</Option>
                  <Option value="guide">Guide</Option>
                  <Option value="link">Link</Option>
                </Dropdown>
              </div>

              <div>
                <Label className={styles.label}>Tags</Label>
                <div className={styles.tagInput}>
                  <Input
                    className={styles.input}
                    value={tagInput}
                    onChange={(e, data) => setTagInput(data.value)}
                    placeholder="Add tags..."
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') {
                        e.preventDefault();
                        handleAddTag();
                      }
                    }}
                  />
                  <Button onClick={handleAddTag} icon={<TagRegular />}>
                    Add
                  </Button>
                </div>
                <div className={styles.tagList}>
                  {tags.map((tag) => (
                    <Badge
                      key={tag}
                      appearance="tint"
                      shape="rounded"
                      onClick={() => handleRemoveTag(tag)}
                      style={{ cursor: 'pointer' }}
                    >
                      {tag} ×
                    </Badge>
                  ))}
                </div>
              </div>
            </div>

            <div className={styles.formRow}>
              <div>
                <Switch
                  label="Save as Draft"
                  checked={isDraft}
                  onChange={(e, data) => setIsDraft(data.checked)}
                />
              </div>
              <div>
                <Switch
                  label="Featured Content"
                  checked={isFeatured}
                  onChange={(e, data) => setIsFeatured(data.checked)}
                />
              </div>
            </div>
          </div>

          {/* Content Editor */}
          <div className={styles.formSection}>
            <TabList
              selectedValue={previewMode}
              onTabSelect={(e, data) =>
                setPreviewMode(data.value as PreviewMode)
              }
              className={styles.tabs}
            >
              <Tab value="edit" icon={<DocumentTextRegular />}>
                Edit
              </Tab>
              <Tab value="preview" icon={<PreviewLinkRegular />}>
                Preview
              </Tab>
              <Tab value="split">Split View</Tab>
            </TabList>

            {previewMode === 'edit' && (
              <div>
                <Label className={styles.label} required>
                  Content (Markdown)
                </Label>
                <Textarea
                  className={styles.textarea}
                  value={content}
                  onChange={(e, data) => setContent(data.value)}
                  placeholder="Write your content in Markdown format..."
                />
              </div>
            )}

            {previewMode === 'preview' && (
              <div className={styles.preview}>
                {content ? (
                  <ReactMarkdown>{content}</ReactMarkdown>
                ) : (
                  <Body1>No content to preview</Body1>
                )}
              </div>
            )}

            {previewMode === 'split' && (
              <div
                style={{
                  display: 'grid',
                  gridTemplateColumns: '1fr 1fr',
                  gap: tokens.spacingHorizontalL,
                }}
              >
                <div>
                  <Label className={styles.label}>Edit</Label>
                  <Textarea
                    className={styles.textarea}
                    value={content}
                    onChange={(e, data) => setContent(data.value)}
                    placeholder="Write your content in Markdown format..."
                  />
                </div>
                <div>
                  <Label className={styles.label}>Preview</Label>
                  <div className={styles.preview}>
                    {content ? (
                      <ReactMarkdown>{content}</ReactMarkdown>
                    ) : (
                      <Body1>No content to preview</Body1>
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>
        </Card>
      </section>
    </div>
  );
}