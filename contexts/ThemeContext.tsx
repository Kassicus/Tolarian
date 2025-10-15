'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { FluentProvider } from '@fluentui/react-components';
import { lightTheme, darkTheme } from '@/styles/theme';

type ThemeMode = 'light' | 'dark' | 'system';

interface ThemeContextType {
  themeMode: ThemeMode;
  actualTheme: 'light' | 'dark';
  setThemeMode: (mode: ThemeMode) => void;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

interface ThemeProviderProps {
  children: React.ReactNode;
}

export function ThemeProvider({ children }: ThemeProviderProps) {
  const [themeMode, setThemeMode] = useState<ThemeMode>('system');
  const [actualTheme, setActualTheme] = useState<'light' | 'dark'>('light');
  const [mounted, setMounted] = useState(false);

  // Detect system preference
  const getSystemTheme = (): 'light' | 'dark' => {
    if (typeof window === 'undefined') return 'light';
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  };

  // Calculate actual theme based on mode
  const calculateActualTheme = (mode: ThemeMode): 'light' | 'dark' => {
    if (mode === 'system') {
      return getSystemTheme();
    }
    return mode;
  };

  // Initialize theme from localStorage and system preference
  useEffect(() => {
    setMounted(true);
    const savedTheme = localStorage.getItem('themeMode') as ThemeMode | null;
    if (savedTheme) {
      setThemeMode(savedTheme);
      setActualTheme(calculateActualTheme(savedTheme));
    } else {
      setActualTheme(getSystemTheme());
    }
  }, []);

  // Listen for system theme changes
  useEffect(() => {
    if (themeMode !== 'system') return;

    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = (e: MediaQueryListEvent) => {
      setActualTheme(e.matches ? 'dark' : 'light');
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [themeMode]);

  // Update theme mode
  const handleSetThemeMode = (mode: ThemeMode) => {
    setThemeMode(mode);
    const newActualTheme = calculateActualTheme(mode);
    setActualTheme(newActualTheme);
    localStorage.setItem('themeMode', mode);

    // Update document class for global styles
    if (newActualTheme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

  // Toggle between light and dark
  const toggleTheme = () => {
    const newMode = actualTheme === 'light' ? 'dark' : 'light';
    handleSetThemeMode(newMode);
  };

  const value: ThemeContextType = {
    themeMode,
    actualTheme,
    setThemeMode: handleSetThemeMode,
    toggleTheme,
  };

  // Prevent flash of unstyled content
  if (!mounted) {
    return <div style={{ visibility: 'hidden' }}>{children}</div>;
  }

  const theme = actualTheme === 'dark' ? darkTheme : lightTheme;

  return (
    <ThemeContext.Provider value={value}>
      <FluentProvider theme={theme}>
        {children}
      </FluentProvider>
    </ThemeContext.Provider>
  );
}