import { renderHook, act } from '@testing-library/react';
import { useIsMobile } from './use-mobile';

describe('useIsMobile', () => {
  const originalInnerWidth = global.innerWidth;

  beforeAll(() => {
    // Mock matchMedia
    Object.defineProperty(window, 'matchMedia', {
      writable: true,
      value: (query) => ({
        matches: window.innerWidth < 768,
        media: query,
        onchange: null,
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
        dispatchEvent: vi.fn(),
      }),
    });
  });

  beforeEach(() => {
    global.innerWidth = originalInnerWidth;
  });

  it('returns true when window width is less than MOBILE_BREAKPOINT', () => {
    global.innerWidth = 500;
    const { result } = renderHook(() => useIsMobile());
    expect(result.current).toBe(true);
  });

  it('returns false when window width is greater than or equal to MOBILE_BREAKPOINT', () => {
    global.innerWidth = 1024;
    const { result } = renderHook(() => useIsMobile());
    expect(result.current).toBe(false);
  });
});
