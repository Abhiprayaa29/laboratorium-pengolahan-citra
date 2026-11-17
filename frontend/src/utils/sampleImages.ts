/**
 * Helper to generate high-contrast clean sample canvas images for immediate testing
 * of morphology (erosion, dilation) and geometry (mirroring).
 */

export function generateSampleBinaryImage(): string {
  const canvas = document.createElement('canvas');
  canvas.width = 240;
  canvas.height = 240;
  const ctx = canvas.getContext('2d');
  if (!ctx) return '';

  // Black background
  ctx.fillStyle = '#000000';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // White shapes
  ctx.fillStyle = '#ffffff';

  // Centered square
  ctx.fillRect(40, 40, 60, 60);

  // White circle
  ctx.beginPath();
  ctx.arc(170, 70, 30, 0, Math.PI * 2);
  ctx.fill();

  // White text "LPCD"
  ctx.font = 'bold 36px monospace';
  ctx.fillText('LPCD', 60, 180);

  // Small dots/noise
  ctx.fillRect(20, 20, 4, 4);
  ctx.fillRect(210, 210, 6, 6);
  ctx.fillRect(30, 200, 3, 3);

  return canvas.toDataURL('image/png');
}

export function generateSampleColorImage(): string {
  const canvas = document.createElement('canvas');
  canvas.width = 240;
  canvas.height = 240;
  const ctx = canvas.getContext('2d');
  if (!ctx) return '';

  // Gradient background
  const grad = ctx.createLinearGradient(0, 0, 240, 240);
  grad.addColorStop(0, '#1e3a8a');
  grad.addColorStop(0.5, '#3b82f6');
  grad.addColorStop(1, '#93c5fd');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Red circle
  ctx.fillStyle = '#ef4444';
  ctx.beginPath();
  ctx.arc(70, 120, 45, 0, Math.PI * 2);
  ctx.fill();

  // Green rectangle
  ctx.fillStyle = '#10b981';
  ctx.fillRect(130, 75, 80, 90);

  // White label
  ctx.fillStyle = '#ffffff';
  ctx.font = 'bold 22px sans-serif';
  ctx.fillText('CITRA DIGITAL', 40, 210);

  return canvas.toDataURL('image/png');
}
