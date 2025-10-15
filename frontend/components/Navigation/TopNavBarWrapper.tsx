'use client';

import React from 'react';
import dynamic from 'next/dynamic';
import { useAuth } from '@/contexts/AuthContext';

// Dynamically import TopNavBar with no SSR to ensure it only renders on client
const TopNavBar = dynamic(
  () => import('./TopNavBar'),
  {
    ssr: false,
    loading: () => <div style={{ height: '64px', backgroundColor: '#f5f5f5' }} />
  }
);

interface TopNavBarWrapperProps {
  user?: any;
}

export default function TopNavBarWrapper({ user: userProp }: TopNavBarWrapperProps) {
  const { user: authUser } = useAuth();
  const user = userProp || authUser;

  return <TopNavBar user={user} />;
}