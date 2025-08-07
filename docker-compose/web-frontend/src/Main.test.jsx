import { describe, it, expect, vi } from 'vitest';

// Mock App
vi.mock('./App.jsx', () => ({
  default: () => <div>Mocked App</div>,
}));

// Mock react-dom/client BEFORE importing main.jsx
const mockRender = vi.fn();
const mockCreateRoot = vi.fn(() => ({ render: mockRender }));

vi.mock('react-dom/client', () => ({
  createRoot: mockCreateRoot,
}));

describe('main.jsx', () => {
  it('renders App inside StrictMode to #root', async () => {
    const rootElement = document.createElement('div');
    rootElement.id = 'root';
    document.body.appendChild(rootElement);

    // Import AFTER mocks
    await import('./main.jsx');

    expect(mockCreateRoot).toHaveBeenCalledWith(rootElement);
    expect(mockRender).toHaveBeenCalled();
  });
});
