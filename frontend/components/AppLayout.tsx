'use client';

import React from 'react';
import TopNavBarWrapper from '@/components/Navigation/TopNavBarWrapper';

interface AppLayoutProps {
  children: React.ReactNode;
  user?: any;
}

export default function AppLayout({ children, user }: AppLayoutProps) {
  return (
    <>
      <TopNavBarWrapper user={user} />
      <main>{children}</main>
    </>
  );
}