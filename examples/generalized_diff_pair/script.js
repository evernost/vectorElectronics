const leftCanvas = document.getElementById('leftCanvas');
const rightCanvas = document.getElementById('rightCanvas');
const leftCtx = leftCanvas.getContext('2d');
const rightCtx = rightCanvas.getContext('2d');

// Define the list of control points
let controlPoints = 
[
  { x: -0.5, y: 0.0 },
  { x: -0.1, y: 0.6 },
  { x: 0.3, y: 0.4 },
  { x: 1.0, y: 0.8 }
];

let draggingPoint = null;

// Convert data coordinates to canvas coordinates
function dataToCanvas(canvas, x, y, xMin, xMax, yMin, yMax) 
{
  const padding = 40;
  const w = canvas.width - 2 * padding;
  const h = canvas.height - 2 * padding;
  return {
    x: padding + ((x - xMin) / (xMax - xMin)) * w,
    y: canvas.height - padding - ((y - yMin) / (yMax - yMin)) * h
  };
}

// Convert canvas coordinates to data coordinates
function canvasToData(canvas, cx, cy, xMin, xMax, yMin, yMax)
{
  const padding = 40;
  const w = canvas.width - 2 * padding;
  const h = canvas.height - 2 * padding;
  return {
    x: xMin + ((cx - padding) / w) * (xMax - xMin),
    y: yMin + ((canvas.height - padding - cy) / h) * (yMax - yMin)
  };
}

// Draw axes and grid
function drawAxes(ctx, canvas, xMin, xMax, yMin, yMax, title)
{
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const padding = 40;
  
  // Draw title
  ctx.fillStyle = '#666';
  ctx.font = '12px Arial';
  ctx.textAlign = 'center';
  ctx.fillText(title, canvas.width / 2, 20);

  // Draw grid
  ctx.strokeStyle = '#eee';
  ctx.lineWidth = 1;
  for (let i = 0; i <= 10; i++)
  {
    const x = dataToCanvas(canvas, xMin + (xMax - xMin) * i / 10, 0, xMin, xMax, yMin, yMax).x;
    const y = dataToCanvas(canvas, 0, yMin + (yMax - yMin) * i / 10, xMin, xMax, yMin, yMax).y;
    
    ctx.beginPath();
    ctx.moveTo(x, padding);
    ctx.lineTo(x, canvas.height - padding);
    ctx.stroke();
    
    ctx.beginPath();
    ctx.moveTo(padding, y);
    ctx.lineTo(canvas.width - padding, y);
    ctx.stroke();
  }

  // Draw axes
  ctx.strokeStyle = '#333';
  ctx.lineWidth = 2;
  const origin = dataToCanvas(canvas, 0, 0, xMin, xMax, yMin, yMax);
  
  ctx.beginPath();
  ctx.moveTo(padding, origin.y);
  ctx.lineTo(canvas.width - padding, origin.y);
  ctx.stroke();
  
  ctx.beginPath();
  ctx.moveTo(origin.x, padding);
  ctx.lineTo(origin.x, canvas.height - padding);
  ctx.stroke();

  // Draw axis labels
  ctx.fillStyle = '#333';
  ctx.font = '10px Arial';
  ctx.textAlign = 'center';
  ctx.fillText(xMin.toFixed(1), padding, canvas.height - 25);
  ctx.fillText(xMax.toFixed(1), canvas.width - padding, canvas.height - 25);
  
  ctx.save();
  ctx.translate(15, canvas.height / 2);
  ctx.rotate(-Math.PI / 2);
  ctx.fillText(yMin.toFixed(1), 0, 0);
  ctx.restore();
  
  ctx.save();
  ctx.translate(15, padding);
  ctx.rotate(-Math.PI / 2);
  ctx.fillText(yMax.toFixed(1), 0, 0);
  ctx.restore();
}

// Get piecewise linear segments (offset, slope, domain)
function getPiecewiseSegments()
{
  const segments = [];
  const sorted = [...controlPoints].sort((a, b) => a.x - b.x);
  
  for (let i = 0; i < sorted.length - 1; i++)
  {
    const p1 = sorted[i];
    const p2 = sorted[i + 1];
    const slope = (p2.y - p1.y) / (p2.x - p1.x);
    const offset = p1.y - slope * p1.x;
    
    segments.push({
      offset: offset,
      slope: slope,
      xMin: p1.x,
      xMax: p2.x
    });
  }
  
  return segments;
}

// Evaluate piecewise linear function at x
function evaluatePiecewiseLinear(x)
{
  const segments = getPiecewiseSegments();
  for (let seg of segments)
  {
    if (x >= seg.xMin && x <= seg.xMax)
    {
      return seg.offset + seg.slope * x;
    }
  }
  return 0.0;
}

// Draw the piecewise linear function
function drawDeviceCurve()
{
  const xMin = -0.5, xMax = 1.0, yMin = -0.2, yMax = 1.2;
  drawAxes(leftCtx, leftCanvas, xMin, xMax, yMin, yMax, "I = f(delta V)");

  // Draw the piecewise linear function
  leftCtx.strokeStyle = '#2196F3';
  leftCtx.lineWidth = 2;
  leftCtx.beginPath();
  
  const sorted = [...controlPoints].sort((a, b) => a.x - b.x);
  sorted.forEach((p, i) => {
    const pos = dataToCanvas(leftCanvas, p.x, p.y, xMin, xMax, yMin, yMax);
    if (i === 0)
    {
      leftCtx.moveTo(pos.x, pos.y);
    }
    else
    {
      leftCtx.lineTo(pos.x, pos.y);
    }
  });
  leftCtx.stroke();

  // Draw control points
  sorted.forEach(p => {
    const pos = dataToCanvas(leftCanvas, p.x, p.y, xMin, xMax, yMin, yMax);
    leftCtx.fillStyle = '#FF5722';
    leftCtx.beginPath();
    leftCtx.arc(pos.x, pos.y, 6, 0, Math.PI * 2);
    leftCtx.fill();
    leftCtx.strokeStyle = '#fff';
    leftCtx.lineWidth = 2;
    leftCtx.stroke();
  });
}

// ============================================================================
// CUSTOM DERIVED FUNCTION - MODIFY THIS SECTION
// ============================================================================
function computeDerivedFunction(x)
{
  // You have access to:
  // 1. getPiecewiseSegments() - returns array of {offset, slope, xMin, xMax}
  // 2. evaluatePiecewiseLinear(x) - evaluates the piecewise function at x
  
  const segments = getPiecewiseSegments();
  
  // Example: Just return the original function (replace with your logic)
  const y = evaluatePiecewiseLinear(x);
  
  // Example: Return squared value
  // return y !== null ? y * y : null;
  
  // Example: Return derivative (slope at that point)
  // for (let seg of segments) {
  //   if (x >= seg.xMin && x <= seg.xMax) {
  //     return seg.slope;
  //   }
  // }
  
  return y;
}
// ============================================================================

// Draw the derived function
function drawTransferCurve()
{
  const xMin = -0.5, xMax = 1.0, yMin = -0.2, yMax = 1.2;
  drawAxes(rightCtx, rightCanvas, xMin, xMax, yMin, yMax, 'Derived Function');

  rightCtx.strokeStyle = '#4CAF50';
  rightCtx.lineWidth = 2;
  rightCtx.beginPath();
  
  let started = false;
  for (let i = 0; i <= 500; i++)
  {
    const x = xMin + (xMax - xMin) * i / 500;
    const y = computeDerivedFunction(x);
    
    if (y !== null)
    {
      const pos = dataToCanvas(rightCanvas, x, y, xMin, xMax, yMin, yMax);
      if (!started)
      {
        rightCtx.moveTo(pos.x, pos.y);
        started = true;
      }
      else
      {
        rightCtx.lineTo(pos.x, pos.y);
      }
    }
  }
  rightCtx.stroke();
}

function redraw()
{
  drawDeviceCurve();
  drawTransferCurve();
}

// Mouse event handlers
leftCanvas.addEventListener('mousedown', (e) => {
  const rect = leftCanvas.getBoundingClientRect();
  const cx = e.clientX - rect.left;
  const cy = e.clientY - rect.top;
  const data = canvasToData(leftCanvas, cx, cy, -0.5, 1.0, -0.2, 1.2);
  
  // Find closest point
  let minDist = Infinity;
  let closest = null;
  controlPoints.forEach(p => {
    const dist = Math.sqrt((p.x - data.x) ** 2 + (p.y - data.y) ** 2);
    if (dist < minDist) {
      minDist = dist;
      closest = p;
    }
  });
  
  if (minDist < 0.1) {
    draggingPoint = closest;
  }
});

leftCanvas.addEventListener('mousemove', (e) => {
  if (draggingPoint) {
    const rect = leftCanvas.getBoundingClientRect();
    const cx = e.clientX - rect.left;
    const cy = e.clientY - rect.top;
    const data = canvasToData(leftCanvas, cx, cy, -0.5, 1.0, -0.2, 1.2);
    
    draggingPoint.x = Math.max(-0.5, Math.min(1.0, data.x));
    draggingPoint.y = Math.max(-0.2, Math.min(1.2, data.y));
    redraw();
  }
});

leftCanvas.addEventListener('mouseup', () => {
  draggingPoint = null;
});

leftCanvas.addEventListener('mouseleave', () => {
  draggingPoint = null;
});

// Initial draw
redraw();