'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import {
  Button,
  Menu,
  MenuTrigger,
  MenuPopover,
  MenuList,
  MenuItem,
  MenuDivider,
  Persona,
  SearchBox,
  Tooltip,
  tokens,
  makeStyles,
  shorthands,
  Switch,
} from '@fluentui/react-components';
import {
  BookRegular,
  HomeRegular,
  DocumentTextRegular,
  SearchRegular,
  SettingsRegular,
  PersonRegular,
  SignOutRegular,
  DarkThemeRegular,
  WeatherSunnyRegular,
  AddRegular,
} from '@fluentui/react-icons';
import { useTheme } from '@/contexts/ThemeContext';

const useStyles = makeStyles({
  navbar: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    ...shorthands.padding(tokens.spacingVerticalM, tokens.spacingHorizontalL),
    backgroundColor: tokens.colorNeutralBackground2,
    boxShadow: tokens.shadow4,
    position: 'sticky',
    top: 0,
    zIndex: 1000,
    backdropFilter: 'blur(20px)',
  },

  brand: {
    display: 'flex',
    alignItems: 'center',
    ...shorthands.gap(tokens.spacingHorizontalM),
    fontSize: tokens.fontSizeBase500,
    fontWeight: tokens.fontWeightSemibold,
    color: tokens.colorBrandForeground1,
    textDecoration: 'none',
  },

  navItems: {
    display: 'flex',
    alignItems: 'center',
    ...shorthands.gap(tokens.spacingHorizontalM),
    '@media (max-width: 768px)': {
      display: 'none',
    },
  },

  navLink: {
    display: 'flex',
    alignItems: 'center',
    ...shorthands.gap(tokens.spacingHorizontalXS),
    ...shorthands.padding(tokens.spacingVerticalS, tokens.spacingHorizontalM),
    borderRadius: tokens.borderRadiusMedium,
    textDecoration: 'none',
    color: tokens.colorNeutralForeground2,
    transition: 'all 0.2s ease',
    ':hover': {
      backgroundColor: tokens.colorNeutralBackground2Hover,
      color: tokens.colorNeutralForeground1,
    },
  },

  activeLink: {
    backgroundColor: tokens.colorBrandBackground2,
    color: tokens.colorBrandForeground1,
  },

  rightSection: {
    display: 'flex',
    alignItems: 'center',
    ...shorthands.gap(tokens.spacingHorizontalM),
  },

  searchBox: {
    minWidth: '250px',
    '@media (max-width: 768px)': {
      minWidth: '150px',
    },
  },

  themeSection: {
    display: 'flex',
    alignItems: 'center',
    ...shorthands.gap(tokens.spacingHorizontalS),
  },
});

interface NavItem {
  label: string;
  href: string;
  icon: React.ReactElement;
}

interface TopNavBarProps {
  user?: {
    id: string;
    email: string;
    role: string;
    avatar_url?: string;
    full_name?: string;
  };
}

export default function TopNavBar({ user }: TopNavBarProps) {
  const styles = useStyles();
  const router = useRouter();
  const { actualTheme, toggleTheme } = useTheme();
  const [searchQuery, setSearchQuery] = useState('');

  const navItems: NavItem[] = [
    { label: 'Home', href: '/', icon: <HomeRegular /> },
    { label: 'Content', href: '/content', icon: <DocumentTextRegular /> },
    { label: 'Search', href: '/search', icon: <SearchRegular /> },
  ];

  if (user?.role === 'admin') {
    navItems.push({ label: 'Admin', href: '/admin', icon: <SettingsRegular /> });
  }

  const handleSearch = (value: string) => {
    if (value.trim()) {
      router.push(`/search?q=${encodeURIComponent(value)}`);
    }
  };

  const handleLogout = async () => {
    // Call logout API
    router.push('/login');
  };

  return (
    <nav className={styles.navbar}>
      {/* Brand */}
      <Link href="/" className={styles.brand}>
        <BookRegular fontSize={24} />
        <span>Tolarian</span>
      </Link>

      {/* Navigation Items */}
      <div className={styles.navItems}>
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={`${styles.navLink} ${
              typeof window !== 'undefined' && window.location.pathname === item.href
                ? styles.activeLink
                : ''
            }`}
          >
            {item.icon}
            <span>{item.label}</span>
          </Link>
        ))}
      </div>

      {/* Right Section */}
      <div className={styles.rightSection}>
        {/* Search */}
        <SearchBox
          className={styles.searchBox}
          placeholder="Search..."
          value={searchQuery}
          onChange={(e, data) => setSearchQuery(data.value)}
          onClear={() => setSearchQuery('')}
          size="medium"
          appearance="filled-lighter"
          contentAfter={<SearchRegular />}
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              handleSearch(searchQuery);
            }
          }}
        />

        {/* Theme Toggle */}
        <div className={styles.themeSection}>
          <Tooltip content={actualTheme === 'light' ? 'Dark mode' : 'Light mode'} relationship="label">
            <Switch
              checked={actualTheme === 'dark'}
              onChange={toggleTheme}
              indicator={{
                children: actualTheme === 'dark' ? <DarkThemeRegular /> : <WeatherSunnyRegular />,
              }}
            />
          </Tooltip>
        </div>

        {/* User Menu */}
        {user ? (
          <Menu>
            <MenuTrigger disableButtonEnhancement>
              <Button
                appearance="subtle"
                icon={
                  <Persona
                    name={user.full_name || user.email}
                    secondaryText={user.role}
                    size="small"
                    avatar={{
                      image: user.avatar_url ? { src: user.avatar_url } : undefined,
                      initials: user.email.substring(0, 2).toUpperCase(),
                    }}
                  />
                }
              />
            </MenuTrigger>
            <MenuPopover>
              <MenuList>
                <MenuItem icon={<PersonRegular />} onClick={() => router.push('/profile')}>
                  Profile
                </MenuItem>
                <MenuItem icon={<DocumentTextRegular />} onClick={() => router.push('/my-content')}>
                  My Content
                </MenuItem>
                {user.role === 'editor' || user.role === 'admin' ? (
                  <MenuItem icon={<AddRegular />} onClick={() => router.push('/content/new')}>
                    Create Content
                  </MenuItem>
                ) : null}
                <MenuDivider />
                <MenuItem icon={<SignOutRegular />} onClick={handleLogout}>
                  Logout
                </MenuItem>
              </MenuList>
            </MenuPopover>
          </Menu>
        ) : (
          <Button appearance="primary" onClick={() => router.push('/login')}>
            Login
          </Button>
        )}
      </div>
    </nav>
  );
}