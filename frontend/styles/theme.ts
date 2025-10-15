import {
  createLightTheme,
  createDarkTheme,
  BrandVariants,
  Theme,
  tokens
} from '@fluentui/react-components';

// Define brand colors for Fluent Design
const brandColors: BrandVariants = {
  10: '#020305',
  20: '#0D1929',
  30: '#0E2648',
  40: '#0E3460',
  50: '#0E4278',
  60: '#0E5191',
  70: '#0E60AA',
  80: '#106EBE',
  90: '#2886DE',
  100: '#479EF5',
  110: '#6CB8F6',
  120: '#96CCF8',
  130: '#BBDCF9',
  140: '#D6E9FA',
  150: '#EBF3FC',
  160: '#F6FAFE'
};

// Create light and dark themes
export const lightTheme: Theme = {
  ...createLightTheme(brandColors),
};

export const darkTheme: Theme = {
  ...createDarkTheme(brandColors),
};

// Customize specific tokens for better Fluent Design alignment
lightTheme.colorNeutralBackground1 = '#FFFFFF';
lightTheme.colorNeutralBackground2 = '#F5F5F5';
lightTheme.colorNeutralBackground3 = '#EBEBEB';
lightTheme.colorBrandBackground = brandColors[80];
lightTheme.colorBrandForeground1 = brandColors[80];

darkTheme.colorNeutralBackground1 = '#1F1F1F';
darkTheme.colorNeutralBackground2 = '#2B2B2B';
darkTheme.colorNeutralBackground3 = '#323232';
darkTheme.colorBrandBackground = brandColors[100];
darkTheme.colorBrandForeground1 = brandColors[100];

// Fluent motion constants
export const fluentMotion = {
  durationUltraFast: tokens.durationUltraFast,
  durationFaster: tokens.durationFaster,
  durationFast: tokens.durationFast,
  durationNormal: tokens.durationNormal,
  durationSlow: tokens.durationSlow,
  durationSlower: tokens.durationSlower,
  durationUltraSlow: tokens.durationUltraSlow,

  curveAccelerateMax: tokens.curveAccelerateMax,
  curveAccelerateMid: tokens.curveAccelerateMid,
  curveAccelerateMin: tokens.curveAccelerateMin,
  curveDecelerateMax: tokens.curveDecelerateMax,
  curveDecelerateMid: tokens.curveDecelerateMid,
  curveDecelerateMin: tokens.curveDecelerateMin,
  curveEasyEase: tokens.curveEasyEase,
  curveLinear: tokens.curveLinear
};

// Fluent spacing system
export const fluentSpacing = {
  none: tokens.spacingHorizontalNone,
  xxs: tokens.spacingHorizontalXXS,
  xs: tokens.spacingHorizontalXS,
  sNudge: tokens.spacingHorizontalSNudge,
  s: tokens.spacingHorizontalS,
  mNudge: tokens.spacingHorizontalMNudge,
  m: tokens.spacingHorizontalM,
  l: tokens.spacingHorizontalL,
  xl: tokens.spacingHorizontalXL,
  xxl: tokens.spacingHorizontalXXL,
  xxxl: tokens.spacingHorizontalXXXL
};

// Fluent shadow system
export const fluentShadows = {
  shadow2: tokens.shadow2,
  shadow4: tokens.shadow4,
  shadow8: tokens.shadow8,
  shadow16: tokens.shadow16,
  shadow28: tokens.shadow28,
  shadow64: tokens.shadow64,

  brand2: tokens.shadow2Brand,
  brand4: tokens.shadow4Brand,
  brand8: tokens.shadow8Brand,
  brand16: tokens.shadow16Brand,
  brand28: tokens.shadow28Brand,
  brand64: tokens.shadow64Brand
};