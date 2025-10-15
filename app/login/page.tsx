'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import {
  Card,
  CardHeader,
  Title1,
  Body1,
  Input,
  Button,
  Checkbox,
  makeStyles,
  shorthands,
  tokens,
  MessageBar,
  MessageBarTitle,
  MessageBarBody,
  Spinner,
} from '@fluentui/react-components';
import {
  PersonRegular,
  KeyRegular,
  BookRegular,
} from '@fluentui/react-icons';
import { useAuth } from '@/contexts/AuthContext';

const useStyles = makeStyles({
  container: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: `linear-gradient(135deg, ${tokens.colorBrandBackground2} 0%, ${tokens.colorNeutralBackground1} 100%)`,
    ...shorthands.padding(tokens.spacingVerticalXL),
  },

  card: {
    width: '100%',
    maxWidth: '400px',
    ...shorthands.padding(tokens.spacingVerticalXXL, tokens.spacingHorizontalXXL),
  },

  header: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    marginBottom: tokens.spacingVerticalXXL,
  },

  logo: {
    display: 'flex',
    alignItems: 'center',
    gap: tokens.spacingHorizontalM,
    marginBottom: tokens.spacingVerticalL,
    color: tokens.colorBrandForeground1,
  },

  title: {
    textAlign: 'center',
  },

  subtitle: {
    textAlign: 'center',
    color: tokens.colorNeutralForeground3,
    marginTop: tokens.spacingVerticalS,
  },

  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: tokens.spacingVerticalL,
  },

  inputGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: tokens.spacingVerticalS,
  },

  label: {
    fontWeight: tokens.fontWeightSemibold,
    color: tokens.colorNeutralForeground1,
  },

  input: {
    width: '100%',
  },

  rememberRow: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },

  submitButton: {
    width: '100%',
    marginTop: tokens.spacingVerticalM,
  },

  divider: {
    display: 'flex',
    alignItems: 'center',
    gap: tokens.spacingHorizontalM,
    marginTop: tokens.spacingVerticalXL,
    marginBottom: tokens.spacingVerticalXL,
    '&::before': {
      content: '""',
      flex: 1,
      height: '1px',
      backgroundColor: tokens.colorNeutralStroke1,
    },
    '&::after': {
      content: '""',
      flex: 1,
      height: '1px',
      backgroundColor: tokens.colorNeutralStroke1,
    },
  },

  dividerText: {
    color: tokens.colorNeutralForeground3,
    fontSize: tokens.fontSizeBase200,
  },

  footer: {
    textAlign: 'center',
    marginTop: tokens.spacingVerticalXL,
    color: tokens.colorNeutralForeground3,
  },

  link: {
    color: tokens.colorBrandForeground1,
    textDecoration: 'none',
    ':hover': {
      textDecoration: 'underline',
    },
  },

  errorMessage: {
    marginBottom: tokens.spacingVerticalL,
  },
});

export default function LoginPage() {
  const styles = useStyles();
  const router = useRouter();
  const { login } = useAuth();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [remember, setRemember] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Reset error state
    setError(null);

    // Basic validation
    if (!email || !password) {
      setError('Please enter both email and password');
      return;
    }

    if (!email.includes('@')) {
      setError('Please enter a valid email address');
      return;
    }

    setLoading(true);

    try {
      await login(email, password);
      // Login function handles redirect
    } catch (err: any) {
      setError(err.message || 'Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <Card className={styles.card} appearance="filled-alternative">
        <div className={styles.header}>
          <div className={styles.logo}>
            <BookRegular fontSize={48} />
          </div>
          <Title1 className={styles.title}>Welcome Back</Title1>
          <Body1 className={styles.subtitle}>
            Sign in to access your knowledge base
          </Body1>
        </div>

        {error && (
          <MessageBar
            intent="error"
            className={styles.errorMessage}
          >
            <MessageBarBody>
              <MessageBarTitle>Login Failed</MessageBarTitle>
              {error}
            </MessageBarBody>
          </MessageBar>
        )}

        <form className={styles.form} onSubmit={handleSubmit}>
          <div className={styles.inputGroup}>
            <label className={styles.label} htmlFor="email">
              Email
            </label>
            <Input
              id="email"
              className={styles.input}
              type="email"
              value={email}
              onChange={(e, data) => setEmail(data.value)}
              placeholder="Enter your email"
              size="large"
              contentBefore={<PersonRegular />}
              disabled={loading}
              required
            />
          </div>

          <div className={styles.inputGroup}>
            <label className={styles.label} htmlFor="password">
              Password
            </label>
            <Input
              id="password"
              className={styles.input}
              type="password"
              value={password}
              onChange={(e, data) => setPassword(data.value)}
              placeholder="Enter your password"
              size="large"
              contentBefore={<KeyRegular />}
              disabled={loading}
              required
            />
          </div>

          <div className={styles.rememberRow}>
            <Checkbox
              label="Remember me"
              checked={remember}
              onChange={(e, data) => setRemember(!!data.checked)}
              disabled={loading}
            />
            <Link href="/forgot-password" className={styles.link}>
              Forgot password?
            </Link>
          </div>

          <Button
            className={styles.submitButton}
            appearance="primary"
            size="large"
            type="submit"
            disabled={loading}
            icon={loading ? <Spinner size="tiny" /> : undefined}
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </Button>
        </form>

        <div className={styles.divider}>
          <span className={styles.dividerText}>or</span>
        </div>

        <Button
          className={styles.submitButton}
          appearance="outline"
          size="large"
          onClick={() => router.push('/')}
          disabled={loading}
        >
          Continue as Guest
        </Button>

        <div className={styles.footer}>
          Don't have an account?{' '}
          <Link href="/register" className={styles.link}>
            Sign up
          </Link>
        </div>
      </Card>
    </div>
  );
}